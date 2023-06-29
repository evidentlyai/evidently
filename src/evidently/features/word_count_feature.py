import re

import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class WordCount(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str):
        self.column_name = column_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def word_count_f(s):
            if s is None:
                return 0
            return len(re.sub(r"[^a-zA-Z ]+", "", s).split())

        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(word_count_f))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name, f"Word Count for {self.column_name}")


def word_count(column_name: str) -> ColumnName:
    return additional_feature(WordCount(column_name), f"{column_name}", f"Word Count for {column_name}")
