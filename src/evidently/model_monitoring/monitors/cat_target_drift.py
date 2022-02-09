from typing import Generator

from evidently.analyzers import cat_target_drift_analyzer
from evidently.model_monitoring import monitoring


class CatTargetDriftMonitorMetrics:
    _tag = 'cat_target_drift'
    drift = monitoring.ModelMonitoringMetric(f'{_tag}:drift', ['feature', 'feature_type', 'kind'])


class NumTargetDriftMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'cat_target_drift'

    def analyzers(self):
        return [cat_target_drift_analyzer.CatTargetDriftAnalyzer]

    def metrics(self, analyzer_results) -> Generator[monitoring.MetricsType, None, None]:
        results = cat_target_drift_analyzer.CatTargetDriftAnalyzer.get_results(analyzer_results)

        if results.prediction_metrics:
            yield CatTargetDriftMonitorMetrics.drift.create(
                results.prediction_metrics.drift,
                dict(feature=results.prediction_metrics.column_name, feature_type='cat', kind='prediction')
            )

        if results.target_metrics:
            yield CatTargetDriftMonitorMetrics.drift.create(
                results.target_metrics.drift,
                dict(feature=results.target_metrics.column_name, feature_type='cat', kind='target')
            )
