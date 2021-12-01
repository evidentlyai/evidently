#!/usr/bin/env python
# coding: utf-8

import abc
from typing import Optional

import pandas

from evidently.model.widget import BaseWidgetInfo
from evidently.options import OptionsProvider

RED = "#ed0400"
GREY = "#4d4d4d"


class Widget:
    title: str
    wi: Optional[BaseWidgetInfo]
    options_provider: OptionsProvider

    def __init__(self, title: str):
        self.title = title
        self.wi = None

    @abc.abstractmethod
    def calculate(self, reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame, column_mapping, analyzers_results):
        raise NotImplementedError()

    def get_info(self) -> Optional[BaseWidgetInfo]:
        if self.wi:
            return self.wi
        raise ValueError(f"[Widget {self.title}] self.wi is None, no data available (forget to set it in widget?)")

    @abc.abstractmethod
    def analyzers(self):
        return []
