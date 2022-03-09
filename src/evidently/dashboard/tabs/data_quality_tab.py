#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab, Verbose
from evidently.dashboard.widgets.data_quality_features_widget import DataQualityFeaturesWidget
from evidently.dashboard.widgets.data_quality_summary import DataQualitySummaryWidget
from evidently.dashboard.widgets.data_quality_correlations import DataQualityCorrelationsWidget


class DataQualityTab(Tab):
    widgets = [
        (DataQualitySummaryWidget("Data Summary"), Verbose.ALWAYS),
        (DataQualityFeaturesWidget("Features"), Verbose.ALWAYS),
        (DataQualityCorrelationsWidget("Correlations"), Verbose.ALWAYS)
    ]
