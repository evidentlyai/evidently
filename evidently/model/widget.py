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
    params: Any
    alertsPosition: str
    alertStats: AlertStats
    alerts: List[Alert]
    insights: List[Insight]
    additionalGraphs: List[AdditionalGraphInfo]


