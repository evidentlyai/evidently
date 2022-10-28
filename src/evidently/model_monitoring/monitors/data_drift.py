from typing import Generator

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer
from evidently.model_monitoring.monitoring import MetricsType
from evidently.model_monitoring.monitoring import ModelMonitor
from evidently.model_monitoring.monitoring import ModelMonitoringMetric


class DataDriftMonitorMetrics:
    _tag = "data_drift"
    value = ModelMonitoringMetric(
        f"{_tag}:value", ["feature", "feature_type", "stat_test"]
    )
    dataset_drift = ModelMonitoringMetric(f"{_tag}:dataset_drift")
    share_drifted_features = ModelMonitoringMetric(f"{_tag}:share_drifted_features")
    n_drifted_features = ModelMonitoringMetric(f"{_tag}:n_drifted_features")


class DataDriftMonitor(ModelMonitor):
    def monitor_id(self) -> str:
        return "data_drift"

    def analyzers(self):
        return [DataDriftAnalyzer]

    def metrics(self, analyzer_results) -> Generator[MetricsType, None, None]:
        data_drift_results = DataDriftAnalyzer.get_results(analyzer_results)
        yield DataDriftMonitorMetrics.share_drifted_features.create(
            data_drift_results.metrics.share_of_drifted_columns
        )
        yield DataDriftMonitorMetrics.n_drifted_features.create(
            data_drift_results.metrics.number_of_drifted_columns
        )
        yield DataDriftMonitorMetrics.dataset_drift.create(
            data_drift_results.metrics.dataset_drift
        )

        for feature_name in data_drift_results.columns.get_all_features_list(
            cat_before_num=True
        ):
            feature_metric = data_drift_results.metrics.drift_by_columns[feature_name]
            yield DataDriftMonitorMetrics.value.create(
                feature_metric.drift_score,
                dict(
                    feature=feature_name,
                    feature_type=feature_metric.column_type,
                    stat_test=feature_metric.stattest_name,
                ),
            )
