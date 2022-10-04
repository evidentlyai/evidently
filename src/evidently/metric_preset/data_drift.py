from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.utils.data_operations import DatasetColumns


class DataDrift(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [DataDriftTable()]
