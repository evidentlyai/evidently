from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model_monitoring.monitoring import ModelMonitor, ModelMonitoringMetric


class DataDriftMetrics:
    p_value = ModelMonitoringMetric("data_drift:p_value", ["feature", "feature_type"])
    dataset_drift = ModelMonitoringMetric("data_drift:dataset_drift")
    share_drifted_features = ModelMonitoringMetric("data_drift:share_drifted_features")
    n_drifted_features = ModelMonitoringMetric("data_drift:n_drifted_features")


class DataDriftMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "data_drift"

    def analyzers(self):
        return [DataDriftAnalyzer]

    def metrics(self, analyzer_results):
        data_drift_results = DataDriftAnalyzer.get_results(analyzer_results)
        yield DataDriftMetrics.share_drifted_features.create(data_drift_results.metrics.share_drifted_features)
        yield DataDriftMetrics.n_drifted_features.create(data_drift_results.metrics.n_drifted_features)
        yield DataDriftMetrics.dataset_drift.create(data_drift_results.metrics.dataset_drift)

        for feature_name in data_drift_results.get_all_features_list():
            feature_metric = data_drift_results.metrics.features[feature_name]
            yield DataDriftMetrics.p_value.create(
                feature_metric.p_value,
                dict(feature=feature_name, feature_type=feature_metric.feature_type))
