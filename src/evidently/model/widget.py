#!/usr/bin/env python
# coding: utf-8
# pylint: disable=invalid-name

from dataclasses import dataclass
from typing import Any, Optional, Iterable, Union


@dataclass()
class TriggeredAlertStats:
    period: int
    last_24h: int


@dataclass
class AlertStats:
    """
    Attributes:
        active: Number of active alerts.
        eggs: An integer count of the eggs we have laid.
    """

    active: int
    triggered: TriggeredAlertStats


@dataclass
class Insight:
    """
    Attributes:
        title: Insight title
        severity: Severity level for insight information (one of 'info', 'warning', 'error', 'success')
        text: Insidght information
    """
    title: str
    severity: str
    text: str


@dataclass
class Alert:
    value: Union[str, int, float]
    state: str
    text: str
    longText: str


@dataclass
class AdditionalGraphInfo:
    id: str
    params: Any


@dataclass
class BaseWidgetInfo:
    type: str
    title: str
    size: int
    details: str = ""
    alertsPosition: Optional[str] = None
    alertStats: Optional[AlertStats] = None
    params: Any = None
    insights: Iterable[Insight] = ()
    additionalGraphs: Iterable[AdditionalGraphInfo] = ()
    alerts: Iterable[Alert] = ()
    tabs: Iterable["TabInfo"] = ()
    widgets: Iterable["BaseWidgetInfo"] = ()
    pageSize: int = 5

    def get_additional_graphs(self) -> Iterable[AdditionalGraphInfo]:
        return list(self.additionalGraphs) + [graph for widget in self.widgets for graph in widget.additionalGraphs]


@dataclass
class TabInfo:
    id: str
    title: str
    widget: BaseWidgetInfo
