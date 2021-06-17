#!/usr/bin/env python
# coding: utf-8

import abc
from typing import List, Dict, Type

import pandas

from evidently.analyzers.base_analyzer import Analyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class Tab:
    widgets: List[Widget]

    def __init__(self):
        self.widgets = []

    def analyzers(self) -> List[Type[Analyzer]]:
        self.widgets = self._get_widgets()
        return list(set([analyzer for widget in self.widgets for analyzer in widget.analyzers()]))

    def calculate(self, reference_data: pandas.DataFrame,
                  current_data: pandas.DataFrame,
                  column_mapping: Dict,
                  analyzers_results: Dict):
        self.widgets = self._get_widgets()
        for widget in self.widgets:
            widget.calculate(reference_data, current_data, column_mapping, analyzers_results)

    def info(self) -> List[BaseWidgetInfo]:
        return [w.get_info() for w in self.widgets]

    @abc.abstractmethod
    def _get_widgets(self) -> List[Widget]:
        raise NotImplemented()
