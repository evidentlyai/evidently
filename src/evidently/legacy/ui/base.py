import contextlib
import datetime
import json
from abc import ABC
from abc import abstractmethod
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Set
from typing import Type
from typing import Union

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import parse_obj_as
from evidently.core.report import Snapshot as SnapshotV2
from evidently.legacy.core import new_id
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import ReportBase
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.ui.dashboards.base import DashboardConfig
from evidently.legacy.ui.dashboards.base import PanelValue
from evidently.legacy.ui.dashboards.base import ReportFilter
from evidently.legacy.ui.dashboards.test_suites import TestFilter
from evidently.legacy.ui.type_aliases import BlobID
from evidently.legacy.ui.type_aliases import DataPoints
from evidently.legacy.ui.type_aliases import DataPointsAsType
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PointType
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import TestResultPoints
from evidently.legacy.ui.type_aliases import UserID
from evidently.legacy.utils import NumpyEncoder
from evidently.legacy.utils.dashboard import TemplateParams
from evidently.legacy.utils.dashboard import inline_iframe_html_template
from evidently.legacy.utils.sync import sync_api
from evidently.ui.service.base import Entity
from evidently.ui.service.base import EntityType
from evidently.ui.service.base import Org
from evidently.ui.service.base import Team
from evidently.ui.service.base import User
from evidently.ui.service.base import _default_dashboard

if TYPE_CHECKING:
    from evidently.legacy.ui.managers.projects import ProjectManager

AnySnapshot = Union[Snapshot, SnapshotV2]


class BlobMetadata(BaseModel):
    id: BlobID
    size: Optional[int]


class SnapshotMetadata(BaseModel):
    id: SnapshotID
    name: Optional[str] = None
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    is_report: bool
    blob: "BlobMetadata"
    links: SnapshotLinks = SnapshotLinks()  # links to datasets and stuff

    _project: "Project" = PrivateAttr(None)
    _dashboard_info: "DashboardInfo" = PrivateAttr(None)
    _additional_graphs: Dict[str, dict] = PrivateAttr(None)

    @property
    def project(self):
        return self._project

    async def load(self) -> Snapshot:
        return await self.project.project_manager.load_snapshot(self.project._user_id, self.project.id, self.id)

    async def as_report_base(self) -> ReportBase:
        value = await self.load()
        return value.as_report() if value.is_report else value.as_test_suite()

    def bind(self, project: "Project"):
        self._project = project
        return self

    @classmethod
    def from_snapshot(cls, snapshot: Snapshot, blob: "BlobMetadata") -> "SnapshotMetadata":
        return SnapshotMetadata(
            id=snapshot.id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            is_report=snapshot.is_report,
            blob=blob,
        )

    async def get_dashboard_info(self):
        if self._dashboard_info is None:
            report = await self.as_report_base()
            _, self._dashboard_info, self._additional_graphs = report._build_dashboard_info()
        return self._dashboard_info

    async def get_additional_graphs(self):
        if self._additional_graphs is None:
            report = await self.as_report_base()
            _, self._dashboard_info, self._additional_graphs = report._build_dashboard_info()
        return self._additional_graphs


