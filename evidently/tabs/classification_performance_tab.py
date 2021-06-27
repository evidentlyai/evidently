#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.target_name_widget import TargetNameWidget
from evidently.widgets.class_quality_metrics_bar_widget import ClassQualityMetricsBarWidget
from evidently.widgets.class_support_widget import ClassSupportWidget
from evidently.widgets.class_conf_matrix_widget import ClassConfMatrixWidget
from evidently.widgets.class_metrics_matrix_widget import ClassMetricsMatrixWidget
from evidently.widgets.class_confusion_based_feature_distr_table_widget import ClassConfusionBasedFeatureDistrTable

from evidently.widgets.widget import Widget


class ClassificationPerformanceTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            TargetNameWidget("Classification Model Performance Report.", kind = 'classification'),
            ClassQualityMetricsBarWidget("Reference: Model Quality With Macro-average Metrics"),
            ClassQualityMetricsBarWidget("Current: Model Quality With Macro-average Metrics", 'current'),
            ClassSupportWidget("Reference: Class Representation"),
            ClassSupportWidget("Current: Class Representation", 'current'),
            ClassConfMatrixWidget("Reference: Confusion Matrix"),
            ClassConfMatrixWidget("Current: Confusion Matrix", 'current'),
            ClassMetricsMatrixWidget("Reference: Quality Metrics by Class"),
            ClassMetricsMatrixWidget("Current: Quality Metrics by Class", 'current'),
            ClassConfusionBasedFeatureDistrTable("Classification Quality By Feature")
        ]
        return widgets