from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.metric_preset.metric_preset import AnyMetric
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.legacy.metrics import RegressionAbsPercentageErrorPlot
from evidently.legacy.metrics import RegressionErrorBiasTable
from evidently.legacy.metrics import RegressionErrorDistribution
from evidently.legacy.metrics import RegressionErrorNormality
from evidently.legacy.metrics import RegressionErrorPlot
from evidently.legacy.metrics import RegressionPredictedVsActualPlot
from evidently.legacy.metrics import RegressionPredictedVsActualScatter
from evidently.legacy.metrics import RegressionQualityMetric
from evidently.legacy.metrics import RegressionTopErrorMetric
from evidently.legacy.utils.data_preprocessing import DataDefinition


class RegressionPreset(MetricPreset):
    class Config:
        type_alias = "evidently:metric_preset:RegressionPreset"

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
        self.columns = columns
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
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
