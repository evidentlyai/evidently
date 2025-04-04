import contextlib
import datetime
import json
import posixpath
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Type

import uuid6
from fsspec import AbstractFileSystem
from fsspec import get_fs_token_paths

from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import ValidationError
from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests.base_test import Test
from evidently.legacy.ui.base import BlobMetadata
from evidently.legacy.ui.base import BlobStorage
from evidently.legacy.ui.base import DataStorage
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.base import ProjectMetadataStorage
from evidently.legacy.ui.base import SnapshotMetadata
from evidently.legacy.ui.base import Team
from evidently.legacy.ui.base import User
from evidently.legacy.ui.dashboards.base import PanelValue
from evidently.legacy.ui.dashboards.base import ReportFilter
from evidently.legacy.ui.dashboards.test_suites import TestFilter
from evidently.legacy.ui.dashboards.test_suites import to_period
from evidently.legacy.ui.errors import ProjectNotFound
from evidently.legacy.ui.managers.projects import ProjectManager
from evidently.legacy.ui.storage.common import NO_TEAM
from evidently.legacy.ui.storage.common import NO_USER
from evidently.legacy.ui.type_aliases import BlobID
from evidently.legacy.ui.type_aliases import DataPointsAsType
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PointInfo
from evidently.legacy.ui.type_aliases import PointType
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TestInfo
from evidently.legacy.ui.type_aliases import TestResultPoints
from evidently.legacy.utils import NumpyEncoder

SNAPSHOTS = "snapshots"
METADATA_PATH = "metadata.json"


class FSLocation:
    fs: AbstractFileSystem
    path: str

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.fs: AbstractFileSystem
        self.path: str
        self.fs, _, (self.path, *_) = get_fs_token_paths(self.base_path)

    @contextlib.contextmanager
    def open(self, path: str, mode="r"):
        with self.fs.open(posixpath.join(self.path, path), mode) as f:
            yield f

    def makedirs(self, path: str):
        self.fs.makedirs(posixpath.join(self.path, path), exist_ok=True)

    def listdir(self, path: str):
        try:
            fullpath = posixpath.join(self.path, path)
            return [posixpath.relpath(p, fullpath) for p in self.fs.listdir(fullpath, detail=False)]
        except FileNotFoundError:
            return []

    def isdir(self, path: str):
        return self.fs.isdir(posixpath.join(self.path, path))

    def exists(self, path: str):
        return self.fs.exists(posixpath.join(self.path, path))

    def rmtree(self, path: str):
        return self.fs.delete(posixpath.join(self.path, path), recursive=True)

    def invalidate_cache(self, path):
        self.fs.invalidate_cache(posixpath.join(self.path, path))

    def size(self, path):
        return self.fs.size(posixpath.join(self.path, path))


class FSSpecBlobStorage(BlobStorage):
    base_path: str

    _location: FSLocation = PrivateAttr(None)

    def __init__(self, base_path: str):
        self.base_path = base_path
        self._location = FSLocation(self.base_path)

    @property
    def location(self) -> FSLocation:
        if self._location is None:
            self._location = FSLocation(self.base_path)
        return self._location

    def get_snapshot_blob_id(self, project_id: ProjectID, snapshot: Snapshot) -> BlobID:
        return posixpath.join(str(project_id), SNAPSHOTS, str(snapshot.id)) + ".json"

    @contextlib.contextmanager
    def open_blob(self, blob_id: str):
        with self.location.open(blob_id) as f:
            yield f

    async def put_blob(self, blob_id: BlobID, obj) -> BlobID:
        self.location.makedirs(posixpath.dirname(blob_id))
        with self.location.open(blob_id, "w") as f:
            f.write(obj)
        return blob_id

    async def get_blob_metadata(self, blob_id: BlobID) -> BlobMetadata:
        return BlobMetadata(id=blob_id, size=self.location.size(blob_id))


def load_project(location: FSLocation, path: str) -> Optional[Project]:
    try:
        with location.open(posixpath.join(path, METADATA_PATH)) as f:
            return parse_obj_as(Project, json.load(f))
    except FileNotFoundError:
        return None


