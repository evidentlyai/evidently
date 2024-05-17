import itertools
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.descriptors import OOV
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import SemanticSimilarity
from evidently.descriptors import SentenceCount
from evidently.descriptors import Sentiment
from evidently.descriptors import TextLength
from evidently.features.generated_features import FeatureDescriptor
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnSummaryMetric
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

    columns: List[str]

    def __init__(
        self,
        column_name: Optional[str] = None,
        columns: Optional[List[str]] = None,
        descriptors: Optional[Dict[str, FeatureDescriptor]] = None,
    ):
        super().__init__()
        if column_name is not None and columns is not None:
            raise ValueError("Cannot specify both `columns` and `columns`.")
        if columns is None and columns is None:
            raise ValueError("Must specify either `columns` or `columns`.")
        self.columns = columns or [column_name]
        self.descriptors = descriptors

    def generate_metrics(self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]):
        result = []
        descriptors = self.descriptors or [
            TextLength(),
            SentenceCount(),
            Sentiment(),
            OOV(),
            NonLetterCharacterPercentage(),
        ]
        for column in self.columns:
            result.append(ColumnSummaryMetric(column_name=column))
            for descriptor in descriptors:
                feature = descriptor.on(column)
                result.append(ColumnSummaryMetric(feature))

        if len(self.columns) > 1:
            column_x_column = itertools.product(self.columns, self.columns)
            for pair in column_x_column:
                if pair[0] == pair[1]:
                    continue
                result.append(ColumnSummaryMetric(SemanticSimilarity(columns=pair).as_column()))
        return result
