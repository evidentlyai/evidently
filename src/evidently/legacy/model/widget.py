#!/usr/bin/env python
# coding: utf-8
# pylint: disable=invalid-name
from enum import Enum
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import Fingerprint


class TriggeredAlertStats(BaseModel):
    period: int
    last_24h: int


class AlertStats(BaseModel):
    """
    Attributes:
        active: Number of active alerts.
        eggs: An integer count of the eggs we have laid.
    """

    active: int
    triggered: TriggeredAlertStats


class Insight(BaseModel):
    """
    Attributes:
        title: Insight title
        severity: Severity level for insight information (one of 'info', 'warning', 'error', 'success')
        text: Insidght information
    """

    title: str
    severity: str
    text: str


class Alert(BaseModel):
    value: Union[str, int, float]
    state: str
    text: str
    longText: str


class AdditionalGraphInfo(BaseModel):
    class Config:
        extra = "forbid"

    id: str
    params: dict


class PlotlyGraphInfo(BaseModel):
    data: dict
    layout: dict
    id: str = Field(default_factory=lambda: str(uuid6.uuid7()))


class WidgetType(Enum):
    COUNTER = "counter"
    TABLE = "table"
    BIG_TABLE = "big_table"
    GROUP = "group"
    BIG_GRAPH = "big_graph"
    RICH_DATA = "rich_data"
    TABBED_GRAPH = "tabbed_graph"
    TABS = "tabs"


# @dataclass
class BaseWidgetInfo(BaseModel):
    class Config:
        smart_union = True

    type: str
    title: str
    size: int
    id: str = Field(default_factory=lambda: str(uuid6.uuid7()))
    details: str = ""
    alertsPosition: Optional[str] = None
    alertStats: Optional[AlertStats] = None
    params: Any = None
    insights: List[Insight] = Field(default_factory=list)
    additionalGraphs: List[Union[AdditionalGraphInfo, "BaseWidgetInfo", PlotlyGraphInfo]] = Field(default_factory=list)
    alerts: List[Alert] = Field(default_factory=list)
    tabs: List["TabInfo"] = Field(default_factory=list)
    widgets: List["BaseWidgetInfo"] = Field(default_factory=list)
    pageSize: int = 5
    source_fingerprint: Optional[Fingerprint] = None
    linked_metrics: Optional[List[Fingerprint]] = None

    def get_additional_graphs(
        self,
    ) -> List[Union[AdditionalGraphInfo, PlotlyGraphInfo, "BaseWidgetInfo"]]:
        return list(self.additionalGraphs) + [
            graph for widget in self.widgets for graph in widget.get_additional_graphs()
        ]


def link_metric(
    widgets: Union[BaseWidgetInfo, Iterable[BaseWidgetInfo], None],
    source: Union[EvidentlyBaseModel, Fingerprint],
):
    if widgets is None:
        return
    fingerprint = source if isinstance(source, Fingerprint) else source.get_fingerprint()
    widgets = [widgets] if isinstance(widgets, BaseWidgetInfo) else widgets
    for widget in widgets:
        if widget.linked_metrics is None:
            widget.linked_metrics = [fingerprint]
        else:
            widget.linked_metrics.append(fingerprint)


def set_source_fingerprint(
    widgets: Union[BaseWidgetInfo, Iterable[BaseWidgetInfo]], source: Union[EvidentlyBaseModel, Fingerprint]
):
    fingerprint = source if isinstance(source, Fingerprint) else source.get_fingerprint()
    widgets = [widgets] if isinstance(widgets, BaseWidgetInfo) else widgets
    for w in widgets:
        w.source_fingerprint = fingerprint
    link_metric(widgets, source)


class TabInfo(BaseModel):
    id: str
    title: str
    widget: BaseWidgetInfo


BaseWidgetInfo.update_forward_refs()
