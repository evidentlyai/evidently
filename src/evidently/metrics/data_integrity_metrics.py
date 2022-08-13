import re

from dataclasses import dataclass
from itertools import combinations
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric


@dataclass
class DataIntegrityMetricsValues:
    number_of_columns: int
    number_of_rows: int
    number_of_nans: int
    number_of_columns_with_nans: int
    number_of_rows_with_nans: int
    number_of_constant_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    number_of_duplicated_columns: int
    columns_type: dict
    nans_by_columns: dict
    number_uniques_by_columns: dict
    counts_of_values: dict


@dataclass
class DataIntegrityMetricsResults:
    current_stats: DataIntegrityMetricsValues
    reference_stats: Optional[DataIntegrityMetricsValues] = None


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    @staticmethod
    def _get_integrity_metrics_values(dataset: pd.DataFrame, columns: tuple) -> DataIntegrityMetricsValues:
        counts_of_values = {}
        for col in dataset.columns:
            feature = dataset[col]
            df_counts = feature.value_counts(dropna=False).reset_index()
            df_counts.columns = ["x", "count"]
            counts_of_values[col] = df_counts
        return DataIntegrityMetricsValues(
            number_of_columns=len(columns),
            number_of_rows=dataset.shape[0],
            number_of_nans=dataset.isna().sum().sum(),
            number_of_columns_with_nans=dataset.isna().any().sum(),
            number_of_rows_with_nans=dataset.isna().any(axis=1).sum(),
            number_of_constant_columns=len(dataset.columns[dataset.nunique() <= 1]),  # type: ignore
            number_of_empty_rows=dataset.isna().all(1).sum(),
            number_of_empty_columns=dataset.isna().all().sum(),
            number_of_duplicated_rows=dataset.duplicated().sum(),
            number_of_duplicated_columns=sum([1 for i, j in combinations(dataset, 2) if dataset[i].equals(dataset[j])]),
            columns_type=dict(dataset.dtypes.to_dict()),
            nans_by_columns=dataset.isna().sum().to_dict(),
            number_uniques_by_columns=dict(dataset.nunique().to_dict()),
            counts_of_values=counts_of_values,
        )

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityMetricsResults:
        columns = []

        for col in [data.column_mapping.target, data.column_mapping.datetime, data.column_mapping.id]:
            if col is not None:
                columns.append(col)

        for features in [
            data.column_mapping.numerical_features,
            data.column_mapping.categorical_features,
            data.column_mapping.datetime_features,
        ]:
            if features is not None:
                columns += features

        if data.column_mapping.prediction is not None:
            if isinstance(data.column_mapping.prediction, str):
                columns.append(data.column_mapping.prediction)

            elif isinstance(data.column_mapping.prediction, str):
                columns += data.column_mapping.prediction

        # even with empty column_mapping we will have 3 default values
        if len(columns) <= 3:
            columns = data.current_data.columns

            if data.reference_data is not None:
                columns = np.union1d(columns, data.reference_data.columns)

        current_columns = np.intersect1d(columns, data.current_data.columns)

        curr_data = data.current_data[current_columns]
        current_stats = self._get_integrity_metrics_values(curr_data, current_columns)

        if data.reference_data is not None:
            reference_columns = np.intersect1d(columns, data.reference_data.columns)
            ref_data = data.reference_data[reference_columns]
            reference_stats: Optional[DataIntegrityMetricsValues] = self._get_integrity_metrics_values(
                ref_data, reference_columns
            )

        else:
            reference_stats = None

        return DataIntegrityMetricsResults(current_stats=current_stats, reference_stats=reference_stats)


@dataclass
class DataIntegrityValueByRegexpMetricResult:
    # mapping column_name: matched_count
    not_matched_values: Dict[str, int]
    not_matched_table: Dict[str, int]
    mult: Optional[float] = None


