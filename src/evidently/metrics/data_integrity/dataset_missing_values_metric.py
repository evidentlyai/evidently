from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


@dataclass
class DataIntegrityNullValuesStat:
    """Statistics about null values in a dataset"""

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
    current_null_values: DataIntegrityNullValuesStat
    reference_null_values: Optional[DataIntegrityNullValuesStat] = None


class DatasetMissingValuesMetric(Metric[DataIntegrityNullValuesMetricsResult]):
    """Count missing values in a dataset.

    Missing value is a null or NaN value.

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

    def _calculate_null_values_stats(self, dataset: pd.DataFrame) -> DataIntegrityNullValuesStat:
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

        return DataIntegrityNullValuesStat(
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

    def calculate(self, data: InputData) -> DataIntegrityNullValuesMetricsResult:
        if not self.null_values:
            raise ValueError("Null-values list should not be empty.")

        current_null_values = self._calculate_null_values_stats(data.current_data)

        if data.reference_data is not None:
            reference_null_values: Optional[DataIntegrityNullValuesStat] = self._calculate_null_values_stats(
                data.reference_data
            )

        else:
            reference_null_values = None

        return DataIntegrityNullValuesMetricsResult(
            current_null_values=current_null_values,
            reference_null_values=reference_null_values,
        )


@default_renderer(wrap_type=DatasetMissingValuesMetric)
class DataIntegrityNullValuesMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetMissingValuesMetric) -> dict:
        return dataclasses.asdict(obj.get_result().current_null_values)

    @staticmethod
    def _get_table_stat(dataset_name: str, stats: DataIntegrityNullValuesStat) -> BaseWidgetInfo:
        matched_stat = [(k, v) for k, v in stats.number_of_nulls_by_column.items()]
        matched_stat_headers = ["Value", "Count"]
        return table_data(
            title=f"{dataset_name.capitalize()}: Nulls Statistic",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def render_html(self, obj: DatasetMissingValuesMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        number_of_nulls = metric_result.current_null_values.number_of_nulls

        result = [
            header_text(label="Data Integrity Metric: Null Values Statistic"),
            header_text(label=f"In current dataset {number_of_nulls} null values."),
            self._get_table_stat(dataset_name="current", stats=metric_result.current_null_values),
        ]

        if metric_result.reference_null_values is not None:
            result.append(self._get_table_stat(dataset_name="reference", stats=metric_result.reference_null_values))

        return result
