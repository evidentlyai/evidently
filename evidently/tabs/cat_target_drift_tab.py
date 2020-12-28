#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.cat_target_drift_widget import CatTargetDriftWidget
from evidently.widgets.cat_prediction_drift_widget import CatPredictionDriftWidget
from evidently.widgets.cat_target_pred_feature_table_widget import CatTargetPredFeatureTable
from evidently.widgets.widget import Widget


class CatTargetDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            CatTargetDriftWidget("Target Drift"),
            CatPredictionDriftWidget("Prediction Drift"),
            CatTargetPredFeatureTable("Target (Prediction) Behavior By Feature")
        ]
        return widgets
