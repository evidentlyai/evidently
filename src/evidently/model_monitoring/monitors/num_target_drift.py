from typing import Generator

from evidently.analyzers import num_target_drift_analyzer
from evidently.model_monitoring import monitoring


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
    _tag = 'num_target_drift'
    count = monitoring.ModelMonitoringMetric(f'{_tag}:count', ['dataset'])
    drift = monitoring.ModelMonitoringMetric(f'{_tag}:drift', ['kind'])
    current_correlations = monitoring.ModelMonitoringMetric(
        f'{_tag}:current_correlations', ['feature', 'feature_type', 'kind']
    )
    reference_correlations = monitoring.ModelMonitoringMetric(
        f'{_tag}:reference_correlations', ['feature', 'feature_type', 'kind']
    )


class NumTargetDriftMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'num_target_drift'

    def analyzers(self):
        return [num_target_drift_analyzer.NumTargetDriftAnalyzer]

    @staticmethod
    def _yield_metrics(
            metrics: num_target_drift_analyzer.NumDataDriftMetrics,
            kind: str
    ) -> Generator[monitoring.MetricsType, None, None]:
        yield NumTargetDriftMonitorMetrics.drift.create(metrics.drift, dict(kind=kind))

        for feature_name, correlation_value in metrics.reference_correlations.items():
            yield NumTargetDriftMonitorMetrics.reference_correlations.create(
                correlation_value, dict(feature=feature_name, feature_type='num', kind=kind)
            )

        for feature_name, correlation_value in metrics.current_correlations.items():
            yield NumTargetDriftMonitorMetrics.current_correlations.create(
                correlation_value, dict(feature=feature_name, feature_type='num', kind=kind)
            )

    def metrics(self, analyzer_results):
        results = num_target_drift_analyzer.NumTargetDriftAnalyzer.get_results(analyzer_results)

        # quantity of rows in income data
        yield NumTargetDriftMonitorMetrics.count.create(results.reference_data_count, dict(dataset='prediction'))
        yield NumTargetDriftMonitorMetrics.count.create(results.current_data_count, dict(dataset='current'))

        if results.prediction_metrics:
            for metric in self._yield_metrics(metrics=results.prediction_metrics, kind='prediction'):
                yield metric

        if results.target_metrics:
            for metric in self._yield_metrics(metrics=results.target_metrics, kind='target'):
                yield metric
