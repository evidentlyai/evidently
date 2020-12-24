#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.big_drift_table_widget import BigDriftTableWidget
from evidently.widgets.widget import Widget


class DriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        return [
            BigDriftTableWidget("Data Drift")
        ]