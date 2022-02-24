#!/usr/bin/env python
# coding: utf-8
import abc
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider

RED = "#ed0400"
GREY = "#4d4d4d"
COLOR_DISCRETE_SEQUENCE = ['#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4']


class Widget:
    title: str
    wi: Optional[BaseWidgetInfo]
    options_provider: OptionsProvider

    def __init__(self, title: str):
        self.title = title
        self.wi = None

    @abc.abstractmethod
    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        raise NotImplementedError()

    @abc.abstractmethod
    def analyzers(self):
        return []
