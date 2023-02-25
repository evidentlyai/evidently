import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature, FeatureDescriptor
from evidently.utils.data_preprocessing import DataDefinition


class TextLength(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def text_len(s):
            if s is None:
                return 0
            return len(s)

        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(text_len))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)


def text_length(column_name: str) -> ColumnName:
    return additional_feature(TextLength(column_name), f"{column_name}")


class TextLengthDesc(FeatureDescriptor):
    def feature(self, column_name: str) -> GeneratedFeature:
        return TextLength(column_name)

    def for_column(self, column_name: str):
        return TextLength(column_name).feature_name()
