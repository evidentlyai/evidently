from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import validator
from evidently.legacy.core import new_id
from evidently.legacy.suite.base_suite import SnapshotLinks
from evidently.legacy.ui.type_aliases import OrgID
from evidently.legacy.ui.type_aliases import PanelID
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.legacy.ui.type_aliases import TabID


class DashboardTabModel(BaseModel):
    id: TabID = Field(default_factory=uuid6.uuid7)
    title: Optional[str]
    panels: List[PanelID]


class PanelMetric(BaseModel):
    legend: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
    metric: str
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    view_params: Dict[str, Any] = Field(default_factory=dict)

    @validator("metric")
    def metric_is_alias(cls, v):
        if not v.startswith("evidently:metric_v2:"):
            v = f"evidently:metric_v2:{v}"
        return v


class DashboardPanelPlot(BaseModel):
    id: PanelID = Field(default_factory=uuid6.uuid7)
    title: str
    subtitle: Optional[str]
    size: Optional[str]
    values: List[PanelMetric]
    plot_params: Dict[str, Any] = Field(default_factory=dict)


class DashboardModel(BaseModel):
    tabs: List[DashboardTabModel]
    panels: List[DashboardPanelPlot]


class ProjectModel(BaseModel):
    id: ProjectID = Field(default_factory=new_id)
    name: str
    description: Optional[str] = None
    org_id: Optional[OrgID] = None
    version: str = "2"


class SnapshotLink(BaseModel):
    snapshot_id: SnapshotID
    dataset_type: str
    dataset_subtype: str


class SnapshotMetadataModel(BaseModel):
    id: SnapshotID
    name: Optional[str]
    metadata: Dict[str, str]
    tags: List[str]
    timestamp: datetime
    links: SnapshotLinks
