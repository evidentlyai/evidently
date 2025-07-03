import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Extra
from evidently.legacy.base_metric import Metric
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.report import Report
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.ui.base import EntityType
from evidently.legacy.ui.base import Org
from evidently.legacy.ui.base import Project
from evidently.legacy.ui.base import SnapshotMetadata
from evidently.legacy.ui.base import Team
from evidently.legacy.ui.base import User
from evidently.legacy.ui.managers.auth import Role
from evidently.legacy.ui.type_aliases import ZERO_UUID
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import RoleID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TeamID
from evidently.legacy.ui.type_aliases import UserID


class EvidentlyAPIModel(BaseModel):
    # todo: migrate all models to this base
    class Config:
        extra = Extra.forbid


class MetricModel(BaseModel):
    id: str

    @classmethod
    def from_metric(cls, metric: Metric):
        return cls(id=metric.get_id())


class ReportModel(BaseModel):
    id: SnapshotID
    name: Optional[str]
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    links: SnapshotLinks = SnapshotLinks()

    @classmethod
    def from_report(cls, report: Report):
        return cls(
            id=report.id,
            name=report.name,
            timestamp=report.timestamp,
            metadata=report.metadata,
            tags=report.tags,
        )

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotMetadata):
        return cls(
            id=snapshot.id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            links=snapshot.links,
        )


class TestSuiteModel(BaseModel):
    id: SnapshotID
    name: Optional[str]
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    links: SnapshotLinks = SnapshotLinks()

    @classmethod
    def from_report(cls, report: TestSuite):
        return cls(
            id=report.id,
            name=report.name,
            timestamp=report.timestamp,
            metadata=report.metadata,
            tags=report.tags,
        )

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotMetadata):
        return cls(
            id=snapshot.id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            links=snapshot.links,
        )


class DashboardInfoModel(BaseModel):
    name: str
    widgets: List[BaseWidgetInfo]
    min_timestamp: Optional[datetime.datetime] = None
    max_timestamp: Optional[datetime.datetime] = None

    @classmethod
    def from_dashboard_info(cls, dashboard_info: DashboardInfo):
        return DashboardInfo(
            name=dashboard_info.name,
            widgets=dashboard_info.widgets,
        )

    @classmethod
    async def from_project_with_time_range(
        cls,
        project: Project,
        timestamp_start: Optional[datetime.datetime] = None,
        timestamp_end: Optional[datetime.datetime] = None,
    ):
        time_range: Dict[str, Optional[datetime.datetime]]
        snapshots = await project.list_snapshots_async()
        if len(snapshots) == 0:
            time_range = {"min_timestamp": None, "max_timestamp": None}
        else:
            time_range = dict(
                min_timestamp=min(r.timestamp for r in snapshots),
                max_timestamp=max(r.timestamp for r in snapshots),
            )

        info = await project.build_dashboard_info_async(timestamp_start=timestamp_start, timestamp_end=timestamp_end)

        return cls(
            name=info.name,
            widgets=info.widgets,
            min_timestamp=time_range["min_timestamp"],
            max_timestamp=time_range["max_timestamp"],
        )


class OrgModel(BaseModel):
    id: OrgID
    name: str

    @classmethod
    def from_org(cls, org: Org):
        return OrgModel(id=org.id, name=org.name)

    def to_org(self) -> Org:
        return Org(id=self.id, name=self.name)


class TeamModel(BaseModel):
    id: TeamID
    name: str
    org_id: OrgID

    @classmethod
    def from_team(cls, team: Team):
        return TeamModel(id=team.id, name=team.name, org_id=team.org_id or ZERO_UUID)

    def to_team(self) -> Team:
        return Team(id=self.id, name=self.name, org_id=self.org_id)


UT = TypeVar("UT", bound="UserModel")


class UserModel(BaseModel):
    id: UserID
    name: str
    email: str

    @classmethod
    def from_user(cls, user: User):
        return UserModel(id=user.id, name=user.name, email=user.email)

    def merge(self: UT, other: "UserModel") -> UT:
        kwargs = {f: getattr(other, f, None) or getattr(self, f) for f in self.__fields__}
        return self.__class__(**kwargs)


class RoleModel(BaseModel):
    id: RoleID
    name: str
    entity_type: Optional[EntityType]

    @classmethod
    def from_role(cls, role: Role):
        return RoleModel(id=role.id, name=role.name, entity_type=role.entity_type)


class Version(BaseModel):
    application: str
    version: str
    commit: str
