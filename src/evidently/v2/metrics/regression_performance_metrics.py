from dataclasses import dataclass
from typing import Optional, Tuple, List

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class RegressionPerformanceMetricsResults:
    mean_error: float
    me_distr: List[Tuple[object, float]]
    mean_abs_error: float
    mae_distr: List[Tuple[object, float, int]]
    mean_abs_perc_error: float
    error_std: float
    abs_error_std: float
    abs_perc_error_std: float
    error_normality: dict
    underperformance: dict
    error_bias: Optional[dict] = None


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

        df = data.current_data.copy()
        df['target_binned'] = pd.cut(df[data.column_mapping.target], 10)

        data = df[data.column_mapping.target] - df[data.column_mapping.prediction]
        me_bins = np.histogram_bin_edges(data, bins="doane")
        me_hist = np.histogram(data, bins=me_bins)

        mae = df.groupby('target_binned').apply(lambda x: mean_absolute_error(x.target, x.preds))
        mae_hist = df.target_binned.value_counts().sort_index()

        return RegressionPerformanceMetricsResults(
            mean_error=analyzer_results.reference_metrics.mean_error,
            me_distr=[(y, x) for x, y in zip(me_hist[0], me_hist[1])],
            mean_abs_error=analyzer_results.reference_metrics.mean_abs_error,
            mae_distr=[(idx, mae[idx], value) for idx, value in mae_hist.items()],
            mean_abs_perc_error=analyzer_results.reference_metrics.mean_abs_perc_error,
            error_std=analyzer_results.reference_metrics.error_std,
            abs_error_std=analyzer_results.reference_metrics.abs_error_std,
            abs_perc_error_std=analyzer_results.reference_metrics.abs_perc_error_std,
            error_normality=analyzer_results.reference_metrics.error_normality,
            underperformance=analyzer_results.reference_metrics.underperformance,
            error_bias=analyzer_results.error_bias
        )
