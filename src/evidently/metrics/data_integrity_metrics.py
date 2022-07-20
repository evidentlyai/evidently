import re

import numpy as np
import pandas as pd
from dataclasses import dataclass
from itertools import combinations
from typing import Dict
from typing import Optional

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
    number_of_differently_encoded_nulls: int
    number_of_null_values: int


@dataclass
class DataIntegrityNullValuesMetricsResult:
    current_null_values: DataIntegrityNullValues
    reference_null_values: Optional[DataIntegrityNullValues] = None


class DataIntegrityNullValuesMetrics(Metric[DataIntegrityNullValuesMetricsResult]):
    """Count null values in a dataset.

    Calculate an amount of null-like values kinds and overall count for such values.
    NA-types like numpy.NaN, pandas.NaT are counted as one type.
    If you do not want to take them into account - you can do it with `ignore_na` parameter.

    Also, you can set you own null-line values list with `null_values` parameter.
    """

    # default custom null values list
    CUSTOM_NULL_VALUES = ["", np.inf]
    null_values: list

    def __init__(self, null_values: Optional[list] = None, ignore_na: bool = False) -> None:
        self.ignore_na = ignore_na

        if null_values is None:
            self.null_values = self.CUSTOM_NULL_VALUES

        else:
            self.null_values = null_values

    def _calculate_null_values_stats(self, dataset: pd.DataFrame) -> DataIntegrityNullValues:
        number_of_differently_encoded_nulls = 0
        number_of_null_values = 0

        if not self.ignore_na:
            null_by_pandas = dataset.isnull().sum().sum()

            if null_by_pandas > 0:
                number_of_differently_encoded_nulls += 1
                number_of_null_values += null_by_pandas

        for null_value in self.null_values:
            value_count = (dataset == null_value).sum().sum()

            if value_count > 0:
                number_of_differently_encoded_nulls += 1
                number_of_null_values += value_count

        return DataIntegrityNullValues(
            number_of_differently_encoded_nulls=number_of_differently_encoded_nulls,
            number_of_null_values=number_of_null_values,
        )

    def calculate(self, data: InputData, metrics: dict) -> DataIntegrityNullValuesMetricsResult:
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
