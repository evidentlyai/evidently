from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import RegressionAbsPercentageErrorPlot
from evidently.metrics import RegressionErrorBiasTable
from evidently.metrics import RegressionErrorDistribution
from evidently.metrics import RegressionErrorNormality
from evidently.metrics import RegressionErrorPlot
from evidently.metrics import RegressionPerformanceMetrics
from evidently.metrics import RegressionPredictedVsActualPlot
from evidently.metrics import RegressionPredictedVsActualScatter
from evidently.metrics import RegressionQualityMetric
from evidently.metrics import RegressionTopErrorMetric
from evidently.metrics.base_metric import InputData
from evidently.metrics.predicted_vs_actual import PredictedVsActualMetric
from evidently.utils.data_operations import DatasetColumns


class RegressionPerformance(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            RegressionPerformanceMetrics(),
            PredictedVsActualMetric(),
        ]


class RegressionPreset(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            RegressionQualityMetric(),
            RegressionPredictedVsActualScatter(),
            RegressionPredictedVsActualPlot(),
            RegressionErrorPlot(),
            RegressionAbsPercentageErrorPlot(),
            RegressionErrorDistribution(),
            RegressionErrorNormality(),
            RegressionTopErrorMetric(),
            RegressionErrorBiasTable(),
        ]
