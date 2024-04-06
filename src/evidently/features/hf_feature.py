from typing import Optional

import evaluate
import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class HFFeature(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        column_data = data[self.column_name]
        model = evaluate.load(
            "toxicity",
            'DaNLP/da-electra-hatespeech-detection',
            module_type="measurement",
        )
        scores = model.compute(predictions=column_data, toxic_label="offensive")
        return pd.DataFrame(dict([(self.column_name, scores["toxicity"])]))

    def feature_name(self) -> ColumnName:
        return additional_feature(
            self,
            self.column_name,
            self.display_name or f"Hugging Face % for {self.column_name}",
        )

