import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.metrics.base_metric import ColumnName
from evidently.metrics.base_metric import additional_feature
from evidently.utils.data_preprocessing import DataDefinition


class TextLength(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(len))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)


def text_length(column_name: str) -> ColumnName:
    return additional_feature(TextLength(column_name), f"{column_name}")
