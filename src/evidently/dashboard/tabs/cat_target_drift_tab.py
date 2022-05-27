#!/usr/bin/env python
# coding: utf-8
from evidently.dashboard.tabs.base_tab import Tab, Verbose
from evidently.dashboard.widgets.cat_output_drift_widget import CatOutputDriftWidget
from evidently.dashboard.widgets.cat_target_pred_feature_table_widget import CatTargetPredFeatureTable
from evidently.dashboard.widgets.prob_class_pred_distr_widget import ProbClassPredDistrWidget


class CatTargetDriftTab(Tab):
    widgets = [
        (CatOutputDriftWidget("Target Drift"), Verbose.ALWAYS),
        (CatOutputDriftWidget("Prediction Drift", 'prediction'), Verbose.ALWAYS),
        (ProbClassPredDistrWidget("Reference: Probability Distribution"), Verbose.FULL),
        (ProbClassPredDistrWidget("Current: Probability Distribution", 'current'), Verbose.FULL),
        (CatTargetPredFeatureTable("Target (Prediction) Behavior By Feature"), Verbose.FULL),
    ]
