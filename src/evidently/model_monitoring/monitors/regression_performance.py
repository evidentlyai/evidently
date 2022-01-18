from typing import List, Type, Generator

from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model_monitoring.monitoring import ModelMonitor, ModelMonitoringMetric, MetricsType


class RegressionPerformanceMetrics:
    _tag = "regression_performance"
    quality = ModelMonitoringMetric(f"{_tag}:quality", ["dataset", "metric"])
    normality = ModelMonitoringMetric(f"{_tag}:error_normality", ["dataset", "metric"])
    underperformance = ModelMonitoringMetric(f"{_tag}:underperformance",
                                             ["dataset", "metric", "type"])
    feature_error_bias = ModelMonitoringMetric(f"{_tag}:feature_error_bias",
                                               ["feature", "feature_type", "metric"])


class RegressionPerformanceMonitor(ModelMonitor):
    def analyzers(self) -> List[Type[Analyzer]]:
        return [RegressionPerformanceAnalyzer]

    def metrics(self, analyzer_results):
        results = analyzer_results[RegressionPerformanceAnalyzer]
        metrics = results['metrics']
        for metric in self._yield_quality(metrics, "reference"):
            yield metric
        for metric in self._yield_error_normality(metrics['reference']['error_normality'], 'reference'):
            yield metric
        for metric in self._yield_underperformance(metrics['reference']['underperformance'], 'reference'):
            yield metric

        if "current" in metrics:
            for metric in self._yield_quality(metrics, "current"):
                yield metric
            for metric in self._yield_error_normality(metrics['current']['error_normality'], 'current'):
                yield metric
            for metric in self._yield_underperformance(metrics['current']['underperformance'], 'current'):
                yield metric

        fields = ['ref_majority', 'ref_under', 'ref_over', 'ref_range',
                  'current_majority', 'current_under', 'current_over', 'current_range']
        for feature in results['num_feature_names']:
            for field in fields:
                yield RegressionPerformanceMetrics.feature_error_bias.create(
                    metrics['error_bias'][feature][field], dict(feature=feature, feature_type='num', metric=field))
        for feature in results['cat_feature_names']:
            for field in fields:
                yield RegressionPerformanceMetrics.feature_error_bias.create(
                    metrics['error_bias'][feature][field], dict(feature=feature, feature_type='cat', metric=field))

    @staticmethod
    def _yield_quality(metrics, dataset) -> Generator[MetricsType, None, None]:
        dataset_quality = metrics[dataset]
        metric_labels = ['mean_error',
                         'mean_abs_error',
                         'mean_abs_perc_error',
                         'error_std',
                         'abs_error_std',
                         'abs_perc_error_std']
        for label in metric_labels:
            yield RegressionPerformanceMetrics.quality.create(dataset_quality[label],
                                                              dict(dataset=dataset, metric=label))

    @staticmethod
    def _yield_error_normality(normality_data, dataset) -> Generator[MetricsType, None, None]:
        metric_labels = ['slope', 'intercept', 'r']
        for label in metric_labels:
            yield RegressionPerformanceMetrics.normality.create(normality_data[label],
                                                                dict(dataset=dataset, metric=label))

    @staticmethod
    def _yield_underperformance(underperformance_data, dataset) -> Generator[MetricsType, None, None]:
        type_labels = ['majority', 'underestimation', 'overestimation']
        metric_labels = ['mean_error', 'std_error']
        for type_label in type_labels:
            for metric_label in metric_labels:
                yield RegressionPerformanceMetrics.underperformance.create(
                    underperformance_data[type_label][metric_label],
                    dict(dataset=dataset, metric=metric_label, type=type_label)
                )

    def monitor_id(self) -> str:
        return "regression_performance"
