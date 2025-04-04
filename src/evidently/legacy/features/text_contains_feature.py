from typing import ClassVar
from typing import List
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class Contains(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:Contains"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    items: List[str]
    case_sensitive: bool
    mode: str

    def __init__(
        self,
        column_name: str,
        items: List[str],
        case_sensitive: bool = True,
        mode: str = "any",
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        if mode not in ["any", "all"]:
            raise ValueError("mode must be either 'any' or 'all'")
        self.mode = mode
        self.items = items
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.column_name}_" + "_".join(self.items) + "_" + str(self.case_sensitive) + "_" + self.mode

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if self.mode == "any":
            calculated = data[self.column_name].str.contains("|".join(self.items), case=self.case_sensitive)
        elif self.mode == "all":
            calculated = data[self.column_name].apply(lambda x: all(self.comparison(i, x) for i in self.items))
        else:
            raise ValueError("mode must be either 'any' or 'all'")
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text Contains of {self.mode} [{', '.join(self.items)}] for {self.column_name}",
        )

    def comparison(self, item: str, string: str):
        if self.case_sensitive:
            return item in string
        return item.casefold() in string.casefold()


class DoesNotContain(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:DoesNotContain"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    items: List[str]
    case_sensitive: bool
    mode: str

    def __init__(
        self,
        column_name: str,
        items: List[str],
        case_sensitive: bool = True,
        mode: str = "any",
        display_name: Optional[str] = None,
    ):
        self.column_name = column_name
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        if mode not in ["any", "all"]:
            raise ValueError("mode must be either 'any' or 'all'")
        self.mode = mode
        self.items = items
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.column_name}_" + "_".join(self.items) + "_" + str(self.case_sensitive) + "_" + self.mode

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if self.mode == "any":
            calculated = ~data[self.column_name].str.contains("|".join(self.items), case=self.case_sensitive)
        elif self.mode == "all":
            calculated = ~data[self.column_name].apply(lambda x: all(self.comparison(i, x) for i in self.items))
        else:
            raise ValueError("mode must be either 'any' or 'all'")
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text Does Not Contain of {self.mode} [{', '.join(self.items)}] for {self.column_name}",
        )

    def comparison(self, item: str, string: str):
        if not isinstance(string, str):
            return False
        if self.case_sensitive:
            return item in string
        return item.casefold() in string.casefold()


class ItemMatch(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:ItemMatch"

    __feature_type__: ClassVar = ColumnType.Categorical
    columns: List[str]
    case_sensitive: bool
    mode: str

    def __init__(
        self,
        columns: List[str],
        case_sensitive: bool = True,
        mode: str = "any",
        display_name: Optional[str] = None,
    ):
        if len(columns) != 2:
            raise ValueError("two columns must be provided")
        self.columns = columns
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        if mode not in ["any", "all"]:
            raise ValueError("mode must be either 'any' or 'all'")
        self.mode = mode
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.columns[0]}_{self.columns[1]}" + "_item_match_" + str(self.case_sensitive) + "_" + self.mode

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if self.mode == "any":
            calculated = data.apply(
                lambda row: any(self.comparison(word, row[self.columns[0]]) for word in row[self.columns[1]]),
                axis=1,
            )
        else:
            calculated = data.apply(
                lambda row: all(self.comparison(word, row[self.columns[0]]) for word in row[self.columns[1]]),
                axis=1,
            )
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text contains {self.mode} of defined items",
        )

    def comparison(self, item: str, string: str):
        if self.case_sensitive:
            return item in string
        return item.casefold() in string.casefold()


class ItemNoMatch(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:ItemNoMatch"

    __feature_type__: ClassVar = ColumnType.Categorical
    columns: List[str]
    case_sensitive: bool
    mode: str

    def __init__(
        self,
        columns: List[str],
        case_sensitive: bool = True,
        mode: str = "any",
        display_name: Optional[str] = None,
    ):
        self.columns = columns
        self.display_name = display_name
        self.case_sensitive = case_sensitive
        if mode not in ["any", "all"]:
            raise ValueError("mode must be either 'any' or 'all'")
        self.mode = mode
        super().__init__()

    def _feature_column_name(self) -> str:
        return f"{self.columns[0]}_{self.columns[1]}" + "_item_no_match_" + str(self.case_sensitive) + "_" + self.mode

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if self.mode == "any":
            calculated = data.apply(
                lambda row: not any(self.comparison(word, row[self.columns[0]]) for word in row[self.columns[1]]),
                axis=1,
            )
        else:
            calculated = data.apply(
                lambda row: not all(self.comparison(word, row[self.columns[0]]) for word in row[self.columns[1]]),
                axis=1,
            )
        return pd.DataFrame({self._feature_column_name(): calculated})

    def _as_column(self) -> ColumnName:
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"Text does not contain {self.mode} of defined items",
        )

    def comparison(self, item: str, string: str):
        if self.case_sensitive:
            return item in string
        return item.casefold() in string.casefold()
