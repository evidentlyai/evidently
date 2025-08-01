import contextlib
import datetime
import json
import posixpath
import re
import uuid
from typing import Dict
from typing import List
from typing import Optional
from typing import Set

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import ValidationError
from evidently._pydantic_compat import parse_obj_as
from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import ByLabelValue
from evidently.core.metric_types import CountValue
from evidently.core.metric_types import MeanStdValue
from evidently.core.metric_types import SingleValue
from evidently.core.serialization import SnapshotModel
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.utils import NumpyEncoder
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import BlobMetadata
from evidently.ui.service.base import BlobStorage
from evidently.ui.service.base import DataStorage
from evidently.ui.service.base import Project
from evidently.ui.service.base import ProjectMetadataStorage
from evidently.ui.service.base import Series
from evidently.ui.service.base import SeriesFilter
from evidently.ui.service.base import SeriesResponse
from evidently.ui.service.base import SeriesSource
from evidently.ui.service.base import User
from evidently.ui.service.errors import ProjectNotFound
from evidently.ui.service.managers.projects import ProjectManager
from evidently.ui.service.storage.common import NO_USER
from evidently.ui.service.storage.fslocation import FSLocation
from evidently.ui.service.type_aliases import BlobID
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.service.type_aliases import SnapshotID
from evidently.ui.storage.local.base import LocalState as WorkspaceLocalState

SNAPSHOTS = "snapshots"
METADATA_PATH = "metadata.json"


UUID_REGEX = re.compile("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


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

    async def put_blob(self, blob_id: BlobID, obj: str) -> BlobID:
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


class LocalState(WorkspaceLocalState):
    def __init__(self, path: str, project_manager: Optional[ProjectManager]):
        super().__init__(path)
        self.project_manager = project_manager
        self.projects: Dict[ProjectID, Project] = {}
        self.snapshots: Dict[ProjectID, Dict[SnapshotID, SnapshotModel]] = {}

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

        for project_id in self.projects:
            self.reload_snapshots(project_id, force=force, skip_errors=False)

    def reload_snapshots(self, project_id: ProjectID, force: bool = False, skip_errors: bool = True):
        path = posixpath.join(str(project_id), SNAPSHOTS)
        if force:
            self.snapshots[project_id] = {}

        project = self.projects[project_id]
        self.location.invalidate_cache(path)
        for file in self.location.listdir(path):
            filename = posixpath.basename(file)
            if not filename.endswith(".json"):
                continue
            sid_str = filename[: -len(".json")]
            if not UUID_REGEX.match(sid_str):
                continue
            snapshot_id = uuid6.UUID(sid_str)
            if snapshot_id in self.snapshots[project_id]:
                continue
            self.reload_snapshot(project, snapshot_id, skip_errors)

    def reload_snapshot(self, project: Project, snapshot_id: SnapshotID, skip_errors: bool = True):
        try:
            snapshot_path = posixpath.join(str(project.id), SNAPSHOTS, str(snapshot_id) + ".json")
            with self.location.open(snapshot_path) as f:
                model = parse_obj_as(SnapshotModel, json.load(f))
            self.snapshots[project.id][snapshot_id] = model
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

    async def add_project(self, project: Project, user: User, org_id: Optional[OrgID] = None) -> Project:
        project_id = str(project.id)
        project.org_id = org_id
        self.state.location.makedirs(posixpath.join(project_id, SNAPSHOTS))
        with self.state.location.open(posixpath.join(project_id, METADATA_PATH), "w") as f:
            json.dump(project.dict(), f, indent=2, cls=NumpyEncoder)
        self.state.projects[project.id] = project
        self.state.reload_snapshots(project.id, force=True)
        return project

    async def update_project(self, project: Project) -> Project:
        return await self.add_project(project, NO_USER, org_id=None)

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

    async def add_snapshot(self, project_id: ProjectID, snapshot: SnapshotModel) -> SnapshotID:
        project = await self.get_project(project_id)
        if project is None:
            raise ProjectNotFound()
        snapshot_id = uuid6.uuid7()
        self.state.snapshots[project_id][snapshot_id] = snapshot
        return snapshot_id

    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        if project_id in self.state.projects and snapshot_id in self.state.snapshots[project_id]:
            del self.state.snapshots[project_id][snapshot_id]
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
    ) -> List[SnapshotMetadataModel]:
        return [
            SnapshotMetadataModel(
                id=snapshot_id,
                name=snapshot.name,
                metadata=snapshot.metadata,
                tags=snapshot.tags,
                timestamp=snapshot.timestamp,
                links=SnapshotLinks(),
            )
            for snapshot_id, snapshot in self.state.snapshots[project_id].items()
        ]

    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadataModel:
        snapshot = self.state.snapshots[project_id][snapshot_id]
        return SnapshotMetadataModel(
            id=snapshot_id,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            timestamp=snapshot.timestamp,
            links=SnapshotLinks(),
        )

    async def reload_snapshots(self, project_id: ProjectID):
        self.state.reload_snapshots(project_id=project_id, force=True)

    async def save_dashboard(self, project_id: ProjectID, dashboard: DashboardModel):
        pass


