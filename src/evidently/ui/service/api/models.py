import datetime
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently.legacy.model.dashboard import DashboardInfo
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.report import Report
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import Org
from evidently.ui.service.base import Project
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import SnapshotID


class ReportModel(BaseModel):
    id: SnapshotID
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]
    links: SnapshotLinks = SnapshotLinks()

    @classmethod
    def from_report(cls, report: Report):
        return cls(
            id=report.id,
            timestamp=report.timestamp,
            metadata=report.metadata,
            tags=report.tags,
        )

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotMetadataModel):
        return cls(
            id=snapshot.id,
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


class Version(BaseModel):
    application: str
    version: str
    commit: str
