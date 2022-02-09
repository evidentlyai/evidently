from evidently.analyzers import num_target_drift_analyzer
from evidently.model_monitoring import monitoring


class NumTargetDriftMonitorMetrics:
    _tag = 'num_target_drift'
    drift = monitoring.ModelMonitoringMetric(f'{_tag}:drift', ['kind'])


class NumTargetDriftMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'num_target_drift'

    def analyzers(self):
        return [num_target_drift_analyzer.NumTargetDriftAnalyzer]

    def metrics(self, analyzer_results):
        results = num_target_drift_analyzer.NumTargetDriftAnalyzer.get_results(analyzer_results)

        if results.prediction_metrics:
            yield NumTargetDriftMonitorMetrics.drift.create(
                results.prediction_metrics.drift,
                dict(feature=results.prediction_metrics.column_name, feature_type='cat', kind='prediction')
            )

        if results.target_metrics:
            yield NumTargetDriftMonitorMetrics.drift.create(
                results.target_metrics.drift,
                dict(feature=results.target_metrics.column_name, feature_type='cat', kind='target')
            )
