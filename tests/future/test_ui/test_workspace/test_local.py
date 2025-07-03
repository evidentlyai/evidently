import datetime

import pytest
import uuid6

from evidently.core.report import Report
from evidently.core.report import Snapshot
from evidently.legacy.core import new_id
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import DashboardPanelPlot
from evidently.sdk.models import ProjectModel
from evidently.ui.workspace import Workspace
from evidently.ui.workspace import WorkspaceBase


@pytest.fixture
def workspace(tmpdir):
    return Workspace(str(tmpdir))


@pytest.fixture
def mock_project():
    return ProjectModel(
        id=uuid6.UUID(int=1, version=7),
        name="mock project",
    )


@pytest.fixture
def mock_snapshot():
    report = Report(metrics=[])
    snapshot = Snapshot(report, "mock", datetime.datetime.now(), metadata={}, tags=[])
    snapshot._widgets = []
    return snapshot


@pytest.fixture
def mock_dashboard():
    return DashboardModel(
        tabs=[],
        panels=[
            DashboardPanelPlot(id=new_id(), title="mock panel", subtitle=None, size="full", values=[], plot_params={})
        ],
    )


def test_add_get_project(workspace: WorkspaceBase, mock_project: ProjectModel):
    workspace.add_project(mock_project)
    assert workspace.get_project(mock_project.id)._project == mock_project


def test_list_project(workspace: WorkspaceBase, mock_project: ProjectModel):
    assert len(workspace.list_projects()) == 0
    workspace.add_project(mock_project)
    assert len(workspace.list_projects()) == 1


def test_delete_project(workspace: WorkspaceBase, mock_project: ProjectModel):
    assert len(workspace.list_projects()) == 0
    workspace.add_project(mock_project)
    assert len(workspace.list_projects()) == 1
    workspace.delete_project(mock_project.id)
    assert len(workspace.list_projects()) == 0


def test_add_snapshot(workspace: WorkspaceBase, mock_project: ProjectModel, mock_snapshot):
    project = workspace.add_project(mock_project)
    workspace.add_run(project.id, mock_snapshot)
    # todo


def test_list_snapshot(workspace: WorkspaceBase, mock_project: ProjectModel, mock_snapshot):
    project = workspace.add_project(mock_project)
    assert len(workspace.list_runs(project.id)) == 0
    workspace.add_run(project.id, mock_snapshot)
    assert len(workspace.list_runs(project.id)) == 1


def test_delete_snapshot(workspace: WorkspaceBase, mock_project: ProjectModel, mock_snapshot):
    project = workspace.add_project(mock_project)
    assert len(workspace.list_runs(project.id)) == 0
    run = workspace.add_run(project.id, mock_snapshot)
    assert len(workspace.list_runs(project.id)) == 1
    workspace.delete_run(project.id, run.id)
    assert len(workspace.list_runs(project.id)) == 0


def test_add_get_dashboard(workspace: WorkspaceBase, mock_project: ProjectModel, mock_dashboard):
    project = workspace.add_project(mock_project)
    workspace.save_dashboard(project.id, mock_dashboard)
    assert workspace.get_dashboard(project.id) == mock_dashboard
