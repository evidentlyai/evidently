#!/usr/bin/env python
# coding: utf-8

from typing import List

from dataclasses import dataclass

from evidently.model.widget import BaseWidgetInfo


@dataclass
class DashboardInfo:
    name: str
    widgets: List[BaseWidgetInfo]
