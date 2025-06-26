import contextlib
import datetime
import json
from abc import ABC
from abc import abstractmethod
from enum import Enum
from typing import IO
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import TypeVar
from typing import Union

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently.core.report import Snapshot as SnapshotV2
from evidently.core.serialization import SnapshotModel
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.ui.type_aliases import BlobID
from evidently.legacy.ui.type_aliases import EntityID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import UserID
from evidently.legacy.utils import NumpyEncoder
from evidently.legacy.utils.sync import sync_api
from evidently.sdk.models import DashboardModel
from evidently.sdk.models import SnapshotMetadataModel

if TYPE_CHECKING:
    from evidently.ui.service.managers.projects import ProjectManager

AnySnapshot = Union[Snapshot, SnapshotV2]


class SeriesFilter(BaseModel):
    tags: List[str]
    metadata: Dict[str, str]
    metric: str
    metric_labels: Dict[str, str]


class BatchMetricData(BaseModel):
    timestamp_start: Optional[datetime.datetime] = None
    timestamp_end: Optional[datetime.datetime] = None
    series_filter: Optional[List[SeriesFilter]] = None


class Series(BaseModel):
    metric_type: str
    filter_index: int
    params: Dict[str, str]
    values: List[Optional[float]]


class SeriesSource(BaseModel):
    snapshot_id: SnapshotID
    timestamp: datetime.datetime
    tags: List[str]
    metadata: Dict[str, str]


class SeriesResponse(BaseModel):
    sources: List[SeriesSource]
    series: List[Series]


class BlobMetadata(BaseModel):
    id: BlobID
    size: Optional[int]


class EntityType(Enum):
    Config = "config"
    ConfigVersion = "config_version"
    Prompt = "prompt"
    PromptVersion = "prompt_version"
    Dataset = "dataset"
    Project = "project"
    Team = "team"
    Org = "org"


class Entity(BaseModel):
    entity_type: ClassVar[EntityType]
    id: EntityID


class Org(Entity):
    entity_type: ClassVar[EntityType] = EntityType.Org
    id: OrgID = Field(default_factory=new_id)
    name: str


class Team(Entity):
    entity_type: ClassVar[EntityType] = EntityType.Team
    id: TeamID = Field(default_factory=new_id)
    name: str
    org_id: Optional[OrgID]


UT = TypeVar("UT", bound="User")


class User(BaseModel):
    id: UserID = Field(default_factory=new_id)
    name: str
    email: str = ""

    def merge(self: UT, other: "User") -> UT:
        kwargs = {f: getattr(other, f, None) or getattr(self, f) for f in self.__fields__}
        return self.__class__(**kwargs)


def _default_dashboard():
    from evidently.legacy.ui.dashboards import DashboardConfig

    return DashboardConfig(name="", panels=[])


