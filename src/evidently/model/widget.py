#!/usr/bin/env python
# coding: utf-8
# pylint: disable=invalid-name

from dataclasses import dataclass
from typing import Any, Optional, Iterable


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
    details: str = ""
    alertsPosition: Optional[str] = None
    alertStats: Optional[AlertStats] = None
    params: Any = None
    insights: Iterable[Insight] = ()
    additionalGraphs: Iterable[AdditionalGraphInfo] = ()
    alerts: Iterable[Alert] = ()
    tabs: Iterable["TabInfo"] = ()


@dataclass
class TabInfo:
    id: str
    title: str
    widget: BaseWidgetInfo
