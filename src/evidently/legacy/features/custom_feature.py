from typing import Callable
from typing import Tuple

import pandas as pd

from evidently._pydantic_compat import Field
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.core import new_id
from evidently.legacy.features.generated_features import FeatureTypeFieldMixin
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.pydantic_utils import FingerprintPart


class CustomFeature(FeatureTypeFieldMixin, GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:CustomFeature"

    display_name: str
    name: str = Field(default_factory=lambda: str(new_id()))
    func: Callable[[pd.DataFrame, DataDefinition], pd.Series]
    feature_type: ColumnType = ColumnType.Numerical

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data, data_definition)
        return pd.DataFrame({self.name: result})

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)


class CustomSingleColumnFeature(FeatureTypeFieldMixin, GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:CustomSingleColumnFeature"

    display_name: str
    func: Callable[[pd.Series], pd.Series]
    name: str = Field(default_factory=lambda: str(new_id()))
    column_name: str
    feature_type: ColumnType = ColumnType.Numerical

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data[self.column_name])
        return pd.DataFrame({self.name: result}, index=data.index)

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)

    def get_fingerprint_parts(self) -> Tuple[FingerprintPart, ...]:
        return tuple(
            (name, self.get_field_fingerprint(name))
            for name, field in sorted(self.__fields__.items())
            if (field.required or getattr(self, name) != field.get_default()) and field.name != "func"
        )


class CustomPairColumnFeature(FeatureTypeFieldMixin, GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:CustomPairColumnFeature"

    display_name: str
    func: Callable[[pd.Series, pd.Series], pd.Series]
    name: str = Field(default_factory=lambda: str(new_id()))
    first_column: str
    second_column: str
    feature_type: ColumnType = ColumnType.Numerical

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = self.func(data[self.first_column], data[self.second_column])
        return pd.DataFrame({self.name: result})

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)
