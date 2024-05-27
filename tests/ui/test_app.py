import datetime
import json
import uuid
from copy import deepcopy
from typing import List

import pytest
from litestar.testing import TestClient

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import Options
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.suite.base_suite import ContextPayload
from evidently.suite.base_suite import Snapshot
from evidently.ui.base import ProjectManager
from evidently.ui.type_aliases import ZERO_UUID
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
    value: str

    @classmethod
    def create(cls, value: str):
        return MockMetricResult(value=value)


class MockMetric(Metric[MockMetricResult]):
    def calculate(self, data: InputData) -> MockMetricResult:
        return MockMetricResult.create("")


@default_renderer(wrap_type=MockMetric)
class MockMetricRenderer(MetricRenderer):
    def render_html(self, obj) -> List[BaseWidgetInfo]:
        return [counter(counters=[CounterData("title", "text")], size=self.size)]


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
            metric_results=[MockMetricResult.create("value")],
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
    r = test_client.delete(f"/api/projects/{project.id}/{mock_snapshot.id}")
    r.raise_for_status()

    assert len(project_manager.list_snapshots(ZERO_UUID, project.id)) == 0


def test_get_project_reports(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/reports"""


def test_get_project_test_suites(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/test_suites"""


def test_get_projects_graphs_data(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}"""


def test_get_snapshot_data(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/{snapshot_id}/data"""


def test_download_snapshot(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/{snapshot_id}/download"""


def test_get_project_panels(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/dashboard/panels"""


def test_get_project_dashboard(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/dashboard"""


def test_reload_project(test_client: TestClient, project_manager: ProjectManager, mock_project):
    """get /api/projects/{project_id}/reload"""


def test_api_version(test_client):
    """get /api/version"""
    response = test_client.get("/api/version")
    assert response.status_code == 200

    version_response = response.json()
    assert "version" in version_response
    assert version_response["application"] == "Evidently UI"
