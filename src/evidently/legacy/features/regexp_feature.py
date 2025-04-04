from typing import ClassVar
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class RegExp(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:RegExp"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    reg_exp: str

    def __init__(self, column_name: str, reg_exp: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.reg_exp = reg_exp
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = data[self.column_name].astype(str).str.fullmatch(self.reg_exp).astype(int)
        return pd.DataFrame({self._feature_name(): result})

    def _feature_name(self):
        return self.column_name + "_" + self.reg_exp

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"RegExp '{self.reg_exp}' Match for column {self.column_name}",
        )