class LocalState:
    def __init__(self, path: str, project_manager: Optional[ProjectManager]):
        self.path = path
        self.project_manager = project_manager
        self.projects: Dict[ProjectID, Project] = {}
        self.snapshots: Dict[ProjectID, Dict[SnapshotID, SnapshotMetadata]] = {}
        self.snapshot_data: Dict[ProjectID, Dict[SnapshotID, Snapshot]] = {}
        self.location = FSLocation(base_path=self.path)

    @classmethod
    def load(cls, path: str, project_manager: Optional[ProjectManager]):
        state = LocalState(path, project_manager)

        state.location.makedirs("")
        state.reload()
        return state

    def reload(self, force: bool = False):
        self.location.invalidate_cache("")
        projects = [load_project(self.location, p) for p in self.location.listdir("") if self.location.isdir(p)]
        self.projects = {p.id: p.bind(self.project_manager, NO_USER.id) for p in projects if p is not None}
        self.snapshots = {p: {} for p in self.projects}
        self.snapshot_data = {p: {} for p in self.projects}

        for project_id in self.projects:
            self.reload_snapshots(project_id, force=force, skip_errors=False)

    def reload_snapshots(self, project_id: ProjectID, force: bool = False, skip_errors: bool = True):
        path = posixpath.join(str(project_id), SNAPSHOTS)
        if force:
            self.snapshots[project_id] = {}
            self.snapshot_data[project_id] = {}

        project = self.projects[project_id]
        self.location.invalidate_cache(path)
        for file in self.location.listdir(path):
            snapshot_id = uuid6.UUID(posixpath.basename(file)[: -len(".json")])
            if snapshot_id in self.snapshots[project_id]:
                continue
            self.reload_snapshot(project, snapshot_id, skip_errors)

    def reload_snapshot(self, project: Project, snapshot_id: SnapshotID, skip_errors: bool = True):
        try:
            snapshot_path = posixpath.join(str(project.id), SNAPSHOTS, str(snapshot_id) + ".json")
            with self.location.open(snapshot_path) as f:
                suite = parse_obj_as(Snapshot, json.load(f))
            snapshot = SnapshotMetadata.from_snapshot(
                suite, BlobMetadata(id=snapshot_path, size=self.location.size(snapshot_path))
            ).bind(project)
            self.snapshots[project.id][snapshot_id] = snapshot
            self.snapshot_data[project.id][snapshot_id] = suite
        except ValidationError as e:
            if not skip_errors:
                raise ValueError(f"{snapshot_id} is malformed") from e


