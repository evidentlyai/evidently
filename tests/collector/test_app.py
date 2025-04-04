import asyncio
import os.path
import sys

import pandas as pd
import pytest
from litestar.testing import TestClient

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.collector.app import check_snapshots_factory
from evidently.legacy.collector.config import CollectorConfig
from evidently.legacy.collector.config import CollectorServiceConfig
from evidently.legacy.ui.storage.common import NoopAuthManager
from evidently.legacy.ui.storage.local import create_local_project_manager
from evidently.legacy.ui.workspace.view import WorkspaceView
from tests.ui.conftest import HEADERS
from tests.ui.conftest import _dumps


@pytest.mark.asyncio
@pytest.mark.skipif(sys.version_info < (3, 10), reason="loop not available on python < 3.10")
async def test_create_collector(
    collector_test_client: TestClient, collector_service_config: CollectorServiceConfig, mock_collector_config
):
    r = collector_test_client.post("/new", content=_dumps(mock_collector_config), headers=HEADERS)
    r.raise_for_status()

    assert "new" in collector_service_config.collectors
    mock_collector_config.id = "new"
    assert collector_service_config.collectors["new"] == mock_collector_config


def test_get_collector(
    collector_test_client: TestClient, collector_service_config: CollectorServiceConfig, mock_collector_config
):
    mock_collector_config.id = "new"
    collector_service_config.collectors["new"] = mock_collector_config

    r = collector_test_client.get("/new")
    r.raise_for_status()

    assert parse_obj_as(CollectorConfig, r.json()) == mock_collector_config


def test_set_reference(
    collector_test_client: TestClient,
    collector_service_config: CollectorServiceConfig,
    mock_collector_config,
    mock_reference,
    collector_workspace: str,
):
    mock_collector_config.id = "new"
    collector_service_config.collectors["new"] = mock_collector_config

    r = collector_test_client.post("/new/reference", json=mock_reference.to_dict())
    r.raise_for_status()

    assert mock_collector_config.reference_path == "new_reference.parquet"
    path = os.path.join(collector_workspace, mock_collector_config.reference_path)
    assert os.path.exists(path)
    saved_reference = pd.read_parquet(path)
    pd.testing.assert_frame_equal(saved_reference, mock_reference)


def test_push_data(
    collector_test_client: TestClient,
    collector_service_config: CollectorServiceConfig,
    mock_collector_config,
    mock_reference,
):
    mock_collector_config.id = "new"
    collector_service_config.collectors["new"] = mock_collector_config
    mock_collector_config._reference = mock_reference
    mock_collector_config.reference_path = ""
    mock_collector_config.trigger.rows_count = 2
    collector_service_config.storage.init("new")

    r = collector_test_client.post("/new/data", json=mock_reference.to_dict())
    r.raise_for_status()

    assert collector_service_config.storage.get_buffer_size("new") == 1


@pytest.fixture()
def ui_workspace(tmp_path) -> WorkspaceView:
    project_manager = create_local_project_manager(str(tmp_path / "ui_ws"), False, NoopAuthManager())
    return WorkspaceView(None, project_manager)


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="infinite loop")
async def test_create_snapshot_and_get_logs(
    collector_test_client: TestClient,
    collector_service_config: CollectorServiceConfig,
    mock_collector_config,
    mock_reference,
    ui_workspace: WorkspaceView,
):
    mock_collector_config.id = "new"
    collector_service_config.collectors["new"] = mock_collector_config
    mock_collector_config._reference = mock_reference
    mock_collector_config.reference_path = ""
    collector_service_config.storage.init("new")

    mock_collector_config._workspace = ui_workspace
    project = ui_workspace.create_project("proj")
    mock_collector_config.project_id = str(project.id)

    r = collector_test_client.post("/new/data", json=mock_reference.to_dict())
    r.raise_for_status()

    assert len(project.list_snapshots()) == 0
    asyncio.get_event_loop().run_until_complete(
        check_snapshots_factory(collector_service_config, collector_service_config.storage)
    )
    assert len(project.list_snapshots()) == 1

    snapshot_id = str(project.list_snapshots()[0].id)

    r = collector_test_client.get("/new/logs")
    r.raise_for_status()

    data = r.json()
    assert data == [
        {"error": "", "ok": True, "report_id": snapshot_id, "type": "UploadReport"},
        {"error": "", "ok": True, "report_id": snapshot_id, "type": "CreateReport"},
    ]
