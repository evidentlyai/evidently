import datetime
import json
import os
import time
import uuid
from copy import deepcopy
from typing import List

import pytest
from litestar.testing import TestClient

import evidently
from evidently._pydantic_compat import parse_obj_as
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import Options
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.suite.base_suite import ContextPayload
from evidently.suite.base_suite import Snapshot
from evidently.ui.base import ProjectManager
from evidently.ui.dashboards import CounterAgg
from evidently.ui.dashboards import DashboardPanelCounter
from evidently.ui.dashboards import ReportFilter
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.storage.local import FSSpecBlobStorage
from evidently.ui.type_aliases import ZERO_UUID
from evidently.utils import NumpyEncoder
from tests.ui.conftest import HEADERS
from tests.ui.conftest import _dumps


def test_list_projects(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects"""
    r = test_client.get("/api/projects")
    r.raise_for_status()
    assert r.json() == []

    project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    r = test_client.get("/api/projects")
    r.raise_for_status()
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == mock_project.name


def test_add_project(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """post /api/projects"""
    r = test_client.post("/api/projects", content=_dumps(mock_project), headers=HEADERS)
    r.raise_for_status()

    data = project_manager.list_projects(ZERO_UUID, None, None)
    assert len(data) == 1
    assert data[0].name == mock_project.name


def test_get_project_info(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/info"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    r = test_client.get(f"/api/projects/{project.id}/info")
    r.raise_for_status()

    data = r.json()

    assert json.dumps(data) == _dumps(project)


def test_update_project_info(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """post /api/projects/{project_id}/info"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    project2 = deepcopy(project)
    project2.name = "mock2"
    r = test_client.post(f"/api/projects/{project.id}/info", content=_dumps(project2), headers=HEADERS)
    r.raise_for_status()

    assert project_manager.get_project(ZERO_UUID, project.id).name == "mock2"


def test_projects_search(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/search/{project_name}"""

    r = test_client.get(f"/api/projects/search/{mock_project.name}")
    r.raise_for_status()
    assert r.json() == []

    project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    r = test_client.get(f"/api/projects/search/{mock_project.name}")
    r.raise_for_status()
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == mock_project.name

    r = test_client.get(f"/api/projects/search/{mock_project.name}_2")
    r.raise_for_status()
    assert r.json() == []


def test_delete_project(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """delete /api/projects/{project_id}"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    assert len(project_manager.list_projects(ZERO_UUID, None, None)) == 1
    r = test_client.delete(f"/api/projects/{project.id}")
    r.raise_for_status()
    assert len(project_manager.list_projects(ZERO_UUID, None, None)) == 0


class MockMetricResult(MetricResult):
    value: float

    @classmethod
    def create(cls, value: float):
        return MockMetricResult(value=value)


class MockMetric(Metric[MockMetricResult]):
    def calculate(self, data: InputData) -> MockMetricResult:
        return MockMetricResult.create(1)


@default_renderer(wrap_type=MockMetric)
class MockMetricRenderer(MetricRenderer):
    def render_html(self, obj) -> List[BaseWidgetInfo]:
        widget = counter(counters=[CounterData("title", "text")], size=WidgetSize.FULL)
        widget.additionalGraphs = [counter(counters=[CounterData("title2", "text2")], size=WidgetSize.FULL)]
        return [widget]


@pytest.fixture
def mock_snapshot():
    return Snapshot(
        id=uuid.uuid4(),
        name="mock",
        timestamp=datetime.datetime.now(),
        metadata={},
        tags=[],
        suite=ContextPayload(
            metrics=[MockMetric()],
            metric_results=[MockMetricResult.create(1)],
            tests=[],
            test_results=[],
            options=Options(),
        ),
        metrics_ids=[],
        test_ids=[],
        options=Options(),
    )


def test_add_snapshot(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """post /api/projects/{project_id}/snapshots"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 0
    r = test_client.post(f"/api/projects/{project.id}/snapshots", content=_dumps(mock_snapshot), headers=HEADERS)
    r.raise_for_status()

    snapshots = project_manager.list_snapshots(ZERO_UUID, project.id)
    assert len(snapshots) == 1
    assert snapshots[0].id == mock_snapshot.id


def test_delete_snapshot(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """delete /api/projects/{project_id}/{snapshot_id}"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1
    time.sleep(0.1)  # try to avoid WinError 32 error (file used by another process)
    r = test_client.delete(f"/api/projects/{project.id}/{mock_snapshot.id}")
    r.raise_for_status()

    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 0


def test_get_project_reports(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """get /api/projects/{project_id}/reports"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    mock_snapshot.metrics_ids = [0]
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    r = test_client.get(f"/api/projects/{project.id}/reports")
    r.raise_for_status()
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == str(mock_snapshot.id)


def test_get_project_test_suites(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """get /api/projects/{project_id}/test_suites"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    r = test_client.get(f"/api/projects/{project.id}/test_suites")
    r.raise_for_status()
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == str(mock_snapshot.id)


def test_get_snapshot_data(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """get /api/projects/{project_id}/{snapshot_id}/data"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    mock_snapshot.metrics_ids = [0]
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    r = test_client.get(f"/api/projects/{project.id}/{mock_snapshot.id}/data")
    r.raise_for_status()
    data = r.json()
    fp = MockMetric().get_fingerprint()
    assert data == {
        "max_timestamp": None,
        "min_timestamp": None,
        "name": "Report",
        "widgets": [
            {
                "additionalGraphs": [
                    {
                        "additionalGraphs": [],
                        "alertStats": None,
                        "alerts": [],
                        "alertsPosition": None,
                        "details": "",
                        "id": "MockMetric-1",
                        "insights": [],
                        "pageSize": 5,
                        "params": {"counters": [{"label": "title2", "value": "text2"}]},
                        "size": 2,
                        "tabs": [],
                        "title": "",
                        "type": "counter",
                        "widgets": [],
                        "source_fingerprint": None,
                    }
                ],
                "alertStats": None,
                "alerts": [],
                "alertsPosition": None,
                "details": "",
                "id": "MockMetric-0",
                "insights": [],
                "pageSize": 5,
                "params": {"counters": [{"label": "title", "value": "text"}]},
                "size": 2,
                "tabs": [],
                "title": "",
                "type": "counter",
                "widgets": [],
                "source_fingerprint": fp,
            }
        ],
    }


def test_get_projects_graphs_data(
    test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot
):
    """get /api/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    mock_snapshot.metrics_ids = [0]
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    r = test_client.get(f"/api/projects/{project.id}/{mock_snapshot.id}/graphs_data/MockMetric-1")
    r.raise_for_status()
    data = r.json()

    assert data == {
        "additionalGraphs": [],
        "alertStats": None,
        "alerts": [],
        "alertsPosition": None,
        "details": "",
        "id": "MockMetric-1",
        "insights": [],
        "pageSize": 5,
        "params": {"counters": [{"label": "title2", "value": "text2"}]},
        "size": 2,
        "tabs": [],
        "title": "",
        "type": "counter",
        "widgets": [],
        "source_fingerprint": None,
    }


@pytest.mark.parametrize("report_format", ["html", "json"])
def test_download_snapshot(
    test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot, report_format
):
    """get /api/projects/{project_id}/{snapshot_id}/download"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    mock_snapshot.metrics_ids = [0]
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    r = test_client.get(
        f"/api/projects/{project.id}/{mock_snapshot.id}/download", params={"report_format": report_format}
    )
    r.raise_for_status()
    if report_format == "json":
        data = r.json()
        data["timestamp"] = None
        assert data == {
            "metrics": [{"metric": "MockMetric", "result": {"value": 1}}],
            "timestamp": None,
            "version": evidently.__version__,
        }
    if report_format == "html":
        pass  # how should we validate it? not 500 seems good enough


def test_get_project_panels(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/dashboard/panels"""
    panel = DashboardPanelCounter(
        title="panel",
        filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
        agg=CounterAgg.NONE,
    )
    mock_project.dashboard.add_panel(panel)
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    r = test_client.get(f"/api/projects/{project.id}/dashboard/panels")
    r.raise_for_status()
    data = r.json()
    assert parse_obj_as(List[DashboardPanel], data) == [panel]


def test_get_project_dashboard(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/dashboard"""
    panel = DashboardPanelCounter(
        title="panel",
        filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
        agg=CounterAgg.NONE,
    )
    mock_project.dashboard.add_panel(panel)
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)

    r = test_client.get(f"/api/projects/{project.id}/dashboard")
    r.raise_for_status()
    data = r.json()
    assert data == {
        "max_timestamp": None,
        "min_timestamp": None,
        "name": "",
        "widgets": [
            {
                "additionalGraphs": [],
                "alertStats": None,
                "alerts": [],
                "alertsPosition": None,
                "details": "",
                "id": str(panel.id),
                "insights": [],
                "pageSize": 5,
                "params": {"counters": [{"label": "panel", "value": ""}]},
                "size": 2,
                "tabs": [],
                "title": "",
                "type": "counter",
                "widgets": [],
                "source_fingerprint": None,
            }
        ],
    }


def test_reload_project(test_client: TestClient, project_manager: ProjectManager, mock_project, mock_snapshot):
    """get /api/projects/{project_id}/reload"""
    project = project_manager.add_project(mock_project, ZERO_UUID, ZERO_UUID)
    mock_snapshot.metrics_ids = [0]
    project_manager.add_snapshot(ZERO_UUID, project.id, mock_snapshot)
    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1

    blob = project_manager.blob
    assert isinstance(blob, FSSpecBlobStorage)
    snapshot_path = os.path.join(blob.base_path, blob.get_snapshot_blob_id(project.id, mock_snapshot))
    snapshot_id2 = uuid.uuid4()
    snapshot2 = deepcopy(mock_snapshot)
    snapshot2.id = snapshot_id2
    snapshot_path2 = snapshot_path.replace(str(mock_snapshot.id), str(snapshot_id2))
    with open(snapshot_path2, "w") as f:
        f.write(json.dumps(snapshot2.dict(), indent=2, cls=NumpyEncoder))

    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 1
    r = test_client.get(f"/api/projects/{project.id}/reload")
    r.raise_for_status()

    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 2


def test_api_version(test_client):
    """get /api/version"""
    response = test_client.get("/api/version")
    assert response.status_code == 200

    version_response = response.json()
    assert "version" in version_response
    assert version_response["application"] == "Evidently UI"
