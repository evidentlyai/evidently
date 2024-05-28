from typing import Callable

import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class CustomFeature(GeneratedFeature):
    display_name: str
    func: Callable[[pd.DataFrame, DataDefinition], pd.Series]

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        result = self.func(data, data_definition)
        return result


class CustomSingleColumnFeature(GeneratedFeature):
    display_name: str
    func: Callable[[pd.Series], pd.Series]
    column_name: str

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        result = self.func(data[self.column_name])
        return result


class CustomPairColumnFeature(GeneratedFeature):
    display_name: str
    func: Callable[[pd.Series, pd.Series], pd.Series]
    first_column: str
    second_column: str

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        result = self.func(data[self.first_column], data[self.second_column])
        return result
