#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.class_target_name_widget import ClassTargetNameWidget
from evidently.widgets.class_ref_quality_metrics_widget import ClassRefQualityMetricsWidget
from evidently.widgets.class_prod_quality_metrics_widget import ClassProdQualityMetricsWidget
from evidently.widgets.class_ref_class_support_widget import ClassRefClassSupportWidget
from evidently.widgets.class_prod_class_support_widget import ClassProdClassSupportWidget
from evidently.widgets.class_ref_conf_matrix_widget import ClassRefConfMatrixWidget
from evidently.widgets.class_prod_conf_matrix_widget import ClassProdConfMatrixWidget
from evidently.widgets.class_ref_metrics_matrix_widget import ClassRefMetricsMatrixWidget
from evidently.widgets.class_prod_metrics_matrix_widget import ClassProdMetricsMatrixWidget
from evidently.widgets.class_confusion_based_feature_distr_table_widget import ClassConfusionBasedFeatureDistrTable

from evidently.widgets.widget import Widget


class ClassificationPerformanceTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            ClassTargetNameWidget(""),
            ClassRefQualityMetricsWidget("Reference: Model Quality With Macro-average Metrics"),
            ClassProdQualityMetricsWidget("Current: Model Quality With Macro-average Metrics"),
            ClassRefClassSupportWidget("Reference: Class Representation"),
            ClassProdClassSupportWidget("Current: Class Representation"),
            ClassRefConfMatrixWidget("Reference: Confusion Matrix"),
            ClassProdConfMatrixWidget("Current: Confusion Matrix"),
            ClassRefMetricsMatrixWidget("Reference: Quality Metrics by Class"),
            ClassProdMetricsMatrixWidget("Current: Quality Metrics by Class"),
            ClassConfusionBasedFeatureDistrTable("Classification Quality By Feature")
        ]
        return widgets