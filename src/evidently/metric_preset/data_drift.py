from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import DataDriftTable
from evidently.metrics import DatasetDriftMetric
from evidently.metrics.base_metric import InputData
from evidently.utils.data_operations import DatasetColumns


class DataDriftPreset(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [DatasetDriftMetric(), DataDriftTable()]
