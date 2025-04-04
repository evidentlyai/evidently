#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently._pydantic_compat import BaseModel
from evidently.legacy.model.widget import BaseWidgetInfo


class DashboardInfo(BaseModel):
    name: str
    widgets: List[BaseWidgetInfo]
