from typing import Optional

import pandas as pd

from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class RegExp(GeneratedFeature):
    column_name: str
    feature_type = ColumnType.Categorical
    reg_exp: str

    def __init__(self, column_name: str, reg_exp: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.reg_exp = reg_exp
        self.display_name = display_name or f"RegExp '{reg_exp}' Match for column {column_name}"
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        result = data[self.column_name].astype(str).str.fullmatch(self.reg_exp).astype(int)
        return result

    def get_parameters(self):
        return self.column_name, self.reg_exp
