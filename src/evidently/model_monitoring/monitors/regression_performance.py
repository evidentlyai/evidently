from typing import List
from typing import Type
from typing import Generator

from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceMetrics
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric
from evidently.model_monitoring.monitoring import MetricsType


class RegressionPerformanceMonitorMetrics:
    _tag = "regression_performance"
    quality = ModelMonitoringMetric(f"{_tag}:quality", ["dataset", "metric"])
    normality = ModelMonitoringMetric(f"{_tag}:error_normality", ["dataset", "metric"])
    underperformance = ModelMonitoringMetric(f"{_tag}:underperformance", ["dataset", "metric", "type"])
    feature_error_bias = ModelMonitoringMetric(f"{_tag}:feature_error_bias", ["feature", "feature_type", "metric"])


class RegressionPerformanceMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "regression_performance"

    def analyzers(self) -> List[Type[Analyzer]]:
        return [RegressionPerformanceAnalyzer]

    def metrics(self, analyzer_results) -> Generator[MetricsType, None, None]:
        results = RegressionPerformanceAnalyzer.get_results(analyzer_results)

        if results.reference_metrics is not None:
            for metric in self._yield_quality(results.reference_metrics, "reference"):
                yield metric

            for metric in self._yield_error_normality(results.reference_metrics.error_normality, "reference"):
                yield metric

            for metric in self._yield_underperformance(results.reference_metrics.underperformance, "reference"):
                yield metric

        if results.current_metrics is not None:
            for metric in self._yield_quality(results.current_metrics, "current"):
                yield metric

            for metric in self._yield_error_normality(results.current_metrics.error_normality, "current"):
                yield metric

            for metric in self._yield_underperformance(results.current_metrics.underperformance, "current"):
                yield metric

        fields = [
            "ref_majority",
            "ref_under",
            "ref_over",
            "ref_range",
            "current_majority",
            "current_under",
            "current_over",
            "current_range",
        ]

        if results.error_bias is not None:
            for feature in results.columns.num_feature_names:
                for field in fields:
                    yield RegressionPerformanceMonitorMetrics.feature_error_bias.create(
                        results.error_bias[feature][field], dict(feature=feature, feature_type="num", metric=field)
                    )

        if results.error_bias is not None:
            for feature in results.columns.cat_feature_names:
                for field in fields:
                    yield RegressionPerformanceMonitorMetrics.feature_error_bias.create(
                        results.error_bias[feature][field], dict(feature=feature, feature_type="cat", metric=field)
                    )

    @staticmethod
    def _yield_quality(metrics: RegressionPerformanceMetrics, dataset: str) -> Generator[MetricsType, None, None]:
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.mean_error, dict(dataset=dataset, metric="mean_error")
        )
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.mean_abs_error, dict(dataset=dataset, metric="mean_abs_error")
        )
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.mean_abs_perc_error, dict(dataset=dataset, metric="mean_abs_perc_error")
        )
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.error_std, dict(dataset=dataset, metric="error_std")
        )
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.abs_error_std, dict(dataset=dataset, metric="abs_error_std")
        )
        yield RegressionPerformanceMonitorMetrics.quality.create(
            metrics.abs_perc_error_std, dict(dataset=dataset, metric="abs_perc_error_std")
        )

    @staticmethod
    def _yield_error_normality(normality_data, dataset) -> Generator[MetricsType, None, None]:
        metric_labels = ["slope", "intercept", "r"]
        for label in metric_labels:
            yield RegressionPerformanceMonitorMetrics.normality.create(
                normality_data[label], dict(dataset=dataset, metric=label)
            )

    @staticmethod
    def _yield_underperformance(underperformance_data, dataset) -> Generator[MetricsType, None, None]:
        type_labels = ["majority", "underestimation", "overestimation"]
        metric_labels = ["mean_error", "std_error"]
        for type_label in type_labels:
            for metric_label in metric_labels:
                yield RegressionPerformanceMonitorMetrics.underperformance.create(
                    underperformance_data[type_label][metric_label],
                    dict(dataset=dataset, metric=metric_label, type=type_label),
                )
