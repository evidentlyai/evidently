from typing import Generator

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.model_monitoring.monitoring import MetricsType
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class NumTargetDriftMonitorMetrics:
    """Class for numeric target grift metrics.

    Metrics list:
        - count: quantity of rows in `reference` and `current` datasets
        - drift: p_value for the data drift
        - current_correlations: correlation with `target` and `prediction` columns
            for numeric features in `current` dataset
        - reference_correlations: correlation with `target` and `prediction` columns
            for numeric features in `reference` dataset
    """

    _tag = "num_target_drift"
    count = ModelMonitoringMetric(f"{_tag}:count", ["dataset"])
    drift = ModelMonitoringMetric(f"{_tag}:drift", ["kind"])
    current_correlations = ModelMonitoringMetric(f"{_tag}:current_correlations", ["feature", "feature_type", "kind"])
    reference_correlations = ModelMonitoringMetric(
        f"{_tag}:reference_correlations", ["feature", "feature_type", "kind"]
    )


class NumTargetDriftMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "num_target_drift"

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    @staticmethod
    def _yield_metrics(metrics: ColumnDataDriftMetrics, kind: str) -> Generator[MetricsType, None, None]:
        yield NumTargetDriftMonitorMetrics.drift.create(metrics.drift_score, dict(kind=kind))

        if metrics.reference.correlations is not None:
            for feature_name, correlation_value in metrics.reference.correlations.items():
                yield NumTargetDriftMonitorMetrics.reference_correlations.create(
                    correlation_value, dict(feature=feature_name, feature_type="num", kind=kind)
                )

        if metrics.current.correlations is not None:
            for feature_name, correlation_value in metrics.current.correlations.items():
                yield NumTargetDriftMonitorMetrics.current_correlations.create(
                    correlation_value, dict(feature=feature_name, feature_type="num", kind=kind)
                )

    def metrics(self, analyzer_results):
        results = NumTargetDriftAnalyzer.get_results(analyzer_results)

        # quantity of rows in income data
        yield NumTargetDriftMonitorMetrics.count.create(results.reference_data_count, dict(dataset="reference"))
        yield NumTargetDriftMonitorMetrics.count.create(results.current_data_count, dict(dataset="current"))

        if results.prediction_metrics:
            for metric in self._yield_metrics(metrics=results.prediction_metrics, kind="prediction"):
                yield metric

        if results.target_metrics:
            for metric in self._yield_metrics(metrics=results.target_metrics, kind="target"):
                yield metric
