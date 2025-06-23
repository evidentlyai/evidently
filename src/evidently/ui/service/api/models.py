import datetime
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently.legacy.report import Report
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.sdk.models import SnapshotMetadataModel
from evidently.ui.service.base import Org
from evidently.ui.service.type_aliases import OrgID
from evidently.ui.service.type_aliases import SnapshotID


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
    def from_snapshot(cls, snapshot: SnapshotMetadataModel):
        return cls(
            id=snapshot.id,
            name=snapshot.name,
            timestamp=snapshot.timestamp,
            metadata=snapshot.metadata,
            tags=snapshot.tags,
            links=snapshot.links,
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
