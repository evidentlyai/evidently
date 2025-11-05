from functools import reduce
from typing import List
from typing import Optional

import pandas as pd

from evidently._pydantic_compat import Extra
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import register_type_alias


class FilterBy(PolymorphicModel):
    column: str

    class Config:
        is_base_type = True
        type_alias = "filter_by"
        extra = Extra.forbid

    def condition(self, df: pd.DataFrame) -> pd.Series:
        raise NotImplementedError


class FilterByString(FilterBy):
    value: str

    class Config:
        is_base_type = True
        type_alias = "filter_by_string"


class FilterByNumber(FilterBy):
    value: float

    class Config:
        is_base_type = True
        type_alias = "filter_by_number"


class ContainsStrFilter(FilterByString):
    class Config:
        type_alias = "contains"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.contains(self.value, na=False)


class StartsWithFilter(FilterByString):
    class Config:
        type_alias = "starts_with"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.startswith(self.value, na=False)


class EndsWithFilter(FilterByString):
    class Config:
        type_alias = "ends_with"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column].str.endswith(self.value, na=False)


class EqualFilter(FilterByNumber):
    class Config:
        type_alias = "eq"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] == self.value


class NotEqualFilter(FilterByNumber):
    class Config:
        type_alias = "not_eq"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] != self.value


class GTFilter(FilterByNumber):
    class Config:
        type_alias = "gt"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] > self.value


class GTEFilter(FilterByNumber):
    class Config:
        type_alias = "gte"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] >= self.value


class LTFilter(FilterByNumber):
    class Config:
        type_alias = "lt"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] < self.value


class LTEFilter(FilterByNumber):
    class Config:
        type_alias = "lte"

    def condition(self, df: pd.DataFrame) -> pd.Series:
        return df[self.column] <= self.value


def filter_df(df: pd.DataFrame, filter_by: Optional[List[FilterBy]]) -> pd.DataFrame:
    if not filter_by:
        return df
    conditions = [f.condition(df) for f in filter_by]
    combined_condition = reduce(lambda x, y: x & y, conditions)
    filtered_df = df[combined_condition]
    return filtered_df


register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.EqualFilter", "eq")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.GTEFilter", "gte")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.GTFilter", "gt")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.LTEFilter", "lte")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.LTFilter", "lt")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.NotEqualFilter", "not_eq")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.ContainsStrFilter", "contains")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.EndsWithFilter", "ends_with")
register_type_alias(FilterBy, "evidently.ui.service.datasets.filters.StartsWithFilter", "starts_with")
