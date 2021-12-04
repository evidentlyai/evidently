#!/usr/bin/env python
# coding: utf-8

from evidently.tabs.base_tab import Tab, Verbose

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
from evidently.widgets.prob_class_confusion_based_feature_distr_table_widget import \
    ProbClassConfusionBasedFeatureDistrTable


class ProbClassificationPerformanceTab(Tab):
    widgets = [
        (TargetNameWidget("Probabilistic Classification Model Performance Report.", kind='prob_classification'),
         Verbose.ALWAYS),
        (ProbClassQualityMetricBarWidget("Reference: Model Quality With Macro-average Metrics"), Verbose.ALWAYS),
        (ProbClassQualityMetricBarWidget("Current: Model Quality With Macro-average Metrics", 'current'),
         Verbose.ALWAYS),
        (ProbClassSupportWidget("Reference: Class Representation"), Verbose.ALWAYS),
        (ProbClassSupportWidget("Current: Class Representation", 'current'), Verbose.ALWAYS),
        (ProbClassConfMatrixWidget("Reference: Confusion Matrix"), Verbose.FULL),
        (ProbClassConfMatrixWidget("Current: Confusion Matrix", 'current'), Verbose.FULL),
        (ProbClassMetricsMatrixWidget("Reference: Quality Metrics by Class"), Verbose.ALWAYS),
        (ProbClassMetricsMatrixWidget("Current: Quality Metrics by Class", 'current'), Verbose.ALWAYS),
        (ProbClassPredictionCloudWidget("Reference: Class Separation Quality"), Verbose.FULL),
        (ProbClassPredictionCloudWidget("Current: Class Separation Quality", 'current'), Verbose.FULL),
        (ProbClassPredDistrWidget("Reference: Probability Distribution"), Verbose.FULL),
        (ProbClassPredDistrWidget("Current: Probability Distribution", 'current'), Verbose.FULL),
        (ProbClassRocCurveWidget("Reference: ROC Curve"), Verbose.FULL),
        (ProbClassRocCurveWidget("Current: ROC Curve", 'current'), Verbose.FULL),
        (ProbClassPRCurveWidget("Reference: Precision-Recall Curve"), Verbose.FULL),
        (ProbClassPRCurveWidget("Current: Precision-Recall Curve", 'current'), Verbose.FULL),
        (ProbClassPRTableWidget("Reference: Precision-Recall Table"), Verbose.FULL),
        (ProbClassPRTableWidget("Current: Precision-Recall Table", 'current'), Verbose.FULL),
        (ProbClassConfusionBasedFeatureDistrTable("Classification Quality By Feature"), Verbose.FULL),
    ]
