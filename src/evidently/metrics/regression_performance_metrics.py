from dataclasses import dataclass
from typing import Dict
from typing import Optional


import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import make_target_bins_for_reg_plots
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.metrics.utils import apply_func_to_binned_data
from evidently.metrics.utils import make_hist_for_num_plot


@dataclass
class RegressionPerformanceMetricsResults:
    r2_score: float
    rmse: float
    rmse_default: float
    mean_error: float
    me_hist_for_plot: Dict[str, pd.Series]
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
    mean_abs_error_ref: Optional[float] = None
    mean_abs_perc_error_ref: Optional[float] = None
    rmse_ref: Optional[float] = None
    r2_score_ref: Optional[float] = None


class RegressionPerformanceMetrics(Metric[RegressionPerformanceMetricsResults]):
    def __init__(self):
        self.analyzer = RegressionPerformanceAnalyzer()

    def calculate(self, data: InputData, metrics: dict) -> RegressionPerformanceMetricsResults:
        if data.current_data is None:
            raise ValueError("current dataset should be present")

        if data.reference_data is None:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.current_data, current_data=None, column_mapping=data.column_mapping
            )
            current_metrics = analyzer_results.reference_metrics
            reference_metrics = None
        else:
            analyzer_results = self.analyzer.calculate(
                reference_data=data.reference_data, current_data=data.current_data, column_mapping=data.column_mapping
            )
            current_metrics = analyzer_results.current_metrics
            reference_metrics = analyzer_results.reference_metrics

        r2_score_value = r2_score(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=data.current_data[data.column_mapping.prediction],
        )
        rmse_score_value = mean_squared_error(
            y_true=data.current_data[data.column_mapping.target],
            y_pred=data.current_data[data.column_mapping.prediction],
        )

        # mae default values
        dummy_preds = data.current_data[data.column_mapping.target].median()
        mean_abs_error_default = mean_absolute_error(
            y_true=data.current_data[data.column_mapping.target], y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        # rmse default values
        rmse_ref = None
        if data.reference_data is not None:
            rmse_ref = mean_squared_error(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction],
            )
        dummy_preds = data.current_data[data.column_mapping.target].mean()
        rmse_default = mean_squared_error(
            y_true=data.current_data[data.column_mapping.target], y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        # mape default values
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
            y_true=data.current_data[data.column_mapping.target], y_pred=[dummy_preds] * data.current_data.shape[0]
        )
        #  r2_score default values
        r2_score_ref = None
        if data.reference_data is not None:
            r2_score_ref = r2_score(
                y_true=data.reference_data[data.column_mapping.target],
                y_pred=data.reference_data[data.column_mapping.prediction],
            )

        # visualisation

        df_target_binned = make_target_bins_for_reg_plots(
            data.current_data, data.column_mapping.target, data.column_mapping.prediction, data.reference_data
        )
        curr_target_bins = df_target_binned.loc[df_target_binned.data == "curr", "target_binned"]
        ref_target_bins = None
        if data.reference_data is not None:
            ref_target_bins = df_target_binned.loc[df_target_binned.data == "ref", "target_binned"]
        hist_for_plot = make_hist_for_cat_plot(curr_target_bins, ref_target_bins)

        vals_for_plots = {}

        if data.reference_data is not None:
            is_ref_data = True

        else:
            is_ref_data = False

        for name, func in zip(
            ["r2_score", "rmse", "mean_abs_error", "mean_abs_perc_error"],
            [r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error],
        ):
            vals_for_plots[name] = apply_func_to_binned_data(
                df_target_binned, func, data.column_mapping.target, data.column_mapping.prediction, is_ref_data
            )

        # me plot
        err_curr = data.current_data[data.column_mapping.prediction] - data.current_data[data.column_mapping.target]
        err_ref = None

        if is_ref_data:
            err_ref = (
                data.reference_data[data.column_mapping.prediction] - data.reference_data[data.column_mapping.target]
            )
        me_hist_for_plot = make_hist_for_num_plot(err_curr, err_ref)

        if r2_score_ref is not None:
            r2_score_ref = float(r2_score_ref)

        if rmse_ref is not None:
            rmse_ref = float(rmse_ref)

        return RegressionPerformanceMetricsResults(
            r2_score=r2_score_value,
            rmse=rmse_score_value,
            rmse_default=rmse_default,
            mean_error=current_metrics.mean_error,
            me_hist_for_plot=me_hist_for_plot,
            mean_abs_error=current_metrics.mean_abs_error,
            mean_abs_error_default=mean_abs_error_default,
            mean_abs_perc_error=current_metrics.mean_abs_perc_error,
            mean_abs_perc_error_default=mean_abs_perc_error_default,
            abs_error_max=current_metrics.abs_error_max,
            error_std=current_metrics.error_std,
            abs_error_std=current_metrics.abs_error_std,
            abs_perc_error_std=current_metrics.abs_perc_error_std,
            error_normality=current_metrics.error_normality,
            underperformance=current_metrics.underperformance,
            hist_for_plot=hist_for_plot,
            vals_for_plots=vals_for_plots,
            error_bias=analyzer_results.error_bias,
            mean_abs_error_ref=reference_metrics.mean_abs_error if reference_metrics is not None else None,
            mean_abs_perc_error_ref=reference_metrics.mean_abs_perc_error if reference_metrics is not None else None,
            rmse_ref=rmse_ref,
            r2_score_ref=r2_score_ref,
        )
