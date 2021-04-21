#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.prob_class_target_name_widget import ProbClassTargetNameWidget
from evidently.widgets.prob_class_ref_quality_metrics_widget import ProbClassRefQualityMetricsWidget
from evidently.widgets.prob_class_prod_quality_metrics_widget import ProbClassProdQualityMetricsWidget
from evidently.widgets.prob_class_ref_class_support_widget import ProbClassRefClassSupportWidget
from evidently.widgets.prob_class_prod_class_support_widget import ProbClassProdClassSupportWidget
from evidently.widgets.prob_class_ref_conf_matrix_widget import ProbClassRefConfMatrixWidget
from evidently.widgets.prob_class_prod_conf_matrix_widget import ProbClassProdConfMatrixWidget
from evidently.widgets.prob_class_ref_metrics_matrix_widget import ProbClassRefMetricsMatrixWidget
from evidently.widgets.prob_class_prod_metrics_matrix_widget import ProbClassProdMetricsMatrixWidget
from evidently.widgets.prob_class_ref_prediction_cloud_widget import ProbClassRefPredictionCloudWidget
from evidently.widgets.prob_class_prod_prediction_cloud_widget import ProbClassProdPredictionCloudWidget
from evidently.widgets.prob_class_ref_pred_distr_widget import ProbClassRefPredDistrWidget
from evidently.widgets.prob_class_prod_pred_distr_widget import ProbClassProdPredDistrWidget
from evidently.widgets.prob_class_ref_roc_curve_widget import ProbClassRefRocCurveWidget
from evidently.widgets.prob_class_prod_roc_curve_widget import ProbClassProdRocCurveWidget
from evidently.widgets.prob_class_ref_pr_curve_widget import ProbClassRefPRCurveWidget
from evidently.widgets.prob_class_prod_pr_curve_widget import ProbClassProdPRCurveWidget
from evidently.widgets.prob_class_ref_pr_table_widget import ProbClassRefPRTableWidget
from evidently.widgets.prob_class_prod_pr_table_widget import ProbClassProdPRTableWidget
from evidently.widgets.prob_class_confusion_based_feature_distr_table_widget import ProbClassConfusionBasedFeatureDistrTable

from evidently.widgets.widget import Widget


class ProbClassificationPerformanceTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            ProbClassTargetNameWidget(""),
            ProbClassRefQualityMetricsWidget("Reference: Model Quality With Macro-average Metrics"),
            ProbClassProdQualityMetricsWidget("Current: Model Quality With Macro-average Metrics"),
            ProbClassRefClassSupportWidget("Reference: Class Representation"),
            ProbClassProdClassSupportWidget("Current: Class Representation"),
            ProbClassRefConfMatrixWidget("Reference: Confusion Matrix"),
            ProbClassProdConfMatrixWidget("Current: Confusion Matrix"),
            ProbClassRefMetricsMatrixWidget("Reference: Quality Metrics by Class"),
            ProbClassProdMetricsMatrixWidget("Current: Quality Metrics by Class"),
            ProbClassRefPredictionCloudWidget("Reference: Class Separation Quality"),
            ProbClassProdPredictionCloudWidget("Current: Class Separation Quality"),
            ProbClassRefPredDistrWidget("Reference: Probability Distribution"),
            ProbClassProdPredDistrWidget("Current: Probability Distribution"),            
            ProbClassRefRocCurveWidget("Reference: ROC Curve"),
            ProbClassProdRocCurveWidget("Current: ROC Curve"),
            ProbClassRefPRCurveWidget("Reference: Precision-Recall Curve"),
            ProbClassProdPRCurveWidget("Current: Precision-Recall Curve"),
            ProbClassRefPRTableWidget("Reference: Precision-Recall Table"),
            ProbClassProdPRTableWidget("Current: Precision-Recall Table"),
            ProbClassConfusionBasedFeatureDistrTable("Classification Quality By Feature")
        ]
        return widgets