#!/usr/bin/env python
# coding: utf-8

import abc
from typing import List, Dict, Type

import pandas

from evidently.analyzes.base_analyze import Analyze
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class Tab:
    widgets: List[Widget]

    def __init__(self):
        self.widgets = []

    def analyzes(self) -> List[Type[Analyze]]:
        return list(set([analyse for widget in self.widgets for analyse in widget.analyzes()]))

    def calculate(self, reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame,
                  column_mapping: Dict,
                  analyzes_results: Dict):
        self.widgets = self._get_widgets()
        for widget in self.widgets:
            widget.calculate(reference_data, production_data, column_mapping, analyzes_results)

    def info(self) -> List[BaseWidgetInfo]:
        return [w.get_info() for w in self.widgets]

    @abc.abstractmethod
    def _get_widgets(self) -> List[Widget]:
        raise NotImplemented()
