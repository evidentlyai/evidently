import json
import posixpath
import re
from typing import List

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.serialization import SnapshotModel
from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import ProjectModel
from evidently.ui.service.storage.fslocation import FSLocation
from evidently.ui.service.type_aliases import STR_UUID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID

DOT_JSON = ".json"

PROJECT_FILE_NAME = "metadata.json"
DASHBOARD_FILE_NAME = "dashboard.json"
SNAPSHOTS_DIR_NAME = "snapshots"


UUID_REGEX = re.compile("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


class ProjectWithDashboards(BaseModel):
    project: ProjectModel
    dashboard: DashboardModel


class LocalState:
    def __init__(self, path: str):
        self.path = path
        self.location = FSLocation(base_path=path)

    def _project_dir(self, project_id: STR_UUID) -> str:
        return str(project_id)

    def _project_path(self, project_id: STR_UUID) -> str:
        return posixpath.join(self._project_dir(project_id), PROJECT_FILE_NAME)

    def _dashboard_path(self, project_id: STR_UUID) -> str:
        return posixpath.join(self._project_dir(project_id), DASHBOARD_FILE_NAME)

    def _snapshot_dir(self, project_id: STR_UUID) -> str:
        return posixpath.join(self._project_dir(project_id), SNAPSHOTS_DIR_NAME)

    def _snapshot_path(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> str:
        return posixpath.join(self._snapshot_dir(project_id), str(snapshot_id) + DOT_JSON)

    def read_project(self, project_id: STR_UUID) -> ProjectModel:
        with self.location.open(self._project_path(project_id)) as f:
            return parse_obj_as(ProjectModel, json.load(f))

    def write_project(self, project: ProjectModel) -> ProjectModel:
        self.location.makedirs(str(project.id))
        with self.location.open(self._project_path(project.id), "w") as f:
            json.dump(project.dict(), f, cls=NumpyEncoder, indent=2)
        return project

    def write_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID, snapshot: SnapshotModel):
        self.location.makedirs(self._snapshot_dir(project_id))
        with self.location.open(self._snapshot_path(project_id, snapshot_id), "w") as f:
            json.dump(snapshot.dict(), f, cls=NumpyEncoder)

    def read_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID) -> SnapshotModel:
        with self.location.open(self._snapshot_path(project_id, snapshot_id)) as f:
            return parse_obj_as(SnapshotModel, json.load(f))

    def list_projects(self) -> List[ProjectID]:
        projects = []
        for p in self.location.listdir("."):
            if not UUID_REGEX.match(p):
                continue
            projects.append(ProjectID(p))
        return projects

    def list_snapshots(self, project_id: STR_UUID) -> List[SnapshotID]:
        snapshots = []
        for s in self.location.listdir(self._snapshot_dir(project_id)):
            sid = s[: -len(DOT_JSON)]
            if not UUID_REGEX.match(sid):
                continue
            snapshots.append(SnapshotID(sid))
        return snapshots

    def delete_project(self, project_id: STR_UUID):
        self.location.rmtree(str(project_id))

    def delete_snapshot(self, project_id: STR_UUID, snapshot_id: STR_UUID):
        self.location.rmtree(self._snapshot_path(project_id, snapshot_id))

    def write_dashboard(self, project_id: STR_UUID, dashboard: DashboardModel):
        with self.location.open(self._dashboard_path(project_id), "w") as f:
            json.dump(dashboard.dict(), f, cls=NumpyEncoder)

    def read_dashboard(self, project_id: STR_UUID) -> DashboardModel:
        if not self.location.exists(self._dashboard_path(project_id)):
            return DashboardModel(tabs=[], panels=[])
        with self.location.open(self._dashboard_path(project_id)) as f:
            return parse_obj_as(DashboardModel, json.load(f))
