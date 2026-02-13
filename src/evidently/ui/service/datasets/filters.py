from functools import reduce
from typing import List
from typing import Optional

import pandas as pd
from pydantic import ConfigDict

from evidently.pydantic_utils import PolymorphicModel


class FilterBy(PolymorphicModel):
    model_config = ConfigDict(extra="forbid")
    __type_alias__: str = "filter_by"
    __is_base_type__: bool = True

    column: str

    def condition(self, df: pd.DataFrame) -> pd.Series:
        raise NotImplementedError


class FilterByString(FilterBy):
    __type_alias__: str = "filter_by_string"
    __is_base_type__: bool = True
    value: str


class FilterByNumber(FilterBy):
    __type_alias__: str = "filter_by_number"
    __is_base_type__: bool = True
    value: float


class ContainsStrFilter(FilterByString):
    __type_alias__: str = "contains"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.contains(self.value, na=False)


class StartsWithFilter(FilterByString):
    __type_alias__: str = "starts_with"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.startswith(self.value, na=False)


class EndsWithFilter(FilterByString):
    __type_alias__: str = "ends_with"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.endswith(self.value, na=False)


class EqualFilter(FilterByNumber):
    __type_alias__: str = "eq"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] == self.value


class NotEqualFilter(FilterByNumber):
    __type_alias__: str = "not_eq"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] != self.value


class GTFilter(FilterByNumber):
    __type_alias__: str = "gt"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] > self.value


class GTEFilter(FilterByNumber):
    __type_alias__: str = "gte"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] >= self.value


class LTFilter(FilterByNumber):
    __type_alias__: str = "lt"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] < self.value


class LTEFilter(FilterByNumber):
    __type_alias__: str = "lte"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] <= self.value


def filter_df(df: pd.DataFrame, filter_by: Optional[List[FilterBy]]) -> pd.DataFrame:
    if not filter_by:
        return df
    conditions = [f.condition(df) for f in filter_by]
    combined_condition = reduce(lambda x, y: x & y, conditions)
    filtered_df = df[combined_condition]
    return filtered_df
