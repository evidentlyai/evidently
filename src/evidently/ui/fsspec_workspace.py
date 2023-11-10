import datetime
import json
import posixpath
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from fsspec import AbstractFileSystem
from fsspec import get_fs_token_paths
from pydantic import ValidationError
from pydantic import parse_obj_as

from evidently.model.dashboard import DashboardInfo
from evidently.renderers.notebook_utils import determine_template
from evidently.report import Report
from evidently.suite.base_suite import ReportBase
from evidently.suite.base_suite import Snapshot
from evidently.test_suite import TestSuite
from evidently.ui.dashboards import DashboardConfig
from evidently.ui.workspace import METADATA_PATH
from evidently.ui.workspace import SNAPSHOTS
from evidently.ui.workspace import STR_UUID
from evidently.ui.workspace import Project
from evidently.ui.workspace import ProjectBase
from evidently.ui.workspace import ProjectSnapshot
from evidently.ui.workspace import WorkspaceBase
from evidently.utils import NumpyEncoder
from evidently.utils.dashboard import TemplateParams


class FSSpecProject(ProjectBase["FSSpecWorkspace"]):
    _snapshots: Dict[uuid.UUID, ProjectSnapshot] = {}

    @property
    def path(self):
        return posixpath.join(self.workspace.path, str(self.id))

    def add_snapshot(self, snapshot: Snapshot):
        item = ProjectSnapshot(snapshot.id, self, snapshot)
        with self.workspace.fs.open(item.path, "w") as f:
            json.dump(snapshot.dict(), f, indent=2, cls=NumpyEncoder)
        self._snapshots[item.id] = item

    def delete_snapshot(self, snapshot_id: Union[str, uuid.UUID]):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid.UUID(snapshot_id)
        if snapshot_id in self._snapshots:
            del self._snapshots[snapshot_id]
        path = posixpath.join(self.path, SNAPSHOTS, f"{snapshot_id}.json")
        if self.workspace.fs.exists(path):
            self.workspace.fs.delete(path)

    @classmethod
    def load(cls, fs: AbstractFileSystem, path: str) -> "FSSpecProject":
        try:
            with fs.open(posixpath.join(path, METADATA_PATH)) as f:
                return parse_obj_as(FSSpecProject, json.load(f))
        except FileNotFoundError:
            return FSSpecProject(name="Unnamed Project", dashboard=DashboardConfig(name="Dashboard", panels=[]))

    def save(self):
        self.workspace.fs.makedirs(posixpath.join(self.path, SNAPSHOTS), exist_ok=True)
        with self.workspace.fs.open(posixpath.join(self.path, METADATA_PATH), "w") as f:
            return json.dump(self.dict(), f, indent=2, cls=NumpyEncoder)

    def load_snapshot(self, snapshot_id: uuid.UUID) -> Snapshot:
        path = posixpath.join(self.path, SNAPSHOTS, str(snapshot_id) + ".json")

        with self.workspace.fs.open(path, "r") as f:
            return parse_obj_as(Snapshot, json.load(f))

    def reload(self, reload_snapshots=False):
        project = self.load(self.workspace.fs, self.path).bind(self.workspace)
        self.__dict__.update(project.__dict__)

        if reload_snapshots:
            self._reload_snapshots(force=True)

    def _reload_snapshots(self, skip_errors=True, force: bool = False):
        path = posixpath.join(self.path, SNAPSHOTS)
        self.workspace.fs.invalidate_cache(path)
        if force:
            self._snapshots = {}
        for file in self.workspace.fs.listdir(path, detail=False):
            snapshot_id = uuid.UUID(posixpath.basename(file)[: -len(".json")])
            if snapshot_id in self._snapshots:
                continue
            self.reload_snapshot(snapshot_id, skip_errors)

    def reload_snapshot(self, snapshot_id: Union[str, uuid.UUID], skip_errors=True):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid.UUID(snapshot_id)
        try:
            suite = self.load_snapshot(snapshot_id)
            self._snapshots[snapshot_id] = ProjectSnapshot(snapshot_id, self, suite)
        except ValidationError:
            if not skip_errors:
                raise

    @property
    def reports(self) -> Dict[uuid.UUID, Report]:
        self._reload_snapshots()
        return {key: value.value.as_report() for key, value in self._snapshots.items() if value.value.is_report}

    @property
    def test_suites(self) -> Dict[uuid.UUID, TestSuite]:
        self._reload_snapshots()
        return {key: value.value.as_test_suite() for key, value in self._snapshots.items() if not value.value.is_report}

    @property
    def reports_and_test_suites(self) -> Dict[uuid.UUID, ReportBase]:
        self._reload_snapshots()
        return {
            key: value.value.as_report() if value.value.is_report else value.value.as_test_suite()
            for key, value in self._snapshots.items()
        }

    def get_snapshot(self, id: uuid.UUID) -> Optional[ProjectSnapshot]:
        self._reload_snapshots()
        return self._snapshots.get(id, None)

    def build_dashboard_info(
        self, timestamp_start: Optional[datetime.datetime], timestamp_end: Optional[datetime.datetime]
    ) -> DashboardInfo:
        self.reload()
        return self.dashboard.build_dashboard_info(
            [
                r
                for r in self.reports_and_test_suites.values()
                if (timestamp_start is None or r.timestamp >= timestamp_start)
                and (timestamp_end is None or r.timestamp < timestamp_end)
            ]
        )

    def show_dashboard(
        self, timestamp_start: Optional[datetime.datetime] = None, timestamp_end: Optional[datetime.datetime] = None
    ):
        dashboard_info = self.build_dashboard_info(timestamp_start, timestamp_end)
        template_params = TemplateParams(
            dashboard_id="pd_" + str(uuid.uuid4()).replace("-", ""),
            dashboard_info=dashboard_info,
            additional_graphs={},
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(determine_template("inline")(params=template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err


class FSSpecWorkspace(WorkspaceBase[FSSpecProject]):
    fs: AbstractFileSystem

    def __init__(self, uri: str, storage_options: dict = None, protocol: str = None):
        self.uri = uri

        self.fs, _, (path, *_) = get_fs_token_paths(self.uri, storage_options=storage_options, protocol=protocol)
        self.path = path
        self.fs.mkdirs(self.path, exist_ok=True)
        self._projects: Dict[uuid.UUID, FSSpecProject] = self._load_projects()

    def create_project(self, name: str, description: Optional[str] = None) -> FSSpecProject:
        project = Project(name=name, description=description, dashboard=DashboardConfig(name=name, panels=[]))
        return self.add_project(project)

    def add_project(self, project: ProjectBase) -> FSSpecProject:
        if not isinstance(project, FSSpecProject):
            project = FSSpecProject(**project.dict())
        project.bind(self)
        project_id = str(project.id)

        snapshots_path = posixpath.join(self.path, project_id, SNAPSHOTS)
        self.fs.makedirs(snapshots_path, exist_ok=True)
        metadata_path = posixpath.join(self.path, project_id, METADATA_PATH)
        with self.fs.open(metadata_path, "w") as f:
            json.dump(project.dict(), f, indent=2, cls=NumpyEncoder)
        self._projects[project.id] = project
        return project

    def _load_projects(self) -> Dict[uuid.UUID, FSSpecProject]:
        try:
            self.fs.invalidate_cache(self.path)
            projects = [
                FSSpecProject.load(self.fs, p).bind(self)
                for p in self.fs.listdir(self.path, detail=False)
                if self.fs.isdir(p)
            ]
            return {p.id: p for p in projects}
        except FileNotFoundError:
            return {}

    def get_project(self, project_id: STR_UUID) -> Optional[Project]:
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        return self._projects.get(project_id, None)

    def list_projects(self) -> List[FSSpecProject]:
        self._projects = self._load_projects()
        return list(self._projects.values())

    def add_snapshot(self, project_id: STR_UUID, snapshot: Snapshot):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].add_snapshot(snapshot)

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        self._projects[project_id].delete_snapshot(snapshot_id)

    def search_project(self, project_name: str) -> List[FSSpecProject]:
        return [p for p in self._projects.values() if p.name == project_name]

    def reload_project(self, project_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        project = FSSpecProject.load(self.fs, posixpath.join(self.path, str(project_id))).bind(self)
        self._projects[project.id] = project

    def delete_project(self, project_id: STR_UUID):
        if isinstance(project_id, str):
            project_id = uuid.UUID(project_id)
        if project_id in self._projects:
            del self._projects[project_id]
        path = posixpath.join(self.path, str(project_id))
        if self.fs.exists(path):
            self.fs.delete(path, recursive=True)

    def reload_projects(self):
        self._projects = self._load_projects()
