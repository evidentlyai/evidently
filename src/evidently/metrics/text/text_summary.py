from typing import List
from typing import Optional

from evidently.descriptors import OOV
from evidently.descriptors import NonLetterCharacterPercentage
from evidently.descriptors import TextLength
from evidently.features.generated_features import FeatureDescriptor
from evidently.metrics import ColumnSummaryMetric
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.generators import BaseGenerator
from evidently.utils.generators import TObject


class TextSummary(BaseGenerator):
    def __init__(self, column_name: str, descriptors: Optional[List[FeatureDescriptor]] = None):
        self.column_name = column_name
        self.descriptors = (
            descriptors
            if descriptors is not None
            else [
                TextLength(),
                OOV(),
                NonLetterCharacterPercentage(),
            ]
        )

    def generate(self, data_definition: DataDefinition) -> List[TObject]:
        return [ColumnSummaryMetric(desc.for_column(self.column_name)) for desc in self.descriptors]