class DataIntegrityValueByRegexpMetrics(Metric[DataIntegrityValueByRegexpMetricResult]):
    """Count number of values in a column not matched a regexp"""

    column_name: str

    def __init__(self, column_name: str, reg_exp: str):
        self.reg_exp = reg_exp

        self.column_name = column_name
        self.reg_exp_compiled = re.compile(reg_exp)

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityValueByRegexpMetricResult:
        mult = None
        not_matched_values = {}
        not_matched_table = {}
        selector = data.current_data[self.column_name].apply(lambda x: bool(self.reg_exp_compiled.match(str(x))))
        n = selector.sum()
        not_matched_values["current"] = data.current_data[self.column_name].dropna().shape[0] - n

        df_counts = (
            data.current_data[self.column_name]
            .dropna()[~selector.dropna().astype(bool)]
            .value_counts(dropna=False)
            .reset_index()
        )
        df_counts.columns = ["x", "count"]
        not_matched_table["current"] = df_counts

        if data.reference_data is not None:
            selector = data.reference_data[self.column_name].apply(lambda x: bool(self.reg_exp_compiled.match(str(x))))
            n = selector.sum()
            not_matched_values["reference"] = data.reference_data[self.column_name].dropna().shape[0] - n
            mult = data.current_data.shape[0] / data.reference_data.shape[0]
            df_counts = (
                data.reference_data[self.column_name]
                .dropna()[~selector.dropna().astype(bool)]
                .value_counts(dropna=False)
                .reset_index()
            )
            df_counts.columns = ["x", "count"]
            not_matched_table["reference"] = df_counts

        return DataIntegrityValueByRegexpMetricResult(
            not_matched_values=not_matched_values,
            not_matched_table=not_matched_table,
            mult=mult,
        )


@dataclass
class DataIntegrityNullValues:
    # set of different null-like values in the dataset
    different_nulls: Dict[Any, int]
    # number of different null-like values in the dataset
    number_of_different_nulls: int
    # set of different null-like values for each column
    different_nulls_by_column: Dict[str, Dict[Any, int]]
    # count of different null-like values for each column
    number_of_different_nulls_by_column: Dict[str, int]
    # count of null-values in all dataset
    number_of_nulls: int
    # share of null-values in all dataset
    share_of_nulls: float
    # count of null-values for each column
    number_of_nulls_by_column: Dict[str, int]
    # share of null-values for each column
    share_of_nulls_by_column: Dict[str, float]
    # count of rows in the dataset
    number_of_rows: int
    # count of rows with a null-value
    number_of_rows_with_nulls: int
    # share of rows with a null-value
    share_of_rows_with_nulls: float
    # count of columns in the dataset
    number_of_columns: int
    # list of columns with a null value
    columns_with_nulls: List[str]
    # count of columns with a null-value
    number_of_columns_with_nulls: int
    # share of columns with a null-value
    share_of_columns_with_nulls: float


@dataclass
class DataIntegrityNullValuesMetricsResult:
    current_null_values: DataIntegrityNullValues
    reference_null_values: Optional[DataIntegrityNullValues] = None


