from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_quality import get_rows_count
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import HistogramData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import histogram
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs


@dataclass
class DatasetMissingValues:
    """Statistics about missed values in a dataset"""

    # set of different missed values in the dataset
    different_nulls: Dict[Any, int]
    # number of different missed values in the dataset
    number_of_different_nulls: int
    # set of different missed values for each column
    different_nulls_by_column: Dict[str, Dict[Any, int]]
    # count of different missed values for each column
    number_of_different_nulls_by_column: Dict[str, int]
    # count of missed values in all dataset
    number_of_missed_values: int
    # share of missed values in all dataset
    share_of_missed_values: float
    # count of missed values for each column
    number_of_nulls_by_column: Dict[str, int]
    # share of missed values for each column
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
class DatasetMissingValuesMetricResult:
    current: DatasetMissingValues
    reference: Optional[DatasetMissingValues] = None


class DatasetMissingValuesMetric(Metric[DatasetMissingValuesMetricResult]):
    """Count missing values in a dataset.

    Missing value is a null or NaN value.

    Calculate an amount of missed values kinds and count for such values.
    NA-types like numpy.NaN, pandas.NaT are counted as one type.

    You can set you own missed values list with `values` parameter.
    Value `None` in the list means that Pandas null values will be included in the calculation.

    If `replace` parameter is False - add defaults to user's list.
    If `replace` parameter is True - use values from `values` list only.
    """

    # default missed values list
    DEFAULT_MISSED_VALUES = ["", np.inf, -np.inf, None]
    values: frozenset

    def __init__(self, values: Optional[list] = None, replace: bool = True) -> None:
        if values is None:
            # use default missed values list if we have no user-defined values
            values = self.DEFAULT_MISSED_VALUES

        elif not replace:
            # add default values to the user-defined list
            values = self.DEFAULT_MISSED_VALUES + values

        # use frozenset because metrics parameters should be immutable/hashable for deduplication
        self.values = frozenset(values)

    def _calculate_missed_values_stats(self, dataset: pd.DataFrame) -> DatasetMissingValues:
        different_nulls = {value: 0 for value in self.values}
        columns_with_nulls = set()
        number_of_nulls = 0
        number_of_nulls_by_column: Dict[str, int] = {}
        different_nulls_by_column: Dict[str, Dict[Any, int]] = {}

        for column_name in dataset.columns:
            number_of_nulls_by_column[column_name] = 0
            different_nulls_by_column[column_name] = {}

            for value in self.values:
                different_nulls_by_column[column_name][value] = 0

        number_of_rows_with_nulls = 0
        number_of_columns = len(dataset.columns)
        number_of_rows = get_rows_count(dataset)

        for column_name in dataset.columns:
            # iterate by each value in custom missed values list and check the value in a column
            for null_value in self.values:
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
            for null_value in self.values:
                if None in self.values and row.isnull().any():
                    # check pandas null values
                    number_of_rows_with_nulls += 1
                    break

                elif null_value in row.values:
                    number_of_rows_with_nulls += 1
                    break

        if number_of_rows == 0:
            share_of_nulls_by_column = {}
            share_of_rows_with_nulls = 0.0
            share_of_missed_values = 0.0

        else:
            share_of_nulls_by_column = {
                column_name: value / number_of_rows for column_name, value in number_of_nulls_by_column.items()
            }
            share_of_missed_values = number_of_nulls / (number_of_columns * number_of_rows)
            share_of_rows_with_nulls = number_of_rows_with_nulls / number_of_rows

        number_of_different_nulls_by_column = {}

        for column_name, nulls in different_nulls_by_column.items():
            # count a number of missed values that have a value in the column
            number_of_different_nulls_by_column[column_name] = len(
                {keys for keys, values in nulls.items() if values > 0}
            )

        number_of_columns_with_nulls = len(columns_with_nulls)
        number_of_different_nulls = len({k for k in different_nulls if different_nulls[k] > 0})

        if number_of_columns == 0:
            share_of_columns_with_nulls = 0.0

        else:
            share_of_columns_with_nulls = number_of_columns_with_nulls / number_of_columns

        return DatasetMissingValues(
            different_nulls=different_nulls,
            number_of_different_nulls=number_of_different_nulls,
            different_nulls_by_column=different_nulls_by_column,
            number_of_different_nulls_by_column=number_of_different_nulls_by_column,
            number_of_missed_values=number_of_nulls,
            share_of_missed_values=share_of_missed_values,
            number_of_nulls_by_column=number_of_nulls_by_column,
            share_of_nulls_by_column=share_of_nulls_by_column,
            number_of_rows=number_of_rows,
            number_of_rows_with_nulls=number_of_rows_with_nulls,
            share_of_rows_with_nulls=share_of_rows_with_nulls,
            number_of_columns=number_of_columns,
            columns_with_nulls=sorted(columns_with_nulls),
            number_of_columns_with_nulls=len(columns_with_nulls),
            share_of_columns_with_nulls=share_of_columns_with_nulls,
        )

    def calculate(self, data: InputData) -> DatasetMissingValuesMetricResult:
        if not self.values:
            raise ValueError("Null-values list should not be empty.")

        current_null_values = self._calculate_missed_values_stats(data.current_data)

        if data.reference_data is not None:
            reference_null_values: Optional[DatasetMissingValues] = self._calculate_missed_values_stats(
                data.reference_data
            )

        else:
            reference_null_values = None

        return DatasetMissingValuesMetricResult(
            current=current_null_values,
            reference=reference_null_values,
        )