class Project(Entity):
    entity_type: ClassVar[EntityType] = EntityType.Project

    class Config:
        underscore_attrs_are_private = True

    id: ProjectID = Field(default_factory=new_id)
    name: str
    description: Optional[str] = None

    team_id: Optional[TeamID] = None
    org_id: Optional[OrgID] = None

    date_from: Optional[datetime.datetime] = None
    date_to: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = Field(default=None)
    version: str = "1"
    # Field(default=datetime.datetime.fromisoformat("1900-01-01T00:00:00"))

    _project_manager: "ProjectManager" = PrivateAttr(None)
    _user_id: UserID = PrivateAttr(None)

    def bind(self, project_manager: Optional["ProjectManager"], user_id: Optional[UserID]):
        # todo: better typing (add optional or forbid optional)
        self._project_manager = project_manager  # type: ignore[assignment]
        self._user_id = user_id  # type: ignore[assignment]
        return self

    @property
    def project_manager(self) -> "ProjectManager":
        if self._project_manager is None:
            raise ValueError("Project is not binded")
        return self._project_manager

    async def save_async(self):
        await self.project_manager.update_project(self._user_id, self)
        return self

    async def load_snapshot_async(self, snapshot_id: SnapshotID) -> SnapshotModel:
        return await self.project_manager.load_snapshot(self._user_id, self.id, snapshot_id)

    async def add_snapshot_async(self, snapshot: SnapshotModel):
        await self.project_manager.add_snapshot(self._user_id, self.id, snapshot)

    async def delete_snapshot_async(self, snapshot_id: Union[str, SnapshotID]):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid6.UUID(snapshot_id)
        await self.project_manager.delete_snapshot(self._user_id, self.id, snapshot_id)

    async def list_snapshots_async(self) -> List[SnapshotMetadataModel]:
        return await self.project_manager.list_snapshots(self._user_id, self.id)

    async def get_snapshot_metadata_async(self, id: SnapshotID) -> SnapshotMetadataModel:
        return await self.project_manager.get_snapshot_metadata(self._user_id, self.id, id)

    async def reload_async(self, reload_snapshots: bool = False):
        # fixme: reload snapshots
        project = await self.project_manager.get_project(self._user_id, self.id)
        self.__dict__.update(project.__dict__)

        if reload_snapshots:
            await self.project_manager.reload_snapshots(self._user_id, self.id)

    save = sync_api(save_async)
    load_snapshot = sync_api(load_snapshot_async)
    delete_snapshot = sync_api(delete_snapshot_async)
    list_snapshots = sync_api(list_snapshots_async)
    get_snapshot_metadata = sync_api(get_snapshot_metadata_async)
    add_snapshot = sync_api(add_snapshot_async)
    reload = sync_api(reload_async)


class ProjectMetadataStorage(ABC):
    @abstractmethod
    async def add_project(self, project: Project, user: User, org_id: Optional[OrgID] = None) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project(self, project_id: ProjectID) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    async def delete_project(self, project_id: ProjectID):
        raise NotImplementedError

    @abstractmethod
    async def list_projects(self, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def add_snapshot(self, project_id: ProjectID, snapshot: SnapshotModel) -> SnapshotID:
        raise NotImplementedError

    @abstractmethod
    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        raise NotImplementedError

    @abstractmethod
    async def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def list_snapshots(self, project_id: ProjectID) -> List[SnapshotMetadataModel]:
        raise NotImplementedError

    @abstractmethod
    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadataModel:
        raise NotImplementedError

    @abstractmethod
    async def update_project(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def reload_snapshots(self, project_id: ProjectID):
        raise NotImplementedError


class BlobStorage(ABC):
    @abstractmethod
    @contextlib.contextmanager
    def open_blob(self, id: BlobID) -> Iterator[IO]:
        raise NotImplementedError

    @abstractmethod
    async def put_blob(self, blob_id: str, obj):
        raise NotImplementedError

    def get_snapshot_blob_id(self, project_id: ProjectID, snapshot: Snapshot) -> BlobID:
        raise NotImplementedError

    async def put_snapshot(self, project_id: ProjectID, snapshot: Snapshot) -> BlobMetadata:
        id = self.get_snapshot_blob_id(project_id, snapshot)
        await self.put_blob(id, json.dumps(snapshot.dict(), cls=NumpyEncoder))
        return await self.get_blob_metadata(id)

    async def get_blob_metadata(self, blob_id: BlobID) -> BlobMetadata:
        raise NotImplementedError


class ProjectDashboardStorage:
    @abstractmethod
    async def get_project_dashboard(self, project_id: ProjectID) -> DashboardModel:
        raise NotImplementedError


class DataStorage(ABC):
    @abstractmethod
    async def add_snapshot_points(self, project_id: ProjectID, snapshot_id: SnapshotID, snapshot: SnapshotModel):
        raise NotImplementedError

    @abstractmethod
    async def get_data_series(
        self,
        project_id: ProjectID,
        series_filter: List[SeriesFilter],
        start_time: Optional[datetime.datetime],
        end_time: Optional[datetime.datetime],
    ) -> SeriesResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_metrics(self, project_id: ProjectID, tags: List[str], metadata: Dict[str, str]) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_metric_labels(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
    ) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def get_metric_label_values(
        self,
        project_id: ProjectID,
        tags: List[str],
        metadata: Dict[str, str],
        metric: str,
        label: str,
    ) -> List[str]:
        raise NotImplementedError
