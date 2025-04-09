import json
import posixpath
from typing import List

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.serialization import SnapshotModel
from evidently.legacy.ui.storage.local.base import FSLocation
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.ui.workspace import DashboardModel
from evidently.ui.workspace import ProjectModel

DOT_JSON = ".json"

PROJECT_FILE_NAME = "project.json"
SNAPSHOTS_DIR_NAME = "snapshots"


class ProjectWithDashboards(BaseModel):
    project: ProjectModel
    dashboard: DashboardModel


class LocalState:
    def __init__(self, path: str):
        self.path = path
        self.location = FSLocation(base_path=path)

    def _project_dir(self, project_id: ProjectID) -> str:
        return str(project_id)

    def _project_path(self, project_id: ProjectID) -> str:
        return posixpath.join(self._project_dir(project_id), PROJECT_FILE_NAME)

    def _snapshot_dir(self, project_id: ProjectID) -> str:
        return posixpath.join(self._project_dir(project_id), SNAPSHOTS_DIR_NAME)

    def _snapshot_path(self, project_id: ProjectID, snapshot_id: SnapshotID) -> str:
        return posixpath.join(self._snapshot_dir(project_id), str(snapshot_id) + DOT_JSON)

    def read_project(self, project_id: ProjectID) -> ProjectWithDashboards:
        with self.location.open(self._project_path(project_id)) as f:
            return parse_obj_as(ProjectWithDashboards, json.load(f))

    def write_project(self, project: ProjectModel) -> ProjectWithDashboards:
        self.location.makedirs(str(project.id))
        if self.location.exists(self._project_path(project.id)):
            data = self.read_project(project.id)
            data.project = project
        else:
            data = ProjectWithDashboards(project=project, dashboard=DashboardModel(tabs=[], panels=[]))
        with self.location.open(self._project_path(project.id), "w") as f:
            f.write(data.json())
        return data

    def write_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel):
        self.location.makedirs(self._snapshot_dir(project_id))
        with self.location.open(self._snapshot_path(project_id, snapshot_id), "w") as f:
            f.write(snapshot.json())

    def read_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotModel:
        with self.location.open(self._snapshot_path(project_id, snapshot_id)) as f:
            return parse_obj_as(SnapshotModel, json.load(f))

    def list_projects(self) -> List[ProjectID]:
        return [ProjectID(p) for p in self.location.listdir(".")]

    def list_snapshots(self, project_id: ProjectID) -> List[SnapshotID]:
        return [SnapshotID(s[: -len(DOT_JSON)]) for s in self.location.listdir(self._snapshot_dir(project_id))]

    def delete_project(self, project_id: ProjectID):
        self.location.rmtree(str(project_id))

    def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        self.location.rmtree(self._snapshot_path(project_id, snapshot_id))

    def write_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        project = self.read_project(project_id)
        project.dashboard = dashboard
        with self.location.open(self._project_path(project_id), "w") as f:
            f.write(project.json())

    def read_dashboard(self, project_id: ProjectID) -> DashboardModel:
        project = self.read_project(project_id)
        return project.dashboard