class Project(Entity):
    entity_type: ClassVar[EntityType] = EntityType.Project

    class Config:
        underscore_attrs_are_private = True

    id: ProjectID = Field(default_factory=new_id)
    name: str
    description: Optional[str] = None
    dashboard: "DashboardConfig" = Field(default_factory=_default_dashboard)

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

    async def load_snapshot_async(self, snapshot_id: SnapshotID) -> Snapshot:
        return await self.project_manager.load_snapshot(self._user_id, self.id, snapshot_id)

    async def add_snapshot_async(self, snapshot: AnySnapshot):
        if not isinstance(snapshot, Snapshot):
            from evidently.ui.backport import snapshot_v2_to_v1

            snapshot = snapshot_v2_to_v1(snapshot)
        await self.project_manager.add_snapshot(self._user_id, self.id, snapshot)

    async def delete_snapshot_async(self, snapshot_id: Union[str, SnapshotID]):
        if isinstance(snapshot_id, str):
            snapshot_id = uuid6.UUID(snapshot_id)
        await self.project_manager.delete_snapshot(self._user_id, self.id, snapshot_id)

    async def list_snapshots_async(
        self, include_reports: bool = True, include_test_suites: bool = True
    ) -> List[SnapshotMetadata]:
        return await self.project_manager.list_snapshots(self._user_id, self.id, include_reports, include_test_suites)

    async def get_snapshot_metadata_async(self, id: SnapshotID) -> SnapshotMetadata:
        return await self.project_manager.get_snapshot_metadata(self._user_id, self.id, id)

    async def build_dashboard_info_async(
        self,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DashboardInfo:
        return await self.dashboard.build(self.project_manager.data_storage, self.id, timestamp_start, timestamp_end)

    async def show_dashboard_async(
        self,
        timestamp_start: Optional[datetime.datetime] = None,
        timestamp_end: Optional[datetime.datetime] = None,
    ):
        dashboard_info = await self.build_dashboard_info_async(timestamp_start, timestamp_end)
        template_params = TemplateParams(
            dashboard_id="pd_" + str(new_id()).replace("-", ""),
            dashboard_info=dashboard_info,
            additional_graphs={},
        )
        # pylint: disable=import-outside-toplevel
        try:
            from IPython.display import HTML

            return HTML(inline_iframe_html_template(params=template_params))
        except ImportError as err:
            raise Exception("Cannot import HTML from IPython.display, no way to show html") from err

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
    show_dashboard = sync_api(show_dashboard_async)
    build_dashboard_info = sync_api(build_dashboard_info_async)
    get_snapshot_metadata = sync_api(get_snapshot_metadata_async)
    add_snapshot = sync_api(add_snapshot_async)
    reload = sync_api(reload_async)


class ProjectMetadataStorage(ABC):
    @abstractmethod
    async def add_project(
        self, project: Project, user: User, team: Optional[Team], org_id: Optional[OrgID] = None
    ) -> Project:
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
    async def add_snapshot(self, project_id: ProjectID, snapshot: Snapshot, blob: "BlobMetadata"):
        raise NotImplementedError

    @abstractmethod
    async def delete_snapshot(self, project_id: ProjectID, snapshot_id: SnapshotID):
        raise NotImplementedError

    @abstractmethod
    async def search_project(self, project_name: str, project_ids: Optional[Set[ProjectID]]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def list_snapshots(
        self,
        project_id: ProjectID,
        include_reports: bool = True,
        include_test_suites: bool = True,
    ) -> List[SnapshotMetadata]:
        raise NotImplementedError

    @abstractmethod
    async def get_snapshot_metadata(self, project_id: ProjectID, snapshot_id: SnapshotID) -> SnapshotMetadata:
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


class DataStorage(ABC):
    @abstractmethod
    async def extract_points(self, project_id: ProjectID, snapshot: Snapshot):
        raise NotImplementedError

    async def load_points(
        self,
        project_id: ProjectID,
        filter: "ReportFilter",
        values: List["PanelValue"],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DataPoints:
        return await self.load_points_as_type(float, project_id, filter, values, timestamp_start, timestamp_end)

    @staticmethod
    def parse_value(cls: Type[PointType], value: Any) -> PointType:
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            value = json.loads(value)
        return parse_obj_as(cls, value)

    @abstractmethod
    async def load_test_results(
        self,
        project_id: ProjectID,
        filter: "ReportFilter",
        test_filters: List["TestFilter"],
        time_agg: Optional[str],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> TestResultPoints:
        raise NotImplementedError

    @abstractmethod
    async def load_points_as_type(
        self,
        cls: Type[PointType],
        project_id: ProjectID,
        filter: "ReportFilter",
        values: List["PanelValue"],
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> DataPointsAsType[PointType]:
        raise NotImplementedError


__all__ = [
    "EntityType",
    "Entity",
    "Org",
    "Project",
    "Team",
    "User",
    "DataStorage",
    "ProjectMetadataStorage",
    "Snapshot",
    "BlobMetadata",
    "AnySnapshot",
]
