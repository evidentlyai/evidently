from evidently.utils.data_operations import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.regression_performance_metrics import RegressionPerformanceMetrics
from evidently.metrics.predicted_vs_actual import PredictedVsActualMetric


class RegressionPerformance(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            RegressionPerformanceMetrics(),
            PredictedVsActualMetric(),
        ]
