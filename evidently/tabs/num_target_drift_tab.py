#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.num_target_drift_widget import NumTargetDriftWidget
from evidently.widgets.num_prediction_drift_widget import NumPredictionDriftWidget 
from evidently.widgets.num_target_corr_widget import NumTargetCorrWidget
from evidently.widgets.num_prediction_corr_widget import NumPredictionCorrWidget
from evidently.widgets.num_target_values_widget import NumTargetValuesWidget
from evidently.widgets.num_prediction_values_widget import NumPredictionValuesWidget
from evidently.widgets.num_target_pred_feature_table_widget import NumTargetPredFeatureTable
from evidently.widgets.widget import Widget


class NumTargetDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            NumTargetDriftWidget("Target Drift"),
            NumTargetCorrWidget("Target Correlations"),
            NumTargetValuesWidget("Target Values"),
            NumPredictionDriftWidget("Prediction Drift"),
            NumPredictionCorrWidget("Prediction Correlations"),
            NumPredictionValuesWidget("Prediction Values"),
            NumTargetPredFeatureTable("Target (Prediction) Behavior By Feature")
        ]
        return widgets
