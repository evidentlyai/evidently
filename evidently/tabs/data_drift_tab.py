#!/usr/bin/env python
# coding: utf-8
from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.data_drift_table_widget import DataDriftTableWidget, DataDriftOptions
from evidently.widgets.widget import Widget


class DataDriftTab(Tab):
    def __init__(self, options: DataDriftOptions = None):
        super().__init__()
        self.options = options if options else DataDriftOptions()

    def _get_widgets(self) -> List[Widget]:
        return [
            DataDriftTableWidget("Data Drift", options=self.options)
        ]
