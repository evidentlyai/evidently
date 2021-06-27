#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab

from evidently.widgets.target_name_widget import TargetNameWidget
from evidently.widgets.prob_class_quality_metrics_bar_widget import ProbClassQualityMetricBarWidget
from evidently.widgets.prob_class_support_widget import ProbClassSupportWidget
from evidently.widgets.prob_class_conf_matrix_widget import ProbClassConfMatrixWidget
from evidently.widgets.prob_class_metrics_matrix_widget import ProbClassMetricsMatrixWidget
from evidently.widgets.prob_class_prediction_cloud_widget import ProbClassPredictionCloudWidget
from evidently.widgets.prob_class_pred_distr_widget import ProbClassPredDistrWidget
from evidently.widgets.prob_class_roc_curve_widget import ProbClassRocCurveWidget
from evidently.widgets.prob_class_pr_curve_widget import ProbClassPRCurveWidget
from evidently.widgets.prob_class_pr_table_widget import ProbClassPRTableWidget
from evidently.widgets.prob_class_confusion_based_feature_distr_table_widget import ProbClassConfusionBasedFeatureDistrTable

from evidently.widgets.widget import Widget


class ProbClassificationPerformanceTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            TargetNameWidget("Probabilistic Classification Model Performance Report.", kind = 'prob_classification'),
            ProbClassQualityMetricBarWidget("Reference: Model Quality With Macro-average Metrics"),
            ProbClassQualityMetricBarWidget("Current: Model Quality With Macro-average Metrics", 'current'),
            ProbClassSupportWidget("Reference: Class Representation"),
            ProbClassSupportWidget("Current: Class Representation", 'current'),
            ProbClassConfMatrixWidget("Reference: Confusion Matrix"),
            ProbClassConfMatrixWidget("Current: Confusion Matrix", 'current'),
            ProbClassMetricsMatrixWidget("Reference: Quality Metrics by Class"),
            ProbClassMetricsMatrixWidget("Current: Quality Metrics by Class", 'current'),
            ProbClassPredictionCloudWidget("Reference: Class Separation Quality"),
            ProbClassPredictionCloudWidget("Current: Class Separation Quality", 'current'),
            ProbClassPredDistrWidget("Reference: Probability Distribution"),
            ProbClassPredDistrWidget("Current: Probability Distribution", 'current'),            
            ProbClassRocCurveWidget("Reference: ROC Curve"),
            ProbClassRocCurveWidget("Current: ROC Curve", 'current'),
            ProbClassPRCurveWidget("Reference: Precision-Recall Curve"),
            ProbClassPRCurveWidget("Current: Precision-Recall Curve", 'current'),
            ProbClassPRTableWidget("Reference: Precision-Recall Table"),
            ProbClassPRTableWidget("Current: Precision-Recall Table", 'current'),
            ProbClassConfusionBasedFeatureDistrTable("Classification Quality By Feature")
        ]
        return widgets