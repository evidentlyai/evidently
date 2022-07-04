import re

import numpy as np
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
    current_stats: dict
    reference_stats: dict = None
    # number_of_columns: int
    # number_of_rows: int
    # number_of_nans: int
    # number_of_columns_with_nans: int
    # number_of_rows_with_nans: int
    # # number_of_differently_encoded_nulls: int
    # number_of_constant_columns: int
    # number_of_empty_rows: int
    # number_of_empty_columns: int
    # number_of_duplicated_rows: int
    # number_of_duplicated_columns: int
    # columns_type: dict
    # nans_by_columns: dict
    # number_uniques_by_columns: dict


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:

        columns = []
        for col in [data.column_mapping.target, data.column_mapping.datetime, data.column_mapping.id]:
            if col is not None:
                columns.append(col)
        for features in [data.column_mapping.numerical_features, data.column_mapping.categorical_features, 
                         data.column_mapping.datetime_features]:
            if features is not None:
                columns += features
        if data.column_mapping.prediction is not None:
            if isinstance(data.column_mapping.prediction, str):
                columns.append(data.column_mapping.prediction)
            elif isinstance(data.column_mapping.prediction, str):
                columns += data.column_mapping.prediction
        
        if len(columns) <= 3: # even with empty column_mapping we will have 3 default values
            columns = data.current_data.columns
            if data.reference_data is not None:
                columns = np.union1d(columns, data.reference_data.columns)
        current_columns = np.intersect1d(columns, data.current_data.columns)
        
        curr_data = data.current_data[current_columns]
        current_stats = {}
        current_stats['number_of_columns'] = len(current_columns)
        current_stats['number_of_rows'] = curr_data.shape[0]
        current_stats['number_of_nans'] = curr_data.isna().sum().sum()
        current_stats['number_of_columns_with_nans'] = curr_data.isna().any().sum()
        current_stats['number_of_rows_with_nans'] = curr_data.isna().any(axis=1).sum()
        current_stats['number_of_constant_columns'] = len(curr_data.columns[curr_data.nunique() <= 1])  # type: ignore
        current_stats['number_of_empty_rows'] = curr_data.isna().all(1).sum()
        current_stats['number_of_empty_columns'] = curr_data.isna().all().sum()
        current_stats['number_of_duplicated_rows'] = curr_data.duplicated().sum()
        current_stats['number_of_duplicated_columns'] = sum([
            1 for i, j in combinations(curr_data, 2) if curr_data[i].equals(curr_data[j])
        ])
        current_stats['columns_type'] = dict(curr_data.dtypes.to_dict())
        current_stats['nans_by_columns'] = curr_data.isna().sum().to_dict()
        current_stats['number_uniques_by_columns'] = dict(curr_data.nunique().to_dict())

        if data.reference_data is not None:
            reference_columns = np.intersect1d(columns, data.reference_data.columns)
            ref_data = data.reference_data[reference_columns]
            reference_stats = {}
            reference_stats['number_of_columns'] = len(reference_columns)
            reference_stats['number_of_rows'] = ref_data.shape[0]
            reference_stats['number_of_nans'] = ref_data.isna().sum().sum()
            reference_stats['number_of_columns_with_nans'] = ref_data.isna().any().sum()
            reference_stats['number_of_rows_with_nans'] = ref_data.isna().any(axis=1).sum()
            reference_stats['number_of_constant_columns'] = len(ref_data.columns[ref_data.nunique() <= 1])  # type: ignore
            reference_stats['number_of_empty_rows'] = ref_data.isna().all(1).sum()
            reference_stats['number_of_empty_columns'] = ref_data.isna().all().sum()
            reference_stats['number_of_duplicated_rows'] = ref_data.duplicated().sum()
            reference_stats['number_of_duplicated_columns'] = sum([
                1 for i, j in combinations(ref_data, 2) if ref_data[i].equals(ref_data[j])
            ])
            reference_stats['columns_type'] = dict(ref_data.dtypes.to_dict())
            reference_stats['nans_by_columns'] = ref_data.isna().sum().to_dict()
            reference_stats['number_uniques_by_columns'] = dict(ref_data.nunique().to_dict())
        else:
            reference_stats = None

        return DataIntegrityMetricsResults(
            current_stats=current_stats,
            reference_stats=reference_stats
        )


@dataclass
class DataIntegrityValueByRegexpMetricResult:
    # mapping column_name: matched_count
    matched_values: Dict[str, int]


class DataIntegrityValueByRegexpMetrics(Metric[DataIntegrityValueByRegexpMetricResult]):
    """Count number of values in a column or in columns matched a regexp"""
    def __init__(self, columns: Union[str, List[str]], reg_exp: str):
        self.reg_exp = reg_exp

        if isinstance(columns, str):
            columns = [columns]

        self.columns = columns
        self.reg_exp_compiled = re.compile(reg_exp)

    def _calculate_matched_for_dataset(self, dataset: pd.DataFrame) -> Dict[str, int]:
        matched_values = {}

        for column_name in self.columns:
            n = dataset[column_name].apply(lambda x: bool(self.reg_exp_compiled.match(str(x)))).sum()
            matched_values[column_name] = n

        return matched_values

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityValueByRegexpMetricResult:
        matched_values = self._calculate_matched_for_dataset(data.current_data)
        return DataIntegrityValueByRegexpMetricResult(matched_values=matched_values)
