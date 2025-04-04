from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.metric_preset.metric_preset import AnyMetric
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.legacy.metrics import ColumnSummaryMetric
from evidently.legacy.metrics import DatasetSummaryMetric
from evidently.legacy.metrics.base_metric import generate_column_metrics
from evidently.legacy.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from evidently.legacy.utils.data_preprocessing import DataDefinition


class DataQualityPreset(MetricPreset):
    class Config:
        type_alias = "evidently:metric_preset:DataQualityPreset"

    """Metric preset for Data Quality analysis.

    Contains metrics:
    - DatasetSummaryMetric
    - ColumnSummaryMetric for each column
    - DatasetMissingValuesMetric
    - DatasetCorrelationsMetric

    Args:
        columns: list of columns for analysis.
    """

    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        return [
            DatasetSummaryMetric(),
            generate_column_metrics(ColumnSummaryMetric, columns=self.columns, skip_id_column=True),
            DatasetMissingValuesMetric(),
        ]
