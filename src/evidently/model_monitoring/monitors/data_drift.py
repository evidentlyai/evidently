from evidently.analyzers import data_drift_analyzer
from evidently.model_monitoring import monitoring


class DataDriftMonitorMetrics:
    _tag = 'data_drift'
    p_value = monitoring.ModelMonitoringMetric(f'{_tag}:p_value', ['feature', 'feature_type'])
    dataset_drift = monitoring.ModelMonitoringMetric(f'{_tag}:dataset_drift')
    share_drifted_features = monitoring.ModelMonitoringMetric(f'{_tag}:share_drifted_features')
    n_drifted_features = monitoring.ModelMonitoringMetric(f'{_tag}:n_drifted_features')


class DataDriftMonitor(monitoring.ModelMonitor):
    def monitor_id(self) -> str:
        return 'data_drift'

    def analyzers(self):
        return [data_drift_analyzer.DataDriftAnalyzer]

    def metrics(self, analyzer_results):
        data_drift_results = data_drift_analyzer.DataDriftAnalyzer.get_results(analyzer_results)
        yield DataDriftMonitorMetrics.share_drifted_features.create(data_drift_results.metrics.share_drifted_features)
        yield DataDriftMonitorMetrics.n_drifted_features.create(data_drift_results.metrics.n_drifted_features)
        yield DataDriftMonitorMetrics.dataset_drift.create(data_drift_results.metrics.dataset_drift)

        for feature_name in data_drift_results.columns.get_all_features_list(cat_before_num=True):
            feature_metric = data_drift_results.metrics.features[feature_name]
            yield DataDriftMonitorMetrics.p_value.create(
                feature_metric.p_value,
                dict(feature=feature_name, feature_type=feature_metric.feature_type)
            )