class DataIntegrityNullValuesMetrics(Metric[DataIntegrityNullValuesMetricsResult]):
    """Count null values in a dataset.

    Calculate an amount of null-like values kinds and count for such values.
    NA-types like numpy.NaN, pandas.NaT are counted as one type.

    You can set you own null-line values list with `null_values` parameter.
    Value None in the list means that Pandas null values will be included in the calculation.

    If `replace` parameter is False - add defaults to user's list.
    If `replace` parameter is True - use values from `null_values` list only.
    """

    # default null values list
    DEFAULT_NULL_VALUES = ["", np.inf, -np.inf, None]
    null_values: frozenset

    def __init__(self, null_values: Optional[list] = None, replace: bool = True) -> None:
        if null_values is None:
            # use default null-values list if we have no user-defined null values
            null_values = self.DEFAULT_NULL_VALUES

        elif not replace:
            # add default nulls to user-defined nulls list
            null_values = self.DEFAULT_NULL_VALUES + null_values

        # use frozenset because metrics parameters should be immutable/hashable for deduplication
        self.null_values = frozenset(null_values)

    def _calculate_null_values_stats(self, dataset: pd.DataFrame) -> DataIntegrityNullValues:
        different_nulls = {null_value: 0 for null_value in self.null_values}
        columns_with_nulls = set()
        number_of_nulls = 0
        number_of_nulls_by_column: Dict[str, int] = {}
        different_nulls_by_column: Dict[str, Dict[Any, int]] = {}

        for column_name in dataset.columns:
            number_of_nulls_by_column[column_name] = 0
            different_nulls_by_column[column_name] = {}

            for null_value in self.null_values:
                different_nulls_by_column[column_name][null_value] = 0

        number_of_rows_with_nulls = 0
        number_of_columns = len(dataset.columns)
        number_of_rows = dataset.shape[0]

        for column_name in dataset.columns:
            # iterate by each value in custom null-values list and check the value in a column
            for null_value in self.null_values:
                if null_value is None:
                    # check all pandas null-types like numpy.NAN, pandas.NA, pandas.NaT, etc
                    column_null = dataset[column_name].isnull().sum()

                else:
                    column_null = (dataset[column_name] == null_value).sum()

                if column_null > 0:
                    # increase overall counter
                    number_of_nulls += column_null
                    # increase by-column counter
                    number_of_nulls_by_column[column_name] += column_null
                    # increase by-null-value counter for each column
                    different_nulls_by_column[column_name][null_value] += column_null
                    # increase by-null-value counter
                    different_nulls[null_value] += column_null
                    # add the column to set of columns with a null value
                    columns_with_nulls.add(column_name)

        for _, row in dataset.iterrows():
            if None in self.null_values:
                # check pandas null-values
                if row.isnull().any():
                    # if there is a null-value - just increase the counter and move to check the next row
                    number_of_rows_with_nulls += 1
                    continue

            for null_value in self.null_values:
                if null_value is None:
                    # if there is a pandas null-value
                    increase_counter = row.isnull().any()

                else:
                    # if there is another null value
                    increase_counter = null_value in row

                if increase_counter:
                    number_of_rows_with_nulls += 1
                    continue

        share_of_nulls_by_column = {
            column_name: value / number_of_rows for column_name, value in number_of_nulls_by_column.items()
        }
        number_of_different_nulls_by_column = {}

        for column_name, nulls in different_nulls_by_column.items():
            # count a number of null-values that have a value in the column
            number_of_different_nulls_by_column[column_name] = len(
                {keys for keys, values in nulls.items() if values > 0}
            )

        number_of_columns_with_nulls = len(columns_with_nulls)
        number_of_different_nulls = len({k for k in different_nulls if different_nulls[k] > 0})

        return DataIntegrityNullValues(
            different_nulls=different_nulls,
            number_of_different_nulls=number_of_different_nulls,
            different_nulls_by_column=different_nulls_by_column,
            number_of_different_nulls_by_column=number_of_different_nulls_by_column,
            number_of_nulls=number_of_nulls,
            share_of_nulls=number_of_nulls / (number_of_columns * number_of_rows),
            number_of_nulls_by_column=number_of_nulls_by_column,
            share_of_nulls_by_column=share_of_nulls_by_column,
            number_of_rows=number_of_rows,
            number_of_rows_with_nulls=number_of_rows_with_nulls,
            share_of_rows_with_nulls=number_of_rows_with_nulls / number_of_rows,
            number_of_columns=number_of_columns,
            columns_with_nulls=sorted(columns_with_nulls),
            number_of_columns_with_nulls=len(columns_with_nulls),
            share_of_columns_with_nulls=number_of_columns_with_nulls / number_of_columns,
        )

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityNullValuesMetricsResult:
        if not self.null_values:
            raise ValueError("Null-values list should not be empty.")

        current_null_values = self._calculate_null_values_stats(data.current_data)

        if data.reference_data is not None:
            reference_null_values: Optional[DataIntegrityNullValues] = self._calculate_null_values_stats(
                data.reference_data
            )

        else:
            reference_null_values = None

        return DataIntegrityNullValuesMetricsResult(
            current_null_values=current_null_values,
            reference_null_values=reference_null_values,
        )
