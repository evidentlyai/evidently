#!/usr/bin/env python
# coding: utf-8

import abc
from typing import List, Dict

import pandas

from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class Tab:
    widgets: List[Widget]

    def __init__(self):
        self.widgets = []

    def calculate(self, reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame,
                  column_mapping: Dict):
        self.widgets = self._get_widgets()
        for widget in self.widgets:
            widget.calculate(reference_data, production_data, column_mapping)

    def info(self) -> List[BaseWidgetInfo]:
        return [w.get_info() for w in self.widgets]

    @abc.abstractmethod
    def _get_widgets(self) -> List[Widget]:
        raise NotImplemented()
