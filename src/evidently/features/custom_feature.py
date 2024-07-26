import uuid
from typing import Callable

import pandas as pd

from evidently._pydantic_compat import Field
from evidently.base_metric import ColumnName
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class CustomFeature(GeneratedFeature):
    display_name: str
    name: str = Field(default_factory=lambda: str(uuid.uuid4()))
    func: Callable[[pd.DataFrame, DataDefinition], pd.Series]

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data, data_definition)
        return pd.DataFrame({self.name: result})

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)


class CustomSingleColumnFeature(GeneratedFeature):
    display_name: str
    func: Callable[[pd.Series], pd.Series]
    name: str = Field(default_factory=lambda: str(uuid.uuid4()))
    column_name: str

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data[self.column_name])
        return pd.DataFrame({self.name: result}, index=data.index)

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)


class CustomPairColumnFeature(GeneratedFeature):
    display_name: str
    func: Callable[[pd.Series, pd.Series], pd.Series]
    name: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_column: str
    second_column: str

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data[self.first_column], data[self.second_column])
        return pd.DataFrame({self.name: result})

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)
