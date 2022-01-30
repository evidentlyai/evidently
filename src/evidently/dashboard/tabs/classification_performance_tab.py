#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab, Verbose
from evidently.dashboard.widgets.target_name_widget import TargetNameWidget
from evidently.dashboard.widgets.class_quality_metrics_bar_widget import ClassQualityMetricsBarWidget
from evidently.dashboard.widgets.class_support_widget import ClassSupportWidget
from evidently.dashboard.widgets.class_conf_matrix_widget import ClassConfMatrixWidget
from evidently.dashboard.widgets.class_metrics_matrix_widget import ClassMetricsMatrixWidget
from evidently.dashboard.widgets.class_confusion_based_feature_distr_table_widget import \
    ClassConfusionBasedFeatureDistrTable


class ClassificationPerformanceTab(Tab):
    widgets = [
        (TargetNameWidget("Classification Model Performance Report.", kind='classification'), Verbose.ALWAYS),
        (ClassQualityMetricsBarWidget("Reference: Model Quality With Macro-average Metrics"), Verbose.ALWAYS),
        (ClassQualityMetricsBarWidget("Current: Model Quality With Macro-average Metrics", 'current'),
         Verbose.ALWAYS),
        (ClassSupportWidget("Reference: Class Representation"), Verbose.ALWAYS),
        (ClassSupportWidget("Current: Class Representation", 'current'), Verbose.ALWAYS),
        (ClassConfMatrixWidget("Reference: Confusion Matrix"), Verbose.FULL),
        (ClassConfMatrixWidget("Current: Confusion Matrix", 'current'), Verbose.FULL),
        (ClassMetricsMatrixWidget("Reference: Quality Metrics by Class"), Verbose.ALWAYS),
        (ClassMetricsMatrixWidget("Current: Quality Metrics by Class", 'current'), Verbose.ALWAYS),
        (ClassConfusionBasedFeatureDistrTable("Classification Quality By Feature"), Verbose.FULL),
    ]
