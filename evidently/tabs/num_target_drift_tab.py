#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.num_output_drift_widget import NumOutputDriftWidget
from evidently.widgets.num_output_corr_widget import NumOutputCorrWidget
from evidently.widgets.num_output_values_widget import NumOutputValuesWidget
from evidently.widgets.num_target_pred_feature_table_widget import NumTargetPredFeatureTable
from evidently.widgets.widget import Widget


class NumTargetDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            NumOutputDriftWidget("Target Drift"),
            NumOutputCorrWidget("Target Correlations"),
            NumOutputValuesWidget("Target Values"),
            NumOutputDriftWidget("Prediction Drift", "prediction"),
            NumOutputCorrWidget("Prediction Correlations", "prediction"),
            NumOutputValuesWidget("Prediction Values", "prediction"),
            NumTargetPredFeatureTable("Target (Prediction) Behavior By Feature")
        ]
        return widgets
