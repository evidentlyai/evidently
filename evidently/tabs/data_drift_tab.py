#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.data_drift_table_widget import DataDriftTableWidget
from evidently.widgets.widget import Widget


class DataDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        return [
            DataDriftTableWidget("Data Drift")
        ]
