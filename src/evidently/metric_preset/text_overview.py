from evidently.base_metric import InputData
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import TextDescriptorsCorrelationMetric
from evidently.metrics import TextDescriptorsDistribution
from evidently.metrics import TextDescriptorsDriftMetric
from evidently.utils.data_operations import DatasetColumns


class TextOverviewPreset(MetricPreset):
    """Metric preset for text column analysis.

    Contains metrics:
    - ColumnSummaryMetric
    - TextDescriptorsDistribution
    - TextDescriptorsCorrelation
    - ColumnDriftMetric
    - TextDescriptorsDescriptorsDriftMetric

    Args:
        column_name: text column name.
    """

    column_name: str

    def __init__(self, column_name: str):
        super().__init__()
        self.column_name = column_name

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        result = [
            ColumnSummaryMetric(column_name=self.column_name),
            TextDescriptorsDistribution(column_name=self.column_name),
            TextDescriptorsCorrelationMetric(column_name=self.column_name),
        ]
        if data.reference_data is not None:
            result.extend(
                [
                    ColumnDriftMetric(column_name=self.column_name),
                    TextDescriptorsDriftMetric(column_name=self.column_name),
                ]
            )
        return result