class JsonFileProjectMetadataStorage(ProjectMetadataStorage):
    path: str

    _state: LocalState = PrivateAttr(None)

    def __init__(self, path: str, local_state: Optional[LocalState] = None):
        self.path = path
        self._state = local_state or LocalState.load(self.path, None)

    @property
    def state(self):
        if self._state is None:
            self._state = LocalState.load(self.path, None)
        return self._state

    async def add_project(
        self, project: Project, user: User, team: Optional[Team], org_id: Optional[OrgID] = None
    ) -> Project:
        project_id = str(project.id)
        project.org_id = org_id
        self.state.location.makedirs(posixpath.join(project_id, SNAPSHOTS))
        with self.state.location.open(posixpath.join(project_id, METADATA_PATH), "w") as f:
            json.dump(project.dict(), f, indent=2, cls=NumpyEncoder)
        self.state.projects[project.id] = project
        self.state.reload_snapshots(project.id, force=True)
        return project

    async def update_project(self, project: Project) -> Project:
        return await self.add_project(project, NO_USER, NO_TEAM, org_id=None)

    async def get_project(self, project_id: ProjectID) -> Optional[Project]:
        return self.state.projects.get(project_id)

    async def delete_project(self, project_id: ProjectID):
        if project_id in self.state.projects:
            del self.state.projects[project_id]
        path = str(project_id)
        if self.state.location.exists(path):
            self.state.location.rmtree(path)

    async def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        projects = [p for p in self.state.projects.values() if project_ids is None or p.id in project_ids]
        default_date = datetime.datetime.fromisoformat("1900-01-01T00:00:00")
        projects.sort(key=lambda x: x.created_at or default_date, reverse=True)
        return projects

    async def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot, blob: "BlobMetadata"):
        project = await self.get_project(project_id)
        if project is None:
            raise ProjectNotFound()
        self.state.snapshots[project_id][snapshot.id] = SnapshotMetadata.from_snapshot(snapshot, blob).bind(project)
        self.state.snapshot_data[project_id][snapshot.id] = snapshot

    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        if project_id in self.state.projects and snapshot_id in self.state.snapshots[project_id]:
            del self.state.snapshots[project_id][snapshot_id]
            del self.state.snapshot_data[project_id][snapshot_id]
        path = posixpath.join(str(project_id), SNAPSHOTS, f"{snapshot_id}.json")
        if self.state.location.exists(path):
            self.state.location.rmtree(path)

    async def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        return [
            p
            for p in self.state.projects.values()
            if p.name == project_name and (project_ids is None or p.id in project_ids)
        ]

    async def list_snapshots(
        self, project_id: ProjectID, include_reports: bool = True, include_test_suites: bool = True
    ) -> List[SnapshotMetadata]:
        return [
            s
            for s in self.state.snapshots.get(project_id, {}).values()
            if (include_reports and s.is_report) or (include_test_suites and not s.is_report)
        ]

    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadata:
        return self.state.snapshots[project_id][snapshot_id]

    async def reload_snapshots(self, project_id: ProjectID):
        self.state.reload_snapshots(project_id=project_id, force=True)


class InMemoryDataStorage(DataStorage):
    path: str

    _state: LocalState = PrivateAttr(None)

    def __init__(self, path: str, local_state: Optional[LocalState] = None):
        self.path = path
        self._state = local_state or LocalState.load(self.path, None)

    @property
    def state(self):
        if self._state is None:
            self._state = LocalState.load(self.path, None)
        return self._state

    async def extract_points(self, project_id: ProjectID, snapshot: Snapshot):
        pass

    async def load_test_results(
        self,
        project_id: ProjectID,
        filter: ReportFilter,
        test_filters: List[TestFilter],
        time_agg: Optional[str],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> TestResultPoints:
        points: Dict[datetime.datetime, Dict[Test, TestInfo]] = defaultdict(dict)
        for report in (
            s.as_test_suite()
            for s in self.state.snapshot_data[project_id].values()
            if not s.is_report or s.is_new_report
        ):
            if not (
                filter.filter(report)
                and isinstance(report, TestSuite)
                and (timestamp_start is None or report.timestamp >= timestamp_start)
                and (timestamp_end is None or report.timestamp <= timestamp_end)
            ):
                continue

            ts = to_period(time_agg, report.timestamp)
            if test_filters:
                for test_filter in test_filters:
                    points[ts].update(test_filter.get(report))
            else:
                points[ts].update(TestFilter().get(report))

        return points

    async def load_points_as_type(
        self,
        cls: Type[PointType],
        project_id: ProjectID,
        filter: "ReportFilter",
        values: List["PanelValue"],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DataPointsAsType[PointType]:
        points: DataPointsAsType[PointType] = [{} for _ in range(len(values))]
        for report in (s.as_report() for s in self.state.snapshot_data[project_id].values() if s.is_report):
            if not (
                filter.filter(report)
                and (timestamp_start is None or report.timestamp >= timestamp_start)
                and (timestamp_end is None or report.timestamp <= timestamp_end)
            ):
                continue

            for i, value in enumerate(values):
                for metric, metric_field_value in value.get(report).items():
                    if metric not in points[i]:
                        points[i][metric] = []
                    points[i][metric].append(
                        PointInfo(report.timestamp, report.id, self.parse_value(cls, metric_field_value))
                    )
        return points
