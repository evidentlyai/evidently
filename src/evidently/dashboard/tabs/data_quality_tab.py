#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab, Verbose
from evidently.dashboard.widgets.data_profile_features_widget import DataQualityFeaturesWidget


class DataQualityTab(Tab):
    widgets = [(DataQualityFeaturesWidget("temp"), Verbose.ALWAYS)]
