from datetime import datetime

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceMetrics
from evidently.model_profile.sections.base_profile_section import ProfileSection


class RegressionPerformanceProfileSection(ProfileSection):
    def part_id(self) -> str:
        return "regression_performance"

    def __init__(self):
        super().__init__()
        self.analyzers_types = [RegressionPerformanceAnalyzer]
        self._result = None

    def analyzers(self):
        return self.analyzers_types

    @staticmethod
    def _get_regression_performance_metrics_as_dict(metrics: RegressionPerformanceMetrics) -> dict:
        return {
            "mean_error": metrics.mean_error,
            "mean_abs_error": metrics.mean_abs_error,
            "mean_abs_perc_error": metrics.mean_abs_perc_error,
            "error_std": metrics.error_std,
            "abs_error_std": metrics.abs_error_std,
            "abs_perc_error_std": metrics.abs_perc_error_std,
            "error_normality": metrics.error_normality,
            "underperformance": metrics.underperformance,
        }

    def calculate(self, reference_data, current_data, column_mapping, analyzers_results):
        result = RegressionPerformanceAnalyzer.get_results(analyzers_results)
        result_json = result.columns.dict(by_alias=True)
        result_json["metrics"] = {}

        if result.error_bias is not None:
            result_json["metrics"]["error_bias"] = result.error_bias

        if result.reference_metrics is not None:
            result_json["metrics"]["reference"] = self._get_regression_performance_metrics_as_dict(
                result.reference_metrics
            )

        if result.current_metrics is not None:
            result_json["metrics"]["current"] = self._get_regression_performance_metrics_as_dict(result.current_metrics)

        self._result = {
            "name": self.part_id(),
            "datetime": str(datetime.now()),
            "data": result_json,
        }

    def get_results(self):
        return self._result
