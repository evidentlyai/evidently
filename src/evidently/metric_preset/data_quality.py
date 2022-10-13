from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import DataQualityMetrics
from evidently.metrics import DatasetCorrelationsMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from evidently.utils.data_operations import DatasetColumns


class DataQuality(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [DataQualityMetrics()]


class DataQualityPreset(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            # TODO: add after implementation
            # DatasetSummary(),
            # ColumnSummary(),
            DatasetMissingValuesMetric(),
            DatasetCorrelationsMetric(),
        ]
