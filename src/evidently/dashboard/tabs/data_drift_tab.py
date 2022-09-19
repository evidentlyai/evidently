#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab
from evidently.dashboard.tabs.base_tab import Verbose
from evidently.dashboard.widgets.data_drift_table_widget import DataDriftTableWidget


class DataDriftTab(Tab):
    widgets = [(DataDriftTableWidget("Data Drift"), Verbose.ALWAYS)]
