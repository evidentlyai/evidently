import abc
import os
import pathlib
import uuid
from abc import ABC
from abc import abstractmethod
from json import JSONDecodeError
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Type
from typing import Union
from typing import overload
from urllib.parse import urljoin

from requests import HTTPError
from requests import Response

from evidently._pydantic_compat import BaseModel
from evidently.core.datasets import Dataset
from evidently.core.report import Snapshot
from evidently.core.serialization import SnapshotModel
from evidently.errors import EvidentlyError
from evidently.legacy.core import new_id
from evidently.legacy.ui.api.models import OrgModel
from evidently.legacy.ui.api.service import EVIDENTLY_APPLICATION_NAME
from evidently.legacy.ui.base import Org
from evidently.legacy.ui.storage.common import SECRET_HEADER_NAME
from evidently.legacy.ui.type_aliases import STR_UUID
from evidently.legacy.ui.type_aliases import DatasetID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.workspace.cloud import ACCESS_TOKEN_COOKIE
from evidently.legacy.ui.workspace.cloud import TOKEN_HEADER_NAME
from evidently.legacy.ui.workspace.remote import RemoteBase
from evidently.legacy.ui.workspace.remote import T
from evidently.legacy.utils.sync import async_to_sync
from evidently.sdk.datasets import DatasetList
from evidently.sdk.datasets import RemoteDatasetsManager
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import DashboardPanelPlot
from evidently.sdk.models import DashboardTabModel
from evidently.sdk.models import ProjectModel
from evidently.sdk.models import SnapshotLink
from evidently.ui.service.datasets.metadata import DatasetOrigin
from evidently.ui.service.storage.common import NoopAuthManager
from evidently.ui.service.storage.local import FSSpecBlobStorage
from evidently.ui.service.storage.local import create_local_project_manager
from evidently.ui.service.type_aliases import ZERO_UUID
from evidently.ui.storage.local.base import SNAPSHOTS_DIR_NAME
from evidently.ui.storage.local.base import LocalState
from evidently.ui.utils import get_file_link_to_report
from evidently.ui.utils import get_html_link_to_report


class ProjectDashboard:
    """Dashboard interface for configuring project visualizations.

    `ProjectDashboard` provides methods to manage dashboard tabs and panels
    for a project. Use it to customize which metrics are displayed and how
    they are organized.

    Access via `Project.dashboard` property.
    """

    @property
    @abc.abstractmethod
    def project_id(self) -> ProjectID:
        """Get the project ID this dashboard belongs to.

        Returns:
        * `ProjectID` of the associated project
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_tab(self, tab: str):
        """Add a new tab to the dashboard.

        Args:
        * `tab`: Name of the tab to add
        """
        raise NotImplementedError

    @abstractmethod
    def delete_tab(self, tab: str):
        """Delete a tab from the dashboard.

        Args:
        * `tab`: Name of the tab to delete
        """
        raise NotImplementedError

    @abstractmethod
    def add_panel(self, panel: DashboardPanelPlot, tab: Optional[str] = None, create_if_not_exists: bool = True):
        """Add a panel to a dashboard tab.

        Args:
        * `panel`: `DashboardPanelPlot` to add
        * `tab`: Optional tab name (creates tab if it doesn't exist and `create_if_not_exists=True`)
        * `create_if_not_exists`: If True, create the tab if it doesn't exist
        """
        raise NotImplementedError

    @abstractmethod
    def delete_panel(self, panel: str, tab: str):
        """Delete a panel from a dashboard tab.

        Args:
        * `panel`: ID of the panel to delete
        * `tab`: Name of the tab containing the panel
        """
        raise NotImplementedError

    @abstractmethod
    def model(self) -> DashboardModel:
        """Get the dashboard model configuration.

        Returns:
        * `DashboardModel` with current dashboard configuration
        """
        raise NotImplementedError

    def __repr__(self):
        _model = self.model()
        return f"Dashboard for project {self.project_id}\n  " + "\n  ".join(
            f"Tab '{tab.title}' ({tab.id})\n    "
            + "\n    ".join(
                f"Panel '{p.title}' ({p.id})\n      "
                + "\n      ".join(
                    f"Series metric_type={s.metric}"
                    + f" (tags={s.tags},metadata={s.metadata})"
                    + f" labels={s.metric_labels}"
                    for s in p.values
                )
                for p in _model.panels
                if p.id in tab.panels
            )
            for tab in _model.tabs
        )


class Project:
    """Represents an Evidently project for organizing evaluations.

    A `Project` groups related evaluations (snapshots) together. You can manage
    project metadata, configure dashboards, and access all runs associated
    with the project.

    Example:
    ```python
    workspace = Workspace.create("my_workspace")
    project = workspace.add_project(ProjectModel(name="My Project"))
    project.name = "Updated Name"
    project.save()
    ```

    Access projects via `Workspace.get_project()` or `Workspace.list_projects()`.
    """

    _project: ProjectModel
    _dashboard: ProjectDashboard
    _workspace: "WorkspaceBase"

    def __init__(
        self,
        project: ProjectModel,
        dashboard: ProjectDashboard,
        workspace: "WorkspaceBase",
    ):
        """Initialize a Project instance.

        Args:
        * `project`: `ProjectModel` with project data
        * `dashboard`: `ProjectDashboard` for managing visualizations
        * `workspace`: `WorkspaceBase` for persistence operations
        """
        self._project = project
        self._workspace = workspace
        self._dashboard = dashboard

    @property
    def id(self) -> ProjectID:
        """Get the project ID.

        Returns:
        * `ProjectID` unique identifier for this project
        """
        return self._project.id

    @property
    def name(self) -> str:
        """Get the project name.

        Returns:
        * Project name string
        """
        return self._project.name

    @name.setter
    def name(self, value: str):
        """Set the project name.

        Args:
        * `value`: New project name

        Note: Call `save()` to persist changes.
        """
        self._project.name = value

    @property
    def description(self) -> Optional[str]:
        """Get the project description.

        Returns:
        * Project description string, or None if not set
        """
        return self._project.description

    @description.setter
    def description(self, value: str):
        """Set the project description.

        Args:
        * `value`: New project description

        Note: Call `save()` to persist changes.
        """
        self._project.description = value

    def save(self):
        """Save project changes to the workspace.

        Persists any modifications to project name, description, or other
        metadata to the underlying `Workspace`.
        """
        self._workspace.update_project(self._project)

    @property
    def dashboard(self) -> ProjectDashboard:
        """Get the dashboard interface for this project.

        Returns:
        * `ProjectDashboard` for configuring visualizations
        """
        return self._dashboard

    def __repr__(self):
        return f"""Project ID: {self.id}
Project Name: {self.name}
Project Description: {self.description}
        """

    def dict(self):
        """Get the project as a dictionary.

        Returns a dictionary representation suitable for serialization (JSON/YAML).

        Returns:
        * Dictionary representation of the project model.
        """
        return self._project.dict()

    @property
    def version(self):
        return self._project.version


class _RemoteProjectDashboard(ProjectDashboard):
    _project_id: ProjectID
    _workspace: "WorkspaceBase"

    def __init__(self, project_id: ProjectID, workspace: "WorkspaceBase"):
        self._project_id = project_id
        self._workspace = workspace

    @property
    def project_id(self) -> ProjectID:
        return self._project_id

    def add_tab(self, tab: str):
        """Add a new tab to the dashboard.

        Args:
        * `tab`: Name of the tab to add.

        Raises:
        * `EvidentlyError`: If a tab with the same name already exists.
        """
        _dashboard_model = self.model()
        if any([t.title == tab for t in _dashboard_model.tabs]):
            raise EvidentlyError(f"Tab {tab} already exists in project {self._project_id} dashboard")
        _dashboard_model.tabs.append(DashboardTabModel(title=tab, panels=[]))
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def delete_tab(self, tab: str):
        """Delete a tab from the dashboard.

        Args:
        * `tab`: Name of the tab to delete.
        """
        _dashboard_model = self.model()
        new_tabs = [t for t in _dashboard_model.tabs if t.title != tab]
        _dashboard_model.tabs = new_tabs
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def add_panel(self, panel: DashboardPanelPlot, tab: Optional[str] = None, create_if_not_exists: bool = True):
        """Add a panel to the dashboard.

        Args:
        * `panel`: `DashboardPanelPlot` to add.
        * `tab`: Optional tab name to add the panel to. If `None`, adds to the first tab (or creates "General" tab if none exist).
        * `create_if_not_exists`: If `True`, creates the tab if it doesn't exist. If `False`, raises an error.

        Raises:
        * `EvidentlyError`: If `create_if_not_exists` is `False` and the tab doesn't exist.
        """
        _dashboard_model = self.model()
        _dashboard_model.panels.append(panel)
        _tab_id = None
        if tab is not None:
            for dashboard_tab in _dashboard_model.tabs:
                if dashboard_tab.title == tab:
                    dashboard_tab.panels.append(panel.id)
                    _tab_id = dashboard_tab.id
            if _tab_id is None and create_if_not_exists:
                new_tab_id = uuid.uuid4()
                _dashboard_model.tabs.append(DashboardTabModel(id=new_tab_id, title=tab, panels=[]))
                _tab_id = new_tab_id
            elif _tab_id is None and not create_if_not_exists:
                raise EvidentlyError(
                    f"Tab {tab} is missing in project {self._project_id} and create_if_not_exists is False"
                )
        else:
            if len(_dashboard_model.tabs) == 0:
                new_tab_id = uuid.uuid4()
                _dashboard_model.tabs.append(DashboardTabModel(id=new_tab_id, title="General", panels=[]))
            _tab_id = _dashboard_model.tabs[0].id

        assert _tab_id is not None
        for dashboard_tab in _dashboard_model.tabs:
            if dashboard_tab.id == _tab_id:
                dashboard_tab.panels.append(panel.id)
                break
        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def delete_panel(self, panel: str, tab: str):
        """Delete a panel from a tab.

        Args:
        * `panel`: Title of the panel to delete.
        * `tab`: Name of the tab containing the panel.

        Raises:
        * `EvidentlyError`: If the tab doesn't exist.
        """
        _dashboard_model = self.model()
        _tab = None
        for t in _dashboard_model.tabs:
            if t.title == tab:
                _tab = t

        if _tab is None:
            raise EvidentlyError(f"Tab {tab} does not exist in project {self._project_id} dashboard")

        new_panels = [p for p in _dashboard_model.panels if p.id in _tab.panels and p.title != panel]
        _tab.panels = [p.id for p in new_panels]
        _dashboard_model.panels = new_panels

        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def model(self):
        """Get the dashboard model.

        Returns:
        * `DashboardModel` with current dashboard configuration.
        """
        return self._workspace.get_dashboard(self.project_id)

    def clear_tab(self, tab: str):
        """Remove all panels from a tab.

        Args:
        * `tab`: Name of the tab to clear.

        Raises:
        * `EvidentlyError`: If the tab doesn't exist.
        """
        _dashboard_model = self.model()
        _tab = None
        for t in _dashboard_model.tabs:
            if t.title == tab:
                _tab = t

        if _tab is None:
            raise EvidentlyError(f"Tab {tab} does not exist in project {self._project_id} dashboard")

        new_panels = [p for p in _dashboard_model.panels if p not in _tab.panels]
        _dashboard_model.panels = new_panels
        _tab.panels = []

        self._workspace.save_dashboard(self.project_id, _dashboard_model)

    def clear_dashboard(self):
        """Remove all panels and tabs from the dashboard."""
        _dashboard_model = self.model()
        _dashboard_model.panels = []
        _dashboard_model.tabs = []
        self._workspace.save_dashboard(self.project_id, _dashboard_model)


class SnapshotRef(BaseModel):
    """Reference to a snapshot (run) with its URL and IDs.

    Returned by `WorkspaceBase.add_run()` to provide access to the uploaded snapshot.
    Contains the snapshot ID, project ID, and URL for viewing the snapshot.
    """

    id: SnapshotID
    """Snapshot ID."""
    project_id: ProjectID
    """Project ID this snapshot belongs to."""
    url: str
    """URL to view the snapshot."""

    def __repr__(self):
        return f"Report ID: {self.id}\nLink: {self.url}"

    def _repr_html_(self):
        if self.url.startswith("http:") or self.url.startswith("https:"):
            return get_html_link_to_report(url_to_report=self.url, report_id=self.id)
        if pathlib.Path(self.url).is_absolute():
            return get_file_link_to_report(url_to_report=self.url, report_id=self.id)
        else:
            return get_html_link_to_report(url_to_report=self.url, report_id=self.id)


class WorkspaceBase(ABC):
    """Base class for workspace implementations.

    Provides the interface for managing Evidently projects, runs (snapshots),
    datasets, and dashboards. Implemented by `Workspace`, `RemoteWorkspace`, and `CloudWorkspace`.
    """

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        org_id: Optional[OrgID] = None,
    ) -> Project:
        """Create a new project with the given name and description.

        Convenience method that creates a `ProjectModel` and calls `add_project()`.

        Args:
        * `name`: Name of the project to create.
        * `description`: Optional description for the project.
        * `org_id`: Optional organization ID.

        Returns:
        * `Project`: The newly created project.
        """
        project = self.add_project(
            ProjectModel(
                name=name,
                description=description,
                org_id=org_id,
            ),
            org_id,
        )
        return project

    @abstractmethod
    def add_project(self, project: ProjectModel, org_id: Optional[OrgID] = None) -> Project:
        """Add a new project to the workspace.

        Args:
        * `project`: `ProjectModel` with project data.
        * `org_id`: Optional organization ID.

        Returns:
        * `Project`: The newly created project.
        """
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        """Get a project by ID.

        Args:
        * `project_id`: UUID of the project to retrieve.

        Returns:
        * `Project` if found, `None` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: STR_UUID):
        """Delete a project from the workspace.

        Args:
        * `project_id`: UUID of the project to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def list_projects(self, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """List all projects in the workspace.

        Args:
        * `org_id`: Optional organization ID to filter by.

        Returns:
        * Sequence of `Project` objects.
        """
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project: ProjectModel):
        """Update an existing project.

        Args:
        * `project`: `ProjectModel` with updated data.
        """
        raise NotImplementedError

    @abstractmethod
    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot) -> SnapshotID:
        """Internal method to add a snapshot to a project.

        Args:
        * `project_id`: UUID of the project.
        * `snapshot`: `Snapshot` to add.

        Returns:
        * `SnapshotID` of the added snapshot.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_snapshot_url(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> str:
        """Get the URL for viewing a snapshot.

        Args:
        * `project_id`: UUID of the project.
        * `snapshot_id`: UUID of the snapshot.

        Returns:
        * URL string for viewing the snapshot.
        """
        raise NotImplementedError

    def add_run(
        self,
        project_id: STR_UUID,
        run: Snapshot,
        include_data: bool = False,
        name: Optional[str] = None,
    ) -> SnapshotRef:
        """Add a snapshot (run) to a project.

        Uploads a `Snapshot` to the specified project. Optionally includes
        the input datasets if `include_data=True`.

        Args:
        * `project_id`: UUID of the project to add the run to.
        * `run`: `Snapshot` object to upload.
        * `include_data`: If `True`, uploads input datasets to the server (if supported).
        * `name`: Optional name for the run (overrides snapshot name if provided).

        Returns:
        * `SnapshotRef`: Reference object with snapshot ID, project ID, and URL.
        """
        if name is not None:
            run.set_name(name)
        snapshot_id = self._add_run(project_id, run)
        current_dataset_name = run.get_name() or f"run-current-{snapshot_id}"
        reference_dataset_name = f"{run.get_name()}: reference" if run.get_name() else f"run-reference-{snapshot_id}"
        if include_data:
            current, reference = run.context._input_data
            self.add_dataset(
                project_id,
                current,
                current_dataset_name,
                None,
                link=SnapshotLink(snapshot_id=snapshot_id, dataset_type="output", dataset_subtype="current"),
            )
            if reference is not None:
                self.add_dataset(
                    project_id,
                    reference,
                    reference_dataset_name,
                    None,
                    link=SnapshotLink(snapshot_id=snapshot_id, dataset_type="output", dataset_subtype="reference"),
                )

            base_name = run.get_name() or f"run-{snapshot_id}"
            for key, dataset in run.context.additional_data.items():
                dataset_name = f"{base_name}_{key}"
                dataset_description = f"Additional dataset: {key}"
                self.add_dataset(
                    project_id=project_id,
                    dataset=dataset,
                    name=dataset_name,
                    description=dataset_description,
                    link=SnapshotLink(snapshot_id=snapshot_id, dataset_type="output", dataset_subtype="additional"),
                )
        return SnapshotRef(id=snapshot_id, project_id=project_id, url=self._get_snapshot_url(project_id, snapshot_id))

    @abstractmethod
    def delete_run(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        """Delete a snapshot (run) from a project.

        Args:
        * `project_id`: UUID of the project.
        * `snapshot_id`: UUID of the snapshot to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def get_run(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> Optional[SnapshotModel]:
        """Get a snapshot (run) by ID.

        Args:
        * `project_id`: UUID of the project.
        * `snapshot_id`: UUID of the snapshot to retrieve.

        Returns:
        * `SnapshotModel` if found, `None` otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def list_runs(self, project_id: STR_UUID) -> Sequence[SnapshotID]:
        """List all snapshots (runs) for a project.

        Args:
        * `project_id`: UUID of the project.

        Returns:
        * Sequence of `SnapshotID` objects.
        """
        raise NotImplementedError

    @abstractmethod
    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """Search for projects by name.

        Args:
        * `project_name`: Name or partial name to search for.
        * `org_id`: Optional organization ID to filter by.

        Returns:
        * Sequence of matching `Project` objects.
        """
        raise NotImplementedError

    @abstractmethod
    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str] = None,
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        """Add a dataset to a project.

        Args:
        * `project_id`: UUID of the project.
        * `dataset`: `Dataset` object to add.
        * `name`: Name for the dataset.
        * `description`: Optional description for the dataset.
        * `link`: Optional `SnapshotLink` to associate dataset with a snapshot.

        Returns:
        * `DatasetID` of the added dataset.
        """
        raise NotImplementedError

    def load_dataset(self, dataset_id: DatasetID) -> Dataset:
        """Load a dataset by ID.

        Args:
        * `dataset_id`: UUID of the dataset to load.

        Returns:
        * `Dataset` object.
        """
        raise NotImplementedError

    def list_datasets(self, project: STR_UUID, origins: Optional[List[str]] = None) -> DatasetList:
        """List all datasets in a project.

        Args:
        * `project`: UUID of the project.
        * `origins`: Optional list of origin types to filter by.

        Returns:
        * `DatasetList` containing dataset information.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        """Save dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project.
        * `dashboard`: `DashboardModel` with dashboard configuration.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        """Get dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project.

        Returns:
        * `DashboardModel` with current dashboard configuration.
        """
        raise NotImplementedError


class Workspace(WorkspaceBase):
    """Local file system workspace for storing projects, snapshots, and datasets.

    `Workspace` provides a local file-based storage backend for Evidently projects.
    All data is stored in the specified directory on the local file system.

    Example:
    ```python
    workspace = Workspace.create("my_workspace")
    project = workspace.add_project(ProjectModel(name="My Project"))
    workspace.add_run(project.id, snapshot)
    ```
    """

    def __init__(self, path: str):
        """Initialize a local workspace.

        Args:
        * `path`: Directory path where the workspace data will be stored
        """
        self.path = path
        self.state = LocalState(self.path)
        from evidently.ui.service.datasets.metadata import FileDatasetMetadataStorage
        from evidently.ui.service.managers.datasets import DatasetManager
        from evidently.ui.service.storage.local.dataset import DatasetFileStorage
        from evidently.ui.service.tracing.storage.file import FileTracingStorage

        self.datasets = DatasetManager(
            project_manager=create_local_project_manager(path, False, NoopAuthManager()),
            dataset_metadata=FileDatasetMetadataStorage(base_path=self.path),
            dataset_file_storage=DatasetFileStorage(dataset_blob_storage=FSSpecBlobStorage(path)),
            tracing_storage=FileTracingStorage(path),
        )
        from evidently.ui.service.storage.local.snapshot_links import FileSnapshotDatasetLinksManager

        self.dataset_links = FileSnapshotDatasetLinksManager(path)

        # Add local SDK APIs for artifacts, prompts, and configs
        from evidently.sdk.artifacts import ArtifactAPI
        from evidently.sdk.configs import ConfigAPI
        from evidently.sdk.local import LocalArtifactAPI
        from evidently.sdk.local import LocalConfigAPI
        from evidently.sdk.local import LocalPromptAPI
        from evidently.sdk.prompts import PromptAPI
        from evidently.ui.service.storage.local.artifacts import FileArtifactStorage

        artifact_storage = FileArtifactStorage(base_path=self.path)
        self.artifacts: ArtifactAPI = LocalArtifactAPI(artifact_storage)
        self.prompts: PromptAPI = LocalPromptAPI(artifact_storage)
        self.configs: ConfigAPI = LocalConfigAPI(artifact_storage)

    def add_project(self, project: ProjectModel, org_id: Optional[OrgID] = None) -> Project:
        """Add a new project to the workspace.

        Args:
        * `project`: `ProjectModel` with project configuration
        * `org_id`: Optional organization ID (not used for local workspace)

        Returns:
        * `Project` object for the newly created project
        """
        project_model = self.state.write_project(project)
        dashboard = _RemoteProjectDashboard(project.id, self)
        return Project(project_model, dashboard, self)

    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        """Get a project by ID.

        Args:
        * `project_id`: UUID of the project to retrieve

        Returns:
        * `Project` object if found, None otherwise
        """
        try:
            project_model = self.state.read_project(project_id)
        except FileNotFoundError:
            return None
        return Project(project_model, _RemoteProjectDashboard(project_model.id, self), self)

    def delete_project(self, project_id: STR_UUID):
        """Delete a project from the workspace.

        Args:
        * `project_id`: UUID of the project to delete
        """
        self.state.delete_project(project_id)

    def list_projects(self, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """List all projects in the workspace.

        Args:
        * `org_id`: Optional organization ID (not used for local workspace)

        Returns:
        * Sequence of `Project` objects
        """
        return [self.get_project(project_id) for project_id in self.state.list_projects()]

    def update_project(self, project: ProjectModel):
        """Update an existing project.

        Args:
        * `project`: `ProjectModel` with updated project configuration
        """
        self.state.write_project(project)

    def _get_snapshot_url(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> str:
        return os.path.join(self.path, str(project_id), SNAPSHOTS_DIR_NAME, str(snapshot_id) + ".json")

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot) -> SnapshotID:
        snapshot_id = new_id()
        self.state.write_snapshot(project_id, snapshot_id, snapshot.to_snapshot_model())
        return snapshot_id

    def get_run(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> Optional[SnapshotModel]:
        """Get a snapshot (run) by ID.

        Args:
        * `project_id`: UUID of the project containing the snapshot
        * `snapshot_id`: UUID of the snapshot to retrieve

        Returns:
        * `SnapshotModel` if found, None otherwise
        """
        return self.state.read_snapshot(project_id, snapshot_id)

    def list_runs(self, project_id: STR_UUID) -> Sequence[SnapshotID]:
        """List all snapshots (runs) for a project.

        Args:
        * `project_id`: UUID of the project

        Returns:
        * Sequence of snapshot IDs
        """
        return self.state.list_snapshots(project_id)

    def delete_run(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        """Delete a snapshot (run) from a project.

        Args:
        * `project_id`: UUID of the project containing the snapshot
        * `snapshot_id`: UUID of the snapshot to delete
        """
        self.state.delete_snapshot(project_id, snapshot_id)

    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """Search for projects by name.

        Args:
        * `project_name`: Name to search for (exact match)
        * `org_id`: Optional organization ID (not used for local workspace)

        Returns:
        * Sequence of `Project` objects matching the name
        """
        return [p for p in self.list_projects(org_id) if p.name == project_name]

    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str] = None,
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        metadata = self.datasets.project_manager.project_metadata
        from evidently.ui.service.storage.local import JsonFileProjectMetadataStorage

        project_uuid: ProjectID = uuid.UUID(str(project_id))
        assert isinstance(metadata, JsonFileProjectMetadataStorage)
        if project_uuid not in metadata.state.projects:
            metadata.state.reload(force=True)

        dataset_metadata = async_to_sync(
            self.datasets.upload_dataset(
                ZERO_UUID,
                project_id=project_uuid,
                name=name,
                description=description,
                data=dataset.as_dataframe(),
                data_definition=dataset.data_definition,
                origin=DatasetOrigin.file,
                metadata=dataset.metadata,
                tags=dataset.tags,
            )
        )
        if link is not None:
            async_to_sync(
                self.dataset_links.link_dataset_snapshot(
                    project_uuid, link.snapshot_id, dataset_metadata.id, link.dataset_type, link.dataset_subtype
                )
            )
        return dataset_metadata.id

    def list_datasets(self, project: STR_UUID, origins: Optional[List[str]] = None) -> DatasetList:
        from evidently.sdk.datasets import DatasetInfo

        project_uuid: ProjectID = uuid.UUID(str(project))
        origin_enums = None
        if origins:
            origin_enums = [DatasetOrigin(o) for o in origins]

        datasets_metadata = async_to_sync(
            self.datasets.list_datasets(
                user_id=ZERO_UUID,
                project_id=project_uuid,
                limit=None,
                origin=origin_enums,
                draft=None,
            )
        )

        dataset_infos = [
            DatasetInfo(
                id=d.id,
                project_id=d.project_id,
                name=d.name,
                size_bytes=d.size_bytes,
                row_count=d.row_count,
                column_count=d.column_count,
                description=d.description,
                created_at=d.created_at,
                author_name=d.author_name,
                origin=d.origin.value,
                tags=d.tags,
                metadata=d.metadata,
            )
            for d in datasets_metadata
        ]

        return DatasetList(datasets=dataset_infos)

    def load_dataset(self, dataset_id: DatasetID) -> Dataset:
        df, dataset_metadata = async_to_sync(
            self.datasets.get_dataset(
                user_id=ZERO_UUID,
                dataset_id=dataset_id,
                sort_by=None,
                filter_queries=None,
            )
        )

        return Dataset.from_pandas(
            df,
            data_definition=dataset_metadata.data_definition,
            metadata=dataset_metadata.metadata,
            tags=dataset_metadata.tags,
        )

    def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        """Save a dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project
        * `dashboard`: `DashboardModel` with dashboard configuration
        """
        self.state.write_dashboard(project_id, dashboard)

    def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        """Get the dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project

        Returns:
        * `DashboardModel` with dashboard configuration
        """
        return self.state.read_dashboard(project_id)

    @classmethod
    def create(cls, path: str = "workspace"):
        """Create a new workspace instance.

        Args:
        * `path`: Directory path where the workspace data will be stored (default: "workspace")

        Returns:
        * `Workspace` instance
        """
        return Workspace(path)


class RemoteWorkspace(RemoteBase, WorkspaceBase):  # todo: reuse cloud ws
    """Remote workspace for connecting to an Evidently API server.

    `RemoteWorkspace` provides a client interface to connect to a remote Evidently
    API server. This allows you to store and manage projects, snapshots, and datasets
    on a remote server instead of locally.

    Example:
    ```python
    workspace = RemoteWorkspace("http://localhost:8000", secret="my-secret")
    project = workspace.add_project(ProjectModel(name="My Project"))
    workspace.add_run(project.id, snapshot)
    ```
    """

    def get_url(self):
        """Get the base URL of the remote workspace.

        Returns:
        * Base URL string of the remote API server
        """
        return self.base_url

    def verify(self):
        """Verify that the remote server is running Evidently API.

        Raises:
        * ValueError if the server is not available or not running Evidently API
        """
        try:
            response = self._request("/api/version", "GET")
            assert response.json()["application"] == EVIDENTLY_APPLICATION_NAME
        except (HTTPError, JSONDecodeError, KeyError, AssertionError) as e:
            raise ValueError(f"Evidently API not available at {self.base_url}") from e

    def __init__(self, base_url: str, secret: Optional[str] = None, verify: bool = True):
        """Initialize a remote workspace connection.

        Args:
        * `base_url`: Base URL of the Evidently API server (e.g., "http://localhost:8000")
        * `secret`: Optional secret key for authentication
        * `verify`: If True, verify the server connection on initialization (default: True)
        """
        self.base_url = base_url
        self.secret = secret
        if verify:
            self.verify()
        self.datasets = RemoteDatasetsManager(self, "/api/datasets")
        # artifacts uses artifacts SDK and OSS artifacts API
        from evidently.sdk.adapters import ConfigArtifactAdapter
        from evidently.sdk.adapters import PromptArtifactAdapter
        from evidently.sdk.artifacts import ArtifactAPI
        from evidently.sdk.artifacts import RemoteArtifactAPI
        from evidently.sdk.configs import ConfigAPI
        from evidently.sdk.prompts import PromptAPI

        self.artifacts: ArtifactAPI = RemoteArtifactAPI(self)
        # prompts uses artifacts SDK via ArtifactPromptContent and OSS artifacts API
        self.prompts: PromptAPI = PromptArtifactAdapter(self)
        # configs uses artifacts SDK via OSS artifacts API
        self.configs: ConfigAPI = ConfigArtifactAdapter(self)

    def _prepare_request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ):
        r = super()._prepare_request(
            path=path,
            method=method,
            query_params=query_params,
            body=body,
            cookies=cookies,
            headers=headers,
            form_data=form_data,
        )
        if self.secret is not None:
            r.headers[SECRET_HEADER_NAME] = self.secret
        return r

    def add_project(self, project: ProjectModel, org_id: Optional[OrgID] = None) -> Project:
        """Add a new project to the remote workspace.

        Args:
        * `project`: `ProjectModel` with project configuration
        * `org_id`: Optional organization ID

        Returns:
        * `Project` object for the newly created project

        Raises:
        * `EvidentlyError` if project creation fails
        """
        params = {}
        if org_id:
            params["org_id"] = str(org_id)
        project_id = self._request(
            "/api/v2/projects", "POST", query_params=params, body=project.dict(), response_model=ProjectID
        )
        p = self.get_project(project_id)
        if p is None:
            raise EvidentlyError(
                f"Failed to receive updated information about project" f" after creation (project_id={project_id})"
            )
        return p

    def get_project(self, project_id: STR_UUID) -> Optional["Project"]:
        """Get a project by ID from the remote workspace.

        Args:
        * `project_id`: UUID of the project to retrieve

        Returns:
        * `Project` object if found, None otherwise
        """
        try:
            _project = self._request(f"/api/projects/{project_id}/info", "GET", response_model=ProjectModel)
            return Project(
                project=_project,
                dashboard=_RemoteProjectDashboard(_project.id, self),
                workspace=self,
            )
        except (HTTPError,) as e:
            try:
                data = e.response.json()  # type: ignore[attr-defined]
                if "detail" in data and data["detail"] == "project not found":
                    return None
                raise e
            except (ValueError, AttributeError):
                raise e

    def delete_project(self, project_id: STR_UUID):
        """Delete a project from the remote workspace.

        Args:
        * `project_id`: UUID of the project to delete
        """
        return self._request(f"/api/v2/projects/{project_id}", "DELETE")

    def list_projects(self, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """List all projects in the remote workspace.

        Args:
        * `org_id`: Optional organization ID

        Returns:
        * Sequence of `Project` objects
        """
        projects = self._request("/api/v2/projects", "GET", response_model=List[ProjectModel])
        return [Project(p, _RemoteProjectDashboard(p.id, self), self) for p in projects]

    def update_project(self, project: ProjectModel):
        """Update an existing project in the remote workspace.

        Args:
        * `project`: `ProjectModel` with updated project configuration
        """
        self._request(
            f"/api/v2/projects/{project.id}",
            method="PATCH",
            body=project.dict(),
        )

    def _get_snapshot_url(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> str:
        return urljoin(self.base_url, f"/projects/{project_id}/reports/{snapshot_id}")

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot):
        data = snapshot.dump_dict()
        resp: Response = self._request(f"/api/v2/snapshots/{project_id}", method="POST", body=data)
        return uuid.UUID(resp.json()["snapshot_id"])

    def delete_run(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        """Delete a snapshot (run) from a project.

        Args:
        * `project_id`: UUID of the project containing the snapshot
        * `snapshot_id`: UUID of the snapshot to delete

        Raises:
        * NotImplementedError (snapshot API not yet implemented)
        """
        raise NotImplementedError  # todo: snapshot api

    def get_run(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> Optional[SnapshotModel]:
        """Get a snapshot (run) by ID.

        Args:
        * `project_id`: UUID of the project containing the snapshot
        * `snapshot_id`: UUID of the snapshot to retrieve

        Returns:
        * `SnapshotModel` if found, None otherwise

        Raises:
        * NotImplementedError (snapshot API not yet implemented)
        """
        raise NotImplementedError  # todo: snapshot api

    def list_runs(self, project_id: STR_UUID) -> Sequence[SnapshotID]:
        """List all snapshots (runs) for a project.

        Args:
        * `project_id`: UUID of the project

        Returns:
        * Sequence of snapshot IDs

        Raises:
        * NotImplementedError (snapshot API not yet implemented)
        """
        raise NotImplementedError  # todo: snapshot api

    def search_project(self, project_name: str, org_id: Optional[OrgID] = None) -> Sequence[Project]:
        """Search for projects by name.

        Args:
        * `project_name`: Name to search for
        * `org_id`: Optional organization ID

        Returns:
        * Sequence of `Project` objects matching the name
        """
        projects = self._request(f"/api/projects/search/{project_name}", "GET", response_model=List[ProjectModel])
        return [Project(p, _RemoteProjectDashboard(p.id, self), self) for p in projects]

    def add_dataset(
        self,
        project_id: STR_UUID,
        dataset: Dataset,
        name: str,
        description: Optional[str] = None,
        link: Optional[SnapshotLink] = None,
    ) -> DatasetID:
        """Add a dataset to a project.

        Args:
        * `project_id`: UUID of the project to add the dataset to
        * `dataset`: `Dataset` object to store
        * `name`: Name for the dataset
        * `description`: Optional description of the dataset
        * `link`: Optional link to associate the dataset with a snapshot

        Returns:
        * UUID of the created dataset
        """
        return self.datasets.add(project_id=project_id, dataset=dataset, name=name, description=description, link=link)

    def load_dataset(self, dataset_id: DatasetID) -> Dataset:
        """Load a dataset by ID.

        Args:
        * `dataset_id`: UUID of the dataset to load

        Returns:
        * `Dataset` object loaded from storage
        """
        return self.datasets.load(dataset_id)

    def list_datasets(self, project: STR_UUID, origins: Optional[List[str]] = None) -> DatasetList:
        """List all datasets in a project.

        Args:
        * `project`: UUID of the project
        * `origins`: Optional list of origin types to filter by

        Returns:
        * `DatasetList` containing dataset information
        """
        return self.datasets.list(project, origins=origins)

    def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        """Save a dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project
        * `dashboard`: `DashboardModel` with dashboard configuration
        """
        self._request(f"/api/v2/dashboards/{project_id}", method="POST", body=dashboard.dict())

    def get_dashboard(self, project_id: ProjectID) -> DashboardModel:
        """Get the dashboard configuration for a project.

        Args:
        * `project_id`: UUID of the project

        Returns:
        * `DashboardModel` with dashboard configuration
        """
        data = self._request(f"/api/v2/dashboards/{project_id}", method="GET", response_model=DashboardModel)
        return data


class CloudWorkspace(RemoteWorkspace):
    """Cloud workspace for connecting to Evidently Cloud service.

    `CloudWorkspace` provides a client interface to connect to Evidently Cloud,
    the hosted Evidently service. Requires an API key for authentication.

    Example:
    ```python
    workspace = CloudWorkspace(token="sk_...")
    project = workspace.add_project(ProjectModel(name="My Project"))
    workspace.add_run(project.id, snapshot)
    ```
    """

    URL: str = "https://app.evidently.cloud"

    def __init__(
        self,
        token: Optional[str] = None,
        url: str = None,
    ):
        """Initialize a cloud workspace connection.

        Args:
        * `token`: API key token for authentication. If not provided, will try to read
          from `EVIDENTLY_API_KEY` environment variable
        * `url`: Optional custom cloud URL (defaults to "https://app.evidently.cloud")

        Raises:
        * ValueError if token is not provided and not found in environment
        """
        if token is None:
            token = os.environ.get("EVIDENTLY_API_KEY", default=None)
        if token is None:
            raise ValueError(
                "To use CloudWorkspace you must provide a token through argument or env variable EVIDENTLY_API_KEY"
            )
        self.token = token
        self.token_cookie_name = ACCESS_TOKEN_COOKIE.key
        self._api_key = None
        if token.startswith("sk_") and len(token.split(".")) >= 3:
            self._api_key = token
        self._jwt_token: Optional[str] = None
        self._logged_in: bool = False
        super().__init__(base_url=url if url is not None else self.URL)
        from evidently.sdk.adapters import ArtifactConfigAdapter
        from evidently.sdk.artifacts import ArtifactAPI
        from evidently.sdk.configs import CloudConfigAPI
        from evidently.sdk.configs import ConfigAPI
        from evidently.sdk.prompts import CloudPromptAPI
        from evidently.sdk.prompts import PromptAPI

        self.prompts: PromptAPI = CloudPromptAPI(self)
        self.datasets = RemoteDatasetsManager(self, "/api/v2/datasets")
        self.configs: ConfigAPI = CloudConfigAPI(self)
        # artifacts uses artifacts SDK interface but configs cloud API
        self.artifacts: ArtifactAPI = ArtifactConfigAdapter(self)

    def _get_jwt_token(self):
        return super()._request("/api/users/login", "GET", headers={TOKEN_HEADER_NAME: self.token}).text

    @property
    def jwt_token(self):
        if self._jwt_token is None:
            self._jwt_token = self._get_jwt_token()

        return self._jwt_token

    def _prepare_request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ):
        r = super()._prepare_request(
            path=path,
            method=method,
            query_params=query_params,
            body=body,
            cookies=cookies,
            headers=headers,
            form_data=form_data,
        )
        if path == "/api/users/login":
            return r
        if self._api_key is not None:
            r.headers["Authorization"] = f"Bearer {self._api_key}"
        else:
            r.cookies[self.token_cookie_name] = self.jwt_token
        return r

    @overload
    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Type[T] = ...,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> T:
        pass

    @overload
    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Literal[None] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> Response:
        pass

    def _request(
        self,
        path: str,
        method: str,
        query_params: Optional[dict] = None,
        body: Optional[dict] = None,
        response_model: Optional[Type[T]] = None,
        cookies=None,
        headers: Dict[str, str] = None,
        form_data: bool = False,
    ) -> Union[Response, T]:
        cookies = cookies or {}
        try:
            res = super()._request(
                path=path,
                method=method,
                query_params=query_params,
                body=body,
                response_model=response_model,
                cookies=cookies,
                headers=headers,
                form_data=form_data,
            )
            self._logged_in = True
            return res
        except HTTPError as e:
            if self._logged_in and e.response.status_code == 401:
                # renew token and retry
                self._jwt_token = self._get_jwt_token()
                cookies[self.token_cookie_name] = self.jwt_token
                return super()._request(
                    path,
                    method,
                    query_params,
                    body,
                    response_model,
                    cookies=cookies,
                    headers=headers,
                    form_data=form_data,
                )
            raise
        except EvidentlyError as e:
            if self._logged_in and e.get_message() == "EvidentlyError: Not authorized":
                # renew token and retry
                self._jwt_token = self._get_jwt_token()
                cookies[self.token_cookie_name] = self.jwt_token
                return super()._request(
                    path,
                    method,
                    query_params,
                    body,
                    response_model,
                    cookies=cookies,
                    headers=headers,
                    form_data=form_data,
                )
            raise

    def create_org(self, name: str) -> Org:
        """Create a new organization.

        Args:
        * `name`: Name of the organization.

        Returns:
        * `Org` object representing the created organization.
        """
        return self._request("/api/orgs", "POST", body=Org(name=name).dict(), response_model=OrgModel).to_org()

    def list_orgs(self) -> List[Org]:
        """List all organizations accessible to the current user.

        Returns:
        * List of `Org` objects.
        """
        return [o.to_org() for o in self._request("/api/orgs", "GET", response_model=List[OrgModel])]

    def _get_snapshot_url(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> str:
        return urljoin(self.base_url, f"/v2/projects/{project_id}/explore/{snapshot_id}")

    def _add_run(self, project_id: STR_UUID, snapshot: Snapshot) -> SnapshotID:
        data = snapshot.dump_dict()
        resp: Response = self._request(f"/api/v2/snapshots/{project_id}", method="POST", body=data)
        return uuid.UUID(resp.json()["snapshot_id"])
