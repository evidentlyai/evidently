import re

import pandas as pd
from dataclasses import dataclass
from itertools import combinations
from typing import Dict
from typing import List
from typing import Union

from evidently.v2.metrics.base_metric import InputData
from evidently.v2.metrics.base_metric import Metric


@dataclass
class DataIntegrityMetricsResults:
    number_of_columns: int
    number_of_rows: int
    number_of_nans: int
    number_of_columns_with_nans: int
    number_of_rows_with_nans: int
    # number_of_differently_encoded_nulls: int
    number_of_constant_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    number_of_duplicated_columns: int
    columns_type: dict
    nans_by_columns: dict
    number_uniques_by_columns: dict


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:
        return DataIntegrityMetricsResults(
            number_of_columns=len(data.current_data.columns),
            number_of_rows=data.current_data.shape[0],
            number_of_nans=data.current_data.isna().sum().sum(),
            number_of_columns_with_nans=data.current_data.isna().any().sum(),
            number_of_rows_with_nans=data.current_data.isna().any(axis=1).sum(),
            number_of_constant_columns=len(data.current_data.columns[data.current_data.nunique() <= 1]),  # type: ignore
            number_of_empty_rows=data.current_data.isna().all(1).sum(),
            number_of_empty_columns=data.current_data.isna().all().sum(),
            number_of_duplicated_rows=data.current_data.duplicated().sum(),
            number_of_duplicated_columns=sum([
                1 for i, j in combinations(data.current_data, 2) if data.current_data[i].equals(data.current_data[j])
            ]),
            columns_type=dict(data.current_data.dtypes.to_dict()),
            nans_by_columns=data.current_data.isna().sum().to_dict(),
            number_uniques_by_columns=dict(data.current_data.nunique().to_dict())
        )


@dataclass
class DataIntegrityValueByRegexpMetricResult:
    # mapping column_name: matched_count
    matched_values: Dict[str, int]


class DataIntegrityValueByRegexpMetrics(Metric[DataIntegrityValueByRegexpMetricResult]):
    """Count number of values in a column or in columns matched a regexp"""
    column_name: List[str]

    def __init__(self, column_name: Union[str, List[str]], reg_exp: str):
        self.reg_exp = reg_exp

        if isinstance(column_name, str):
            column_name = [column_name]

        self.column_name = column_name
        self.reg_exp_compiled = re.compile(reg_exp)

    def _calculate_matched_for_dataset(self, dataset: pd.DataFrame) -> Dict[str, int]:
        matched_values = {}

        for column_name in self.column_name:
            n = dataset[column_name].apply(lambda x: bool(self.reg_exp_compiled.match(str(x)))).sum()
            matched_values[column_name] = n

        return matched_values

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityValueByRegexpMetricResult:
        matched_values = self._calculate_matched_for_dataset(data.current_data)
        return DataIntegrityValueByRegexpMetricResult(matched_values=matched_values)
