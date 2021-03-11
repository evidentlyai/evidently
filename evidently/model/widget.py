#!/usr/bin/env python
# coding: utf-8

from dataclasses import dataclass
from typing import List, Any


@dataclass
class AlertStats:
    pass


@dataclass
class Insight:
    pass


@dataclass
class Alert:
    pass


@dataclass
class AdditionalGraphInfo:
    id: str
    params: Any


@dataclass
class BaseWidgetInfo:
    type: str
    title: str
    size: int
    details: str
    alertsPosition: str = None
    alertStats: AlertStats = None
    params: Any = None
    insights: List[Insight] = ()
    additionalGraphs: List[AdditionalGraphInfo] = ()
    alerts: List[Alert] = ()
    tabs: List["TabInfo"] = ()


@dataclass
class TabInfo:
    id: str
    title: str
    widget: BaseWidgetInfo
