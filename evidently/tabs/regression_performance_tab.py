#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.target_name_widget import TargetNameWidget
from evidently.widgets.reg_quality_metrics_bar_widget import RegQualityMetricsBarWidget
from evidently.widgets.reg_pred_vs_actual_widget import RegPredActualWidget
from evidently.widgets.reg_pred_and_actual_in_time_widget import RegPredActualTimeWidget
from evidently.widgets.reg_error_in_time_widget import RegErrorTimeWidget
from evidently.widgets.reg_abs_perc_error_in_time_widget import RegAbsPercErrorTimeWidget
from evidently.widgets.reg_error_distr_widget import RegErrorDistrWidget
from evidently.widgets.reg_error_normality_widget import RegErrorNormalityWidget
from evidently.widgets.reg_underperform_metrics_widget import RegUnderperformMetricsWidget
from evidently.widgets.reg_colored_pred_vs_actual_widget import RegColoredPredActualWidget
from evidently.widgets.reg_underperform_segments_table_widget import UnderperformSegmTableWidget
from evidently.widgets.widget import Widget


class RegressionPerformanceTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            TargetNameWidget("Regression Model Performance Report.", kind='regression'),
            RegQualityMetricsBarWidget("Reference: Model Quality (+/- std)"),
            RegQualityMetricsBarWidget("Current: Model Quality (+/- std)", dataset='current'),
            RegPredActualWidget("Reference: Predicted vs Actual"),
            RegPredActualWidget("Current: Predicted vs Actual", dataset='current'),
            RegPredActualTimeWidget("Reference: Predicted vs Actual in Time"),
            RegPredActualTimeWidget("Current: Predicted vs Actual in Time", dataset='current'),
            RegErrorTimeWidget("Reference: Error (Predicted - Actual)"),
            RegErrorTimeWidget("Current: Error (Predicted - Actual)", dataset='current'),
            RegAbsPercErrorTimeWidget("Reference: Absolute Percentage Error"),
            RegAbsPercErrorTimeWidget("Current: Absolute Percentage Error", dataset='current'),
            RegErrorDistrWidget("Reference: Error Distribution"),
            RegErrorDistrWidget("Current: Error Distribution", dataset='current'),
            RegErrorNormalityWidget("Reference: Error Normality"),
            RegErrorNormalityWidget("Current: Error Normality", dataset='current'),
            RegUnderperformMetricsWidget("Reference: Mean Error per Group (+/- std)"), 
            RegUnderperformMetricsWidget("Current: Mean Error per Group (+/- std)", dataset='current'),
            RegColoredPredActualWidget("Reference: Predicted vs Actual per Group"),
            RegColoredPredActualWidget("Current: Predicted vs Actual per Group", dataset='current'),
            UnderperformSegmTableWidget("Error Bias: Mean/Most Common Feature Value per Group")

        ]
        return widgets