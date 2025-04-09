import abc
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.legacy.core import new_id
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


class ProjectDashboard:
    @property
    @abc.abstractmethod
    def project_id(self) -> ProjectID:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tab(self, tab: str):
        raise NotImplementedError

    @abstractmethod
    def delete_tab(self, tab: str):
        raise NotImplementedError

    @abstractmethod
    def add_panel(self, panel: DashboardPanelPlot, tab: Optional[str], create_if_not_exists: bool = True):
        raise NotImplementedError

    @abstractmethod
    def delete_panel(self, panel: str, tab: str):
        raise NotImplementedError

    @abstractmethod
    def model(self) -> DashboardModel:
        raise NotImplementedError

    def __repr__(self):
        _model = self.model()
        return f"Dashboard for project {self.project_id}\n  " + "\n  ".join(
            f"Tab '{tab.title}' ({tab.id})\n    "
            + "\n    ".join(
                f"Panel '{p.title}' ({p.id})\n      "
                + "\n      ".join(
                    f"Series metric_type={s.metric}"
                    + f" (tags={s.tags},metadata={s.metadata})"
                    + f" labels={s.metric_labels}"
                    for s in p.values
                )
                for p in _model.panels
                if p.id in tab.panels
            )
            for tab in _model.tabs
        )


class SnapshotLink(BaseModel):
    snapshot_id: SnapshotID
    dataset_type: str
    dataset_subtype: str
