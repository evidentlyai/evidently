from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model_monitoring.monitoring import ModelMonitor, ModelMonitoringMetric


class DataDriftMetrics:
    p_value = ModelMonitoringMetric("data_drift:p_value", ["feature", "feature_type"])
    dataset_drift = ModelMonitoringMetric("data_drift:dataset_drift")
    share_drifted_features = ModelMonitoringMetric("data_drift:share_drifted_features")
    n_drifted_features = ModelMonitoringMetric("data_drift:n_drifted_features")


class DataDriftMonitor(ModelMonitor):
    def __init__(self):
        self.analyzers_types = [DataDriftAnalyzer]

    def monitor_id(self) -> str:
        return "data_drift"

    def analyzers(self):
        return self.analyzers_types

    def metrics(self, analyzer_results):
        data_drift_results = analyzer_results[DataDriftAnalyzer]
        features = data_drift_results['cat_feature_names'] + data_drift_results['num_feature_names']
        yield DataDriftMetrics.share_drifted_features.create(data_drift_results['metrics']['share_drifted_features'])
        yield DataDriftMetrics.n_drifted_features.create(data_drift_results['metrics']['n_drifted_features'])
        yield DataDriftMetrics.dataset_drift.create(data_drift_results['metrics']['dataset_drift'])
        for feature in features:
            feature_metric = data_drift_results['metrics'][feature]
            yield DataDriftMetrics.p_value.create(
                feature_metric['p_value'],
                dict(feature=feature, feature_type=feature_metric['feature_type']))