class MetricItem(BaseModel):
    snapshot_id: SnapshotID
    timestamp: datetime.datetime
    metric_id: str
    metric_type: str
    params: Dict[str, str]
    value: float


class InMemoryDataStorage(DataStorage):
    path: str

    _state: LocalState = PrivateAttr(None)
    _metrics_points: Dict[uuid.UUID, Dict[uuid.UUID, List[MetricItem]]] = PrivateAttr(None)

    def __init__(self, path: str, local_state: Optional[LocalState] = None):
        self.path = path
        self._state = local_state or LocalState.load(self.path, None)
        self._metrics_points = {}
        for project_id, snapshots in self._state.snapshots.items():
            for snapshot_id, snapshot in snapshots.items():
                self._add_snapshot_points_sync(project_id, snapshot_id, snapshot)

    @property
    def state(self):
        if self._state is None:
            self._state = LocalState.load(self.path, None)
        return self._state

    async def add_snapshot_points(self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel):
        return self._add_snapshot_points_sync(project_id, snapshot_id, snapshot)

    def _add_snapshot_points_sync(self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel):
        for result in snapshot.metric_results.values():
            if isinstance(result, SingleValue):
                self._add_value(project_id, snapshot_id, snapshot.timestamp, result)
            elif isinstance(result, ByLabelValue):
                for value in result.values.values():
                    self._add_value(project_id, snapshot_id, snapshot.timestamp, value)
            elif isinstance(result, CountValue):
                self._add_value(project_id, snapshot_id, snapshot.timestamp, result.count)
                self._add_value(project_id, snapshot_id, snapshot.timestamp, result.share)
            elif isinstance(result, MeanStdValue):
                self._add_value(project_id, snapshot_id, snapshot.timestamp, result.mean)
                self._add_value(project_id, snapshot_id, snapshot.timestamp, result.std)
            elif isinstance(result, ByLabelCountValue):
                for value in result.counts.values():
                    self._add_value(project_id, snapshot_id, snapshot.timestamp, value)
                for value in result.shares.values():
                    self._add_value(project_id, snapshot_id, snapshot.timestamp, value)
            else:
                raise ValueError(f"type {type(result)} isn't supported")

    def _add_value(
        self,
        project_id: ProjectID,
        snapshot_id: SnapshotID,
        timestamp: datetime.datetime,
        result: SingleValue,
    ) -> None:
        params = {}
        if result.metric_value_location is None:
            raise ValueError("metric_value_location should be set")
        for k, v in result.metric_value_location.param.items():
            if k in params:
                raise ValueError("duplicated key?")
            params[k] = str(v)
        for k, v in result.metric_value_location.metric.params.items():
            if k in ["type", "tests", "count_tests", "share_tests", "mean_tests", "std_tests"]:
                continue
            params[k] = str(v)
        if project_id not in self._metrics_points:
            self._metrics_points[project_id] = {}
        if snapshot_id not in self._metrics_points[project_id]:
            self._metrics_points[project_id][snapshot_id] = []
        self._metrics_points[project_id][snapshot_id].append(
            MetricItem(
                snapshot_id=snapshot_id,
                timestamp=timestamp,
                metric_id=result.metric_value_location.metric.metric_id,
                metric_type=result.metric_value_location.metric.params["type"],
                params=params,
                value=result.value,
            )
        )

    async def get_metrics(self, project_id: ProjectID, tags: List[str], metadata: Dict[str, str]) -> List[str]:
        metrics = []
        for snapshot_id, snapshot in self.state.snapshots[project_id].items():
            if set(snapshot.tags) >= set(tags) and snapshot.metadata.items() >= metadata.items():
                metrics.extend(
                    [x.metric_value_location.metric.params["type"] for x in snapshot.metric_results.values()]
                )
        return list(set(metrics))

    async def get_metric_labels(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
    ) -> List[str]:
        labels = []
        for snapshot_id, snapshot in self.state.snapshots[project_id].items():
            if set(snapshot.tags) >= set(tags) and snapshot.metadata.items() >= metadata.items():
                for x in snapshot.metric_results.values():
                    if x.metric_value_location.metric.params["type"] == metric:
                        labels.extend(list(x.metric_value_location.metric.params.keys()))
        return list(set(x for x in labels if x not in ["type"]))

    async def get_metric_label_values(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
        label: str,
    ) -> List[str]:
        values = []
        for snapshot_id, snapshot in self.state.snapshots[project_id].items():
            if set(snapshot.tags) >= set(tags) and snapshot.metadata.items() >= metadata.items():
                for x in snapshot.metric_results.values():
                    if x.metric_value_location.metric.params["type"] == metric:
                        values.append(x.metric_value_location.metric.params.get(label))
        return list(set(x for x in values if x and x not in ["type"]))

    async def get_data_series(
        self,
        project_id: ProjectID,
        series_filter: List[SeriesFilter],
        start_time: Optional[datetime.datetime],
        end_time: Optional[datetime.datetime],
    ) -> SeriesResponse:
        matching_snapshots = []
        sources = []
        series = {}
        for snapshot_id, snapshot in self.state.snapshots[project_id].items():
            if start_time is not None and snapshot.timestamp < start_time:
                continue
            if end_time is not None and snapshot.timestamp > end_time:
                continue
            for filter_item in series_filter:
                if (
                    set(snapshot.tags) >= set(filter_item.tags)
                    and snapshot.metadata.items() >= filter_item.metadata.items()
                ):
                    matching_snapshots.append((snapshot_id, snapshot.timestamp, snapshot))
        matching_snapshots = sorted(matching_snapshots, key=lambda x: (x[1], x[0]))
        matching_snapshots_map = {snapshot_id: snapshot for snapshot_id, timestamp, snapshot in matching_snapshots}

        last_snapshot = None
        series_filters_map: Dict[tuple, int] = {}
        index = 0
        for snapshot_id, timestamp, snapshot in matching_snapshots:
            for item in self._metrics_points.get(project_id, {}).get(snapshot_id, []):
                metric_type = item.metric_type
                params = item.params
                snapshot_tags = matching_snapshots_map[snapshot_id].tags
                snapshot_metadata = matching_snapshots_map[snapshot_id].metadata
                value = item.value

                filter = next(
                    (
                        f
                        for f in series_filter
                        if f.metric in ("*", metric_type) and params.items() >= f.metric_labels.items()
                    ),
                    None,
                )

                if filter is None or not (
                    set(snapshot_tags) >= set(filter.tags) and snapshot_metadata.items() >= filter.metadata.items()
                ):
                    continue

                if last_snapshot is None:
                    last_snapshot = snapshot_id
                    sources.append(
                        SeriesSource(
                            snapshot_id=snapshot_id, timestamp=timestamp, tags=snapshot_tags, metadata=snapshot_metadata
                        )
                    )
                if last_snapshot != snapshot_id:
                    last_snapshot = snapshot_id
                    sources.append(
                        SeriesSource(
                            snapshot_id=snapshot_id, timestamp=timestamp, tags=snapshot_tags, metadata=snapshot_metadata
                        )
                    )
                    index += 1
                series_id = metric_type + ":" + ",".join([f"{k}={v}" for k, v in params.items()])
                key = (
                    metric_type,
                    frozenset(params.items()),
                    frozenset(snapshot_tags),
                    frozenset(snapshot_metadata.items()),
                )
                filter_index = series_filters_map.get(key)
                if filter_index is None:
                    filter_index = _find_filter_index(
                        series_filter, metric_type, params, snapshot_tags, snapshot_metadata
                    )
                    if filter_index is not None:
                        series_filters_map[key] = filter_index

                if filter_index is None and len(series_filter) > 0:
                    raise ValueError("No filters found for series ({})")

                if series_id not in series:
                    series[series_id] = Series(
                        metric_type=metric_type,
                        filter_index=filter_index or 0,
                        params={k: v for k, v in params.items() if v and v != "None"},
                        values=([None] * index) + [value],
                    )
                else:
                    if len(series[series_id].values) < (index + 1):
                        series[series_id].values.extend([None] * (index - len(series[series_id].values) + 1))
                    series[series_id].values[index] = value

        return SeriesResponse(sources=sources, series=list(series.values()))


def _find_filter_index(
    filters: List[SeriesFilter],
    metric_type: str,
    params: Dict[str, str],
    snapshot_tags: List[str],
    snapshot_metadata: Dict[str, str],
) -> Optional[int]:
    for idx, series_filter in enumerate(filters):
        if (
            series_filter.metric in ("*", metric_type)
            and series_filter.metric_labels.items() <= params.items()
            and set(series_filter.tags) <= set(snapshot_tags)
            and series_filter.metadata.items() <= snapshot_metadata.items()
        ):
            return idx
    return None
