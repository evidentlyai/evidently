#!/usr/bin/env python
# coding: utf-8
from evidently.tabs.base_tab import Tab, Verbose
from evidently.widgets.data_drift_table_widget import DataDriftTableWidget


class DataDriftTab(Tab):
    widgets = [(DataDriftTableWidget("Data Drift"), Verbose.ALWAYS)]
