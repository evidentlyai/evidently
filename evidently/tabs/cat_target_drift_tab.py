#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.cat_output_drift_widget import CatOutputDriftWidget
from evidently.widgets.cat_target_pred_feature_table_widget import CatTargetPredFeatureTable
from evidently.widgets.widget import Widget


class CatTargetDriftTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            CatOutputDriftWidget("Target Drift"),
            CatOutputDriftWidget("Prediction Drift", 'prediction'),
            CatTargetPredFeatureTable("Target (Prediction) Behavior By Feature")
        ]
        return widgets
