from cmath import log
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from visions import logging

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric
from evidently.v2.metrics.utils import make_target_bins_for_reg_plots, make_hist_for_cat_plot, apply_func_to_binned_data
import logging

@dataclass
class RegressionPerformanceMetricsResults:
    r2_score: float
    rmse: float
    rmse_default: float
    mean_error: float
    me_distr: List[Tuple[object, float]]
    ref_me_distr: Optional[List[Tuple[object, float]]]
    mean_abs_error: float
    mean_abs_error_default: float
    mean_abs_perc_error: float
    mean_abs_perc_error_default: float
    abs_error_max: float
    error_std: float
    abs_error_std: float
    abs_perc_error_std: float
    error_normality: dict
    underperformance: dict
    hist_for_plot: Dict[str, pd.Series]
    vals_for_plots: Dict[str, Dict[str, pd.Series]]
    error_bias: Optional[dict] = None
    mean_abs_error_ref: float = None
    mean_abs_perc_error_ref: float = None
    rmse_ref: float = None
    r2_score_ref: float = None
    


class RegressionPerformanceMetrics(Metric[RegressionPerformanceMetricsResults]):
    def __init__(self):
        self.analyzer = RegressionPerformanceAnalyzer()

    def calculate(self, data: InputData, metrics: dict) -> RegressionPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        if data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data,
                current_data=None,
                column_mapping=data.column_mapping
            )
        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data,
                current_data=data.current_data,
                column_mapping=data.column_mapping
            )

        r2_score_value = r2_score(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=data.current_data[data.column_mapping.prediction]
        )
        rmse_score_value = mean_squared_error(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=data.current_data[data.column_mapping.prediction]
        )

        # mae default values
        mean_abs_error_ref = None
        if data.reference_data is not None:
            mean_abs_error_ref = mean_absolute_error(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction]
            )
        dummy_preds = data.current_data[data.column_mapping.target].median()
        mean_abs_error_default = mean_absolute_error(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        # rmse default values
        rmse_ref = None
        if data.reference_data is not None:
            rmse_ref = mean_squared_error(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction]
            )
        dummy_preds = data.current_data[data.column_mapping.target].mean()
        rmse_default = mean_squared_error(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        # mape default values
        mean_abs_perc_error_ref = None
        if data.reference_data is not None:
            mean_abs_perc_error_ref = mean_absolute_percentage_error(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction]
            )
        # optimal constant for mape
        s = data.current_data[data.column_mapping.target]
        inv_y = 1 / s[s != 0].values
        w = inv_y / sum(inv_y)
        idxs = np.argsort(w)
        sorted_w = w[idxs]
        sorted_w_cumsum = np.cumsum(sorted_w)
        idx = np.where(sorted_w_cumsum > 0.5)[0][0]
        pos = idxs[idx]
        dummy_preds = s[s != 0].values[pos]

        mean_abs_perc_error_default = mean_absolute_percentage_error(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        #  r2_score default values
        r2_score_ref = None
        if data.reference_data is not None:
            r2_score_ref = r2_score(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction]
            )

        # visualisation

        df_target_binned = make_target_bins_for_reg_plots(data.current_data, data.column_mapping.target, 
                                                       data.column_mapping.prediction, data.reference_data)
        curr_target_bins = df_target_binned.loc[df_target_binned.data=='curr', 'target_binned']
        ref_target_bins = None
        if data.reference_data is not None:
            ref_target_bins = df_target_binned.loc[df_target_binned.data=='ref', 'target_binned']
        hist_for_plot = make_hist_for_cat_plot(curr_target_bins, ref_target_bins)

        vals_for_plots = {}
        if data.reference_data is None:
            is_ref_data = False
        else:
            is_ref_data = True
        
        for name, func in zip(
            ['r2_score', 'rmse', 'mean_abs_error', 'mean_abs_perc_error'], 
            [r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error]):
            vals_for_plots[name] = apply_func_to_binned_data(df_target_binned, func, data.column_mapping.target, 
                                                             data.column_mapping.prediction, is_ref_data)

        
        me_distr = _me_distr(data.current_data, data.column_mapping)
        ref_me_distr = _me_distr(data.reference_data, data.column_mapping)\
            if data.reference_data is not None else None

        return RegressionPerformanceMetricsResults(
            r2_score=r2_score_value,
            rmse=rmse_score_value,
            rmse_default=rmse_default,
            mean_error=analyzer_results.reference_metrics.mean_error,
            me_distr=me_distr,
            ref_me_distr=ref_me_distr,
            mean_abs_error=analyzer_results.current_metrics.mean_abs_error,
            mean_abs_error_default=mean_abs_error_default,
            mean_abs_perc_error=analyzer_results.reference_metrics.mean_abs_perc_error,
            mean_abs_perc_error_default=mean_abs_perc_error_default,
            abs_error_max=analyzer_results.reference_metrics.abs_error_max,
            error_std=analyzer_results.reference_metrics.error_std,
            abs_error_std=analyzer_results.reference_metrics.abs_error_std,
            abs_perc_error_std=analyzer_results.reference_metrics.abs_perc_error_std,
            error_normality=analyzer_results.reference_metrics.error_normality,
            underperformance=analyzer_results.reference_metrics.underperformance,
            hist_for_plot=hist_for_plot,
            vals_for_plots=vals_for_plots,
            error_bias=analyzer_results.error_bias,
            mean_abs_error_ref=mean_abs_error_ref,
            mean_abs_perc_error_ref=mean_abs_perc_error_ref,
            rmse_ref=rmse_ref,
            r2_score_ref=r2_score_ref
        )


def _me_distr(df: pd.DataFrame, column_mapping: ColumnMapping):
    df = df.copy()
    count_uniq_values = df[column_mapping.target].nunique(dropna=True)
    df['target_binned'] = pd.cut(df[column_mapping.target],  min(count_uniq_values, 10))

    data = df[column_mapping.target] - df[column_mapping.prediction]
    me_bins = np.histogram_bin_edges(data, bins="doane")
    me_hist = np.histogram(data, bins=me_bins)

    return [(y, x) for x, y in zip(me_hist[0], me_hist[1])]
