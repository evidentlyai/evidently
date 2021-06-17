#!/usr/bin/env python
# coding: utf-8

import abc

import pandas

from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class RawWidget(Widget):
    @abc.abstractmethod
    def calculate(self, reference_data: pandas.DataFrame, current_data: pandas.DataFrame, column_mapping,
                  analyzes_results):
        raise NotImplemented()

    def analyzers(self):
        return []

    def __init__(self, wi: BaseWidgetInfo):
        super().__init__()
        self.wi = wi

    def get_info(self) -> BaseWidgetInfo:
        return self.wi
