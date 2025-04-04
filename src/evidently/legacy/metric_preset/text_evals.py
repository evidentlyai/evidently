from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.descriptors import OOV
from evidently.legacy.descriptors import NonLetterCharacterPercentage
from evidently.legacy.descriptors import SentenceCount
from evidently.legacy.descriptors import Sentiment
from evidently.legacy.descriptors import TextLength
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.metric_preset.metric_preset import AnyMetric
from evidently.legacy.metric_preset.metric_preset import MetricPreset
from evidently.legacy.metrics import ColumnSummaryMetric
from evidently.legacy.utils.data_preprocessing import DataDefinition


class TextEvals(MetricPreset):
    class Config:
        type_alias = "evidently:metric_preset:TextEvals"

    column_name: str
    descriptors: Optional[List[FeatureDescriptor]] = None

    def __init__(self, column_name: str, descriptors: Optional[List[FeatureDescriptor]] = None):
        self.column_name: str = column_name
        self.descriptors: Optional[List[FeatureDescriptor]] = descriptors
        super().__init__()

    def generate_metrics(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyMetric]:
        descriptors = self.descriptors or [
            TextLength(),
            SentenceCount(),
            Sentiment(),
            OOV(),
            NonLetterCharacterPercentage(),
        ]
        return [ColumnSummaryMetric(desc.on(self.column_name)) for desc in descriptors]
