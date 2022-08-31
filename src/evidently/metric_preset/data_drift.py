from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.data_drift_metrics import DataDriftMetrics


class DataDrift(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [DataDriftMetrics()]
