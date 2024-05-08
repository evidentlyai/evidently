from typing import Optional

import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class TextPart(GeneratedFeature):
    column_name: str
    case_sensitive: bool
    substring: str
    mode: str

    def __init__(
        self,
        column_name: str,
        substring: str,
        case_sensitive: bool = True,
        mode: str = "prefix",
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        if mode not in ["prefix", "suffix"]:
            raise ValueError("mode must be either 'prefix' or 'suffix'")
        self.mode = mode
        self.substring = substring
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        data = data[self.column_name]
        substr = self.substring
        if not self.case_sensitive:
            data = data.str.casefold()
            substr = substr.casefold()
        if self.mode == "prefix":
            calculated = data.str.startswith(substr)
        elif self.mode == "suffix":
            calculated = data.str.endswith(substr)
        else:
            raise ValueError("mode must be either 'prefix' or 'suffix'")
        return pd.DataFrame(dict([(
            self.column_name,
            calculated,
        )]))

    def feature_name(self) -> ColumnName:
        return additional_feature(
            self,
            self.column_name,
            self.display_name or f"Text {self.mode.capitalize()} [{self.substring}] for {self.column_name}",
        )
