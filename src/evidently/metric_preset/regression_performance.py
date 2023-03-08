from typing import List, Optional

from evidently.base_metric import InputData
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import (
    RegressionAbsPercentageErrorPlot,
    RegressionErrorBiasTable,
    RegressionErrorDistribution,
    RegressionErrorNormality,
    RegressionErrorPlot,
    RegressionPredictedVsActualPlot,
    RegressionPredictedVsActualScatter,
    RegressionQualityMetric,
    RegressionTopErrorMetric,
)
from evidently.utils.data_operations import DatasetColumns


class RegressionPreset(MetricPreset):
    """Metric preset for Regression performance analysis.

    Contains metrics:
    - RegressionQualityMetric
    - RegressionPredictedVsActualScatter
    - RegressionPredictedVsActualPlot
    - RegressionErrorPlot
    - RegressionAbsPercentageErrorPlot
    - RegressionErrorDistribution
    - RegressionErrorNormality
    - RegressionTopErrorMetric
    - RegressionErrorBiasTable
    """

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        super().__init__()
        self.columns = columns

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
            RegressionErrorBiasTable(columns=self.columns),
        ]
