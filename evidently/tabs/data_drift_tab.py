#!/usr/bin/env python
# coding: utf-8

from typing import List, Type

from evidently.analyzers.base_analyzer import Analyzer
from evidently.tabs.base_tab import Tab
from evidently.widgets.data_drift_table_widget import DataDriftTableWidget
from evidently.widgets.widget import Widget


class DataDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        return [
            DataDriftTableWidget("Data Drift")
        ]

#    def get_analyzers(self) -> List[Type[Analyzer]]:
#        return [analyzer for widget in self._get_widgets() for analyzer in widget.analyzers()]
