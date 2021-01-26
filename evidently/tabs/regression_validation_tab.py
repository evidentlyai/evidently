#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.reg_quality_metrics_widget import RegQualityMetricsWidget
from evidently.widgets.reg_pred_vs_actual_widget import RegPredActualWidget
from evidently.widgets.reg_pred_and_actual_in_time_widget import RegPredActualTimeWidget
from evidently.widgets.reg_error_in_time_widget import RegErrorTimeWidget
from evidently.widgets.reg_abs_perc_error_in_time_widget import RegAbsPercErrorTimeWidget
from evidently.widgets.reg_error_distr_widget import RegErrorDistrWidget
from evidently.widgets.reg_error_normality_widget import RegErrorNormalityWidget
from evidently.widgets.reg_underperform_segments_metrics_widget import UnderperformSegmMetricsWidget
from evidently.widgets.reg_underperform_segments_table_widget import UnderperformSegmTableWidget
from evidently.widgets.widget import Widget


class RegressionValidationTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            RegQualityMetricsWidget(""),
            RegPredActualWidget("Predicted vs Actual"),
            RegPredActualTimeWidget("Predicted vs Actual in Time"),
            RegErrorTimeWidget("Error (Actual - Predicted)"),
            RegAbsPercErrorTimeWidget("Absolute Percentage Error"),
            RegErrorDistrWidget("Error Distribution"),
            RegErrorNormalityWidget("Error Normality"),
            UnderperformSegmMetricsWidget("Error bias shift"), 
            UnderperformSegmTableWidget("Error bias shift: mean/most common feature values per segment")

        ]
        return widgets