from dataclasses import dataclass
from typing import Optional
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class RegressionPerformanceMetricsResults:
    mean_error: float
    mean_abs_error: float
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

        analyzer_results = self.analyzer.calculate(
            reference_data=data.current_data,
            current_data=None,
            column_mapping=data.column_mapping
        )
        return RegressionPerformanceMetricsResults(
            mean_error=analyzer_results.reference_metrics.mean_error,
            mean_abs_error=analyzer_results.reference_metrics.mean_abs_error,
            mean_abs_perc_error=analyzer_results.reference_metrics.mean_abs_perc_error,
            error_std=analyzer_results.reference_metrics.error_std,
            abs_error_std=analyzer_results.reference_metrics.abs_error_std,
            abs_perc_error_std=analyzer_results.reference_metrics.abs_perc_error_std,
            error_normality=analyzer_results.reference_metrics.error_normality,
            underperformance=analyzer_results.reference_metrics.underperformance,
            error_bias=analyzer_results.error_bias
        )
