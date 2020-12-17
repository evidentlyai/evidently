#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.regression_output_drift_widget import RegOutputDriftWidget
from evidently.widgets.regression_output_corr_widget import RegOutputCorrWidget
from evidently.widgets.regression_output_values_widget import RegOutputValuesWidget
from evidently.widgets.regression_target_drift_widget import RegTargetDriftWidget
from evidently.widgets.widget import Widget


class RegressionOutputDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            RegOutputDriftWidget("Prediction Drift"),
            RegOutputCorrWidget("Prediction Correlations"),
            RegOutputValuesWidget("Prediction Values"),
            RegTargetDriftWidget("Target Drift"),
        ]
        return widgets
