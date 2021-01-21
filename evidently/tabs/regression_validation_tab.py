#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.reg_pred_vs_actual_widget import RegPredActualWidget
from evidently.widgets.reg_pred_and_actual_in_time_widget import RegPredActualTimeWidget
from evidently.widgets.reg_error_in_time_widget import RegErrorTimeWidget
from evidently.widgets.reg_abs_perc_error_in_time_widget import RegAbsPercErrorTimeWidget
from evidently.widgets.reg_error_distr_widget import RegErrorDistrWidget
from evidently.widgets.reg_error_normality_widget import RegErrorNormalityWidget
from evidently.widgets.widget import Widget


class RegressionValidationTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            RegPredActualWidget("Predicted vs Actual"),
            RegPredActualTimeWidget("Predicted vs Actual in Time"),
            RegErrorTimeWidget("Error (Actual - Predicted)"),
            RegAbsPercErrorTimeWidget("Absolute Percentage Error"),
            RegErrorDistrWidget("Error Distribution"),
            RegErrorNormalityWidget("Error Normality")

        ]
        return widgets