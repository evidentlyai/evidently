import datetime

import pandas as pd
import pytest
import uuid6

from evidently.core.datasets import Dataset
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


@pytest.fixture
def mock_dataset():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    return Dataset.from_pandas(df, metadata={"test": "metadata"}, tags=["test_tag"])


def test_list_datasets(workspace: WorkspaceBase, mock_project: ProjectModel, mock_dataset: Dataset):
    project = workspace.add_project(mock_project)

    assert len(workspace.list_datasets(project.id).datasets) == 0

    dataset_id = workspace.add_dataset(project.id, mock_dataset, "test_dataset", "Test description")

    datasets = workspace.list_datasets(project.id)
    assert len(datasets.datasets) == 1
    assert datasets.datasets[0].id == dataset_id
    assert datasets.datasets[0].name == "test_dataset"
    assert datasets.datasets[0].description == "Test description"
    assert datasets.datasets[0].row_count == 3
    assert datasets.datasets[0].column_count == 2
    assert datasets.datasets[0].origin == "file"
    assert "test_tag" in datasets.datasets[0].tags
    assert datasets.datasets[0].metadata["test"] == "metadata"


def test_list_datasets_filter_by_origin(workspace: WorkspaceBase, mock_project: ProjectModel, mock_dataset: Dataset):
    project = workspace.add_project(mock_project)

    dataset_id = workspace.add_dataset(project.id, mock_dataset, "test_dataset", "Test description")

    datasets = workspace.list_datasets(project.id, origins=["file"])
    assert len(datasets.datasets) == 1
    assert datasets.datasets[0].id == dataset_id

    datasets = workspace.list_datasets(project.id, origins=["tracing"])
    assert len(datasets.datasets) == 0


def test_load_dataset(workspace: WorkspaceBase, mock_project: ProjectModel, mock_dataset: Dataset):
    project = workspace.add_project(mock_project)

    dataset_id = workspace.add_dataset(project.id, mock_dataset, "test_dataset", "Test description")

    loaded_dataset = workspace.load_dataset(dataset_id)

    pd.testing.assert_frame_equal(loaded_dataset.as_dataframe(), mock_dataset.as_dataframe())
    assert loaded_dataset.data_definition == mock_dataset.data_definition
    assert loaded_dataset.metadata == mock_dataset.metadata
    assert loaded_dataset.tags == mock_dataset.tags