@default_renderer(wrap_type=DatasetMissingValuesMetric)
class DatasetMissingValuesMetricRenderer(MetricRenderer):
    def render_json(self, obj: DatasetMissingValuesMetric) -> dict:
        return dataclasses.asdict(obj.get_result().current)

    def _get_table_stat(self, dataset_name: str, stats: DatasetMissingValues) -> BaseWidgetInfo:
        matched_stat = [(k, v) for k, v in stats.number_of_nulls_by_column.items()]
        matched_stat = sorted(matched_stat, key=lambda x: x[1], reverse=True)
        matched_stat_headers = ["Value", "Count"]
        table_tab = table_data(
            title="",
            column_names=matched_stat_headers,
            data=matched_stat,
        )
        histogram_tab = histogram(
            title="",
            primary_hist=HistogramData(
                name="",
                x=list(stats.number_of_nulls_by_column.keys()),
                y=list(stats.number_of_nulls_by_column.values()),
            ),
            color_options=self.color_options,
        )
        return widget_tabs(
            title=f"{dataset_name.capitalize()} dataset",
            tabs=[
                TabData(title="Table", widget=table_tab),
                TabData(
                    title="Histogram",
                    widget=histogram_tab,
                ),
            ],
        )

    @staticmethod
    def _get_info_string(stats: DatasetMissingValues) -> str:
        percents = round(stats.share_of_missed_values * 100, 3)
        return f"{stats.number_of_missed_values} ({percents}%)"

    def _get_overall_missing_values_info(self, metric_result: DatasetMissingValuesMetricResult) -> BaseWidgetInfo:
        counters = [
            CounterData.string("Missing values (Current data)", self._get_info_string(metric_result.current)),
        ]
        if metric_result.reference is not None:
            counters.append(
                CounterData.string("Missing values (Reference data)", self._get_info_string(metric_result.reference)),
            )

        return counter(
            title="",
            counters=counters,
        )

    def render_html(self, obj: DatasetMissingValuesMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Dataset Missing Values"),
            self._get_overall_missing_values_info(metric_result),
            self._get_table_stat(dataset_name="current", stats=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_table_stat(dataset_name="reference", stats=metric_result.reference))

        return result
