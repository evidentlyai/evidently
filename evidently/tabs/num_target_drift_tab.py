#!/usr/bin/env python
# coding: utf-8
from evidently.tabs.base_tab import Tab, Verbose
from evidently.widgets.num_output_drift_widget import NumOutputDriftWidget
from evidently.widgets.num_output_corr_widget import NumOutputCorrWidget
from evidently.widgets.num_output_values_widget import NumOutputValuesWidget
from evidently.widgets.num_target_pred_feature_table_widget import NumTargetPredFeatureTable


class NumTargetDriftTab(Tab):
    widgets = [
        (NumOutputDriftWidget("Target Drift"), Verbose.ALWAYS),
        (NumOutputCorrWidget("Target Correlations"), Verbose.ALWAYS),
        (NumOutputValuesWidget("Target Values"), Verbose.ALWAYS),
        (NumOutputDriftWidget("Prediction Drift", "prediction"), Verbose.ALWAYS),
        (NumOutputCorrWidget("Prediction Correlations", "prediction"), Verbose.ALWAYS),
        (NumOutputValuesWidget("Prediction Values", "prediction"), Verbose.ALWAYS),
        (NumTargetPredFeatureTable("Target (Prediction) Behavior By Feature"), Verbose.ALWAYS),
    ]
