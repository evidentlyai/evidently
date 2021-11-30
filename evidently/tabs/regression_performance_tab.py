#!/usr/bin/env python
# coding: utf-8

from evidently.tabs.base_tab import Tab, Verbose
from evidently.widgets.target_name_widget import TargetNameWidget
from evidently.widgets.reg_quality_metrics_bar_widget import RegQualityMetricsBarWidget
from evidently.widgets.reg_pred_vs_actual_widget import RegPredActualWidget
from evidently.widgets.reg_pred_and_actual_in_time_widget import RegPredActualTimeWidget
from evidently.widgets.reg_error_in_time_widget import RegErrorTimeWidget
from evidently.widgets.reg_abs_perc_error_in_time_widget import RegAbsPercErrorTimeWidget
from evidently.widgets.reg_error_distr_widget import RegErrorDistrWidget
from evidently.widgets.reg_error_normality_widget import RegErrorNormalityWidget
from evidently.widgets.reg_underperform_metrics_widget import RegUnderperformMetricsWidget
from evidently.widgets.reg_colored_pred_vs_actual_widget import RegColoredPredActualWidget
from evidently.widgets.reg_underperform_segments_table_widget import UnderperformSegmTableWidget


class RegressionPerformanceTab(Tab):
    widgets = [
        (TargetNameWidget("Regression Model Performance Report.", kind='regression'), Verbose.ALWAYS),
        (RegQualityMetricsBarWidget("Reference: Model Quality (+/- std)"), Verbose.ALWAYS),
        (RegQualityMetricsBarWidget("Current: Model Quality (+/- std)", dataset='current'), Verbose.ALWAYS),
        (RegPredActualWidget("Reference: Predicted vs Actual"), Verbose.ALWAYS),
        (RegPredActualWidget("Current: Predicted vs Actual", dataset='current'), Verbose.ALWAYS),
        (RegPredActualTimeWidget("Reference: Predicted vs Actual in Time"), Verbose.ALWAYS),
        (RegPredActualTimeWidget("Current: Predicted vs Actual in Time", dataset='current'), Verbose.ALWAYS),
        (RegErrorTimeWidget("Reference: Error (Predicted - Actual)"), Verbose.ALWAYS),
        (RegErrorTimeWidget("Current: Error (Predicted - Actual)", dataset='current'), Verbose.ALWAYS),
        (RegAbsPercErrorTimeWidget("Reference: Absolute Percentage Error"), Verbose.FULL),
        (RegAbsPercErrorTimeWidget("Current: Absolute Percentage Error", dataset='current'), Verbose.FULL),
        (RegErrorDistrWidget("Reference: Error Distribution"), Verbose.ALWAYS),
        (RegErrorDistrWidget("Current: Error Distribution", dataset='current'), Verbose.ALWAYS),
        (RegErrorNormalityWidget("Reference: Error Normality"), Verbose.FULL),
        (RegErrorNormalityWidget("Current: Error Normality", dataset='current'), Verbose.FULL),
        (RegUnderperformMetricsWidget("Reference: Mean Error per Group (+/- std)"), Verbose.FULL),
        (RegUnderperformMetricsWidget("Current: Mean Error per Group (+/- std)", dataset='current'), Verbose.FULL),
        (RegColoredPredActualWidget("Reference: Predicted vs Actual per Group"), Verbose.FULL),
        (RegColoredPredActualWidget("Current: Predicted vs Actual per Group", dataset='current'), Verbose.FULL),
        (UnderperformSegmTableWidget("Error Bias: Mean/Most Common Feature Value per Group"), Verbose.FULL),
    ]
