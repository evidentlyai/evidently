#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab
from evidently.dashboard.tabs.base_tab import Verbose
from evidently.dashboard.widgets.data_quality_correlations import DataQualityCorrelationsWidget
from evidently.dashboard.widgets.data_quality_features_widget import DataQualityFeaturesWidget
from evidently.dashboard.widgets.data_quality_summary_widget import DataQualitySummaryWidget


class DataQualityTab(Tab):
    widgets = [
        (DataQualitySummaryWidget("Data Summary"), Verbose.ALWAYS),
        (DataQualityFeaturesWidget("Features"), Verbose.ALWAYS),
        (DataQualityCorrelationsWidget("Correlations"), Verbose.FULL),
    ]
