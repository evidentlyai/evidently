from typing import Any
from typing import Dict
from typing import Optional

from evidently.features.generated_features import FeatureDescriptor
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnSummaryMetric
from evidently.metrics import TextDescriptorsCorrelationMetric
from evidently.metrics import TextDescriptorsDistribution
from evidently.metrics import TextDescriptorsDriftMetric
from evidently.utils.data_preprocessing import DataDefinition


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

    def __init__(self, column_name: str, descriptors: Optional[Dict[str, FeatureDescriptor]] = None):
        super().__init__()
        self.column_name = column_name
        self.descriptors = descriptors

    def generate_metrics(self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]):
        result = [
            ColumnSummaryMetric(column_name=self.column_name),
            TextDescriptorsDistribution(column_name=self.column_name, descriptors=self.descriptors),
            TextDescriptorsCorrelationMetric(column_name=self.column_name, descriptors=self.descriptors),
        ]
        if data_definition.reference_present() is not None:
            result.extend(
                [
                    ColumnDriftMetric(column_name=self.column_name),
                    TextDescriptorsDriftMetric(column_name=self.column_name, descriptors=self.descriptors),
                ]
            )
        return result
