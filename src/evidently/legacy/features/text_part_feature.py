from typing import ClassVar
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class BeginsWith(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:BeginsWith"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    case_sensitive: bool
    prefix: str

    def __init__(
        self,
        column_name: str,
        prefix: str,
        case_sensitive: bool = True,
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        self.prefix = prefix
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.column_name}.{self.prefix}.{self.case_sensitive}"

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        column_data = data[self.column_name]
        substr = self.prefix
        if not self.case_sensitive:
            column_data = column_data.str.casefold()
            substr = substr.casefold()
        calculated = column_data.str.startswith(substr)
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text Begins with [{self.prefix}] for {self.column_name}",
        )


class EndsWith(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:EndsWith"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    case_sensitive: bool
    suffix: str

    def __init__(
        self,
        column_name: str,
        suffix: str,
        case_sensitive: bool = True,
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        self.suffix = suffix
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.column_name}.{self.suffix}.{self.case_sensitive}"

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        column_data = data[self.column_name]
        substr = self.suffix
        if not self.case_sensitive:
            column_data = column_data.str.casefold()
            substr = substr.casefold()
        calculated = column_data.str.endswith(substr)
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text Ends with [{self.suffix}] for {self.column_name}",
        )
