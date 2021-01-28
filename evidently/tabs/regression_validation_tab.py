#!/usr/bin/env python
# coding: utf-8

from typing import List

from evidently.tabs.base_tab import Tab
from evidently.widgets.reg_ref_quality_metrics_widget import RegRefQualityMetricsWidget
from evidently.widgets.reg_prod_quality_metrics_widget import RegProdQualityMetricsWidget
from evidently.widgets.reg_ref_pred_vs_actual_widget import RegRefPredActualWidget
from evidently.widgets.reg_prod_pred_vs_actual_widget import RegProdPredActualWidget
from evidently.widgets.reg_ref_pred_and_actual_in_time_widget import RegRefPredActualTimeWidget
from evidently.widgets.reg_prod_pred_and_actual_in_time_widget import RegProdPredActualTimeWidget
from evidently.widgets.reg_ref_error_in_time_widget import RegRefErrorTimeWidget
from evidently.widgets.reg_prod_error_in_time_widget import RegProdErrorTimeWidget
from evidently.widgets.reg_ref_abs_perc_error_in_time_widget import RegRefAbsPercErrorTimeWidget
from evidently.widgets.reg_prod_abs_perc_error_in_time_widget import RegProdAbsPercErrorTimeWidget
from evidently.widgets.reg_ref_error_distr_widget import RegRefErrorDistrWidget
from evidently.widgets.reg_prod_error_distr_widget import RegProdErrorDistrWidget
from evidently.widgets.reg_ref_error_normality_widget import RegRefErrorNormalityWidget
from evidently.widgets.reg_prod_error_normality_widget import RegProdErrorNormalityWidget
from evidently.widgets.reg_ref_underperform_metrics_widget import RefUnderperformMetricsWidget
from evidently.widgets.reg_prod_underperform_metrics_widget import ProdUnderperformMetricsWidget
from evidently.widgets.reg_underperform_segments_table_widget import UnderperformSegmTableWidget
from evidently.widgets.widget import Widget


class RegressionValidationTab(Tab):
    def _get_widgets(self) -> List[Widget]:
        
        widgets = [
            RegRefQualityMetricsWidget("Reference Quality"),
            RegProdQualityMetricsWidget("Production Quality"),
            RegRefPredActualWidget("Reference: Predicted vs Actual"),
            RegProdPredActualWidget("Production: Predicted vs Actual"),
            RegRefPredActualTimeWidget("Reference: Predicted vs Actual in Time"),
            RegProdPredActualTimeWidget("Production: Predicted vs Actual in Time"),
            RegRefErrorTimeWidget("Reference: Error (Predicted - Actual)"),
            RegProdErrorTimeWidget("Production: Error (Predicted - Actual)"),
            RegRefAbsPercErrorTimeWidget("Reference: Absolute Percentage Error"),
            RegProdAbsPercErrorTimeWidget("Production: Absolute Percentage Error"),
            RegRefErrorDistrWidget("Reference: Error Distribution"),
            RegProdErrorDistrWidget("Production: Error Distribution"),
            RegRefErrorNormalityWidget("Reference: Error Normality"),
            RegProdErrorNormalityWidget("Production: Error Normality"),
            RefUnderperformMetricsWidget("Error bias"), 
            ProdUnderperformMetricsWidget("Error bias"),
            UnderperformSegmTableWidget("Error bias shift: mean/most common feature values per segment")

        ]
        return widgets