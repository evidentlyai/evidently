import collections
import re
from itertools import combinations
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Pattern

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import WidgetType
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


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
    current: DataIntegrityMetricsValues
    reference: Optional[DataIntegrityMetricsValues] = None


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    @staticmethod
    def _get_integrity_metrics_values(dataset: pd.DataFrame, columns: tuple) -> DataIntegrityMetricsValues:
        counts_of_values = {}

        for column_name in dataset.columns:
            feature = dataset[column_name]
            df_counts = feature.value_counts(dropna=False).reset_index()
            df_counts.columns = ["x", "count"]
            counts_of_values[column_name] = df_counts

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

    def calculate(self, data: InputData) -> DataIntegrityMetricsResults:
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
                columns.extend(features)

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
        current = self._get_integrity_metrics_values(curr_data, current_columns)

        if data.reference_data is not None:
            reference_columns = np.intersect1d(columns, data.reference_data.columns)
            ref_data = data.reference_data[reference_columns]
            reference: Optional[DataIntegrityMetricsValues] = self._get_integrity_metrics_values(
                ref_data, reference_columns
            )

        else:
            reference = None

        return DataIntegrityMetricsResults(current=current, reference=reference)


@default_renderer(wrap_type=DataIntegrityMetrics)
class DataIntegrityMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataIntegrityMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        if "current" in result:
            result["current"].pop("counts_of_values", None)

            result["current"]["columns_type"] = [str(t) for t in result["current"]["columns_type"]]

        if "reference" in result and result["reference"]:
            result["reference"].pop("counts_of_values", None)
            result["reference"]["columns_type"] = [str(t) for t in result["reference"]["columns_type"]]

        return result

    @staticmethod
    def _get_metrics_table(dataset_name: str, metrics: DataIntegrityMetricsValues) -> MetricHtmlInfo:
        headers = ("Quality Metric", "Value")
        stats = (
            ("Number of columns", metrics.number_of_columns),
            ("Number of rows", metrics.number_of_rows),
            ("Number of NaNs", metrics.number_of_nans),
            ("Number of columns with NaNs", metrics.number_of_columns_with_nans),
            ("Number of rows with NaNs", metrics.number_of_rows_with_nans),
            ("Number of constant columns", metrics.number_of_constant_columns),
            ("Number of empty rows", metrics.number_of_empty_rows),
            ("Number of empty columns", metrics.number_of_empty_columns),
            ("Number of duplicated rows", metrics.number_of_duplicated_rows),
            ("Number of duplicated columns", metrics.number_of_duplicated_columns),
        )

        return MetricHtmlInfo(
            f"data_integrity_metrics_table_{dataset_name.lower()}",
            table_data(column_names=headers, data=stats),
        )

    def render_html(self, obj: DataIntegrityMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()

        result = [
            MetricHtmlInfo(
                "data_integrity_title",
                header_text(label="Data Integrity"),
            ),
            self._get_metrics_table(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        return result


@dataclass
class DataIntegrityValueByRegexpStat:
    """Statistics about matched by a regular expression values in a column for one dataset"""

    # count of matched values in the column, without NaNs
    number_of_matched: int
    # count of not matched values in the column, without NaNs
    number_of_not_matched: int
    # count of rows in the column, including matched, not matched and NaNs
    number_of_rows: int
    # map with matched values (keys) and count of the values (value)
    table_of_matched: Dict[str, int]
    # map with not matched values (keys) and count of the values (values)
    table_of_not_matched: Dict[str, int]


@dataclass
class DataIntegrityValueByRegexpMetricResult:
    # name of the column that we check by the regular expression
    column_name: str
    # the regular expression as a string
    reg_exp: str
    # match statistic for current dataset
    current: DataIntegrityValueByRegexpStat
    # match statistic for reference dataset, equals None if the reference is not present
    reference: Optional[DataIntegrityValueByRegexpStat] = None


class DataIntegrityValueByRegexpMetrics(Metric[DataIntegrityValueByRegexpMetricResult]):
    """Count number of values in a column matched or not by a regular expression (regexp)"""

    # name of the column that we check
    column_name: str
    # the regular expression
    reg_exp: str
    # compiled regular expression for speed optimization
    _reg_exp_compiled: Pattern

    def __init__(self, column_name: str, reg_exp: str):
        self.reg_exp = reg_exp
        self.column_name = column_name
        self._reg_exp_compiled = re.compile(reg_exp)

    def _calculate_stats_by_regexp(self, column: pd.Series) -> DataIntegrityValueByRegexpStat:
        number_of_matched = 0
        number_of_na = 0
        number_of_not_matched = 0
        table_of_matched: Dict[str, int] = collections.defaultdict(int)
        table_of_not_matched: Dict[str, int] = collections.defaultdict(int)

        for item in column:
            if pd.isna(item):
                number_of_na += 1
                continue

            item = str(item)

            if bool(self._reg_exp_compiled.match(str(item))):
                number_of_matched += 1
                table_of_matched[item] += 1

            else:
                number_of_not_matched += 1
                table_of_not_matched[item] += 1

        return DataIntegrityValueByRegexpStat(
            number_of_matched=number_of_matched,
            number_of_not_matched=number_of_not_matched,
            number_of_rows=column.shape[0],
            table_of_matched=dict(table_of_matched),
            table_of_not_matched=dict(table_of_not_matched),
        )

    def calculate(self, data: InputData) -> DataIntegrityValueByRegexpMetricResult:
        current = self._calculate_stats_by_regexp(data.current_data[self.column_name])
        reference = None

        if data.reference_data is not None:
            if self.column_name not in data.reference_data:
                raise ValueError(f"Column {self.column_name} was not found in reference dataset.")

            reference = self._calculate_stats_by_regexp(data.reference_data[self.column_name])

        return DataIntegrityValueByRegexpMetricResult(
            column_name=self.column_name, reg_exp=self.reg_exp, current=current, reference=reference
        )


@default_renderer(wrap_type=DataIntegrityValueByRegexpMetrics)
class DataIntegrityValueByRegexpMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataIntegrityValueByRegexpMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_table_stat(dataset_name: str, metrics: DataIntegrityValueByRegexpStat) -> MetricHtmlInfo:
        matched_stat = [(f"{k} (matched)", v) for k, v in metrics.table_of_matched.items()]
        matched_stat += [(f"{k} (not matched)", v) for k, v in metrics.table_of_not_matched.items()]
        matched_stat += [
            ("NaN", metrics.number_of_rows - metrics.number_of_matched - metrics.number_of_not_matched),
            ("Total", metrics.number_of_rows),
        ]
        matched_stat_headers = ["Value", "Count"]
        return MetricHtmlInfo(
            name=f"data_integrity_value_by_regexp_stats_{dataset_name.lower()}",
            info=table_data(
                title=f"{dataset_name.capitalize()}: Match Statistics",
                column_names=matched_stat_headers,
                data=matched_stat,
            ),
        )

    def render_html(self, obj: DataIntegrityValueByRegexpMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        number_of_matched = metric_result.current.number_of_matched
        number_of_rows = metric_result.current.number_of_rows

        result = [
            MetricHtmlInfo(
                name="data_integrity_value_by_regexp_title",
                info=counter(
                    title="Data Integrity Metric: Values Matching By Regexp In a Column",
                    counters=[
                        CounterData(
                            label="",
                            value=f"Founded {number_of_matched} of {number_of_rows} with "
                            f"regexp '{metric_result.reg_exp}' in "
                            f"column '{metric_result.column_name}' in current dataset.",
                        )
                    ],
                ),
            ),
            self._get_table_stat(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_table_stat(dataset_name="reference", metrics=metric_result.reference))

        return result


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


@default_renderer(wrap_type=DataIntegrityNullValuesMetrics)
class DataIntegrityNullValuesMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataIntegrityNullValuesMetrics) -> dict:
        return dataclasses.asdict(obj.get_result().current_null_values)

    @staticmethod
    def _get_table_stat(dataset_name: str, stats: DataIntegrityNullValuesStat) -> MetricHtmlInfo:
        matched_stat = [(k, v) for k, v in stats.number_of_nulls_by_column.items()]
        matched_stat_headers = ["Value", "Count"]
        return MetricHtmlInfo(
            name=f"data_integrity_null_values_stats_{dataset_name.lower()}",
            info=table_data(
                title=f"{dataset_name.capitalize()}: Nulls Statistic",
                column_names=matched_stat_headers,
                data=matched_stat,
            ),
        )

    def render_html(self, obj: DataIntegrityNullValuesMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        number_of_nulls = metric_result.current_null_values.number_of_nulls

        result = [
            MetricHtmlInfo(
                name="data_integrity_null_values_title",
                info=header_text(label="Data Integrity Metric: Null Values Statistic"),
            ),
            MetricHtmlInfo(
                name="data_integrity_null_values_title",
                info=header_text(label=f"In current dataset {number_of_nulls} null values."),
            ),
            self._get_table_stat(dataset_name="current", stats=metric_result.current_null_values),
        ]

        if metric_result.reference_null_values is not None:
            result.append(self._get_table_stat(dataset_name="reference", stats=metric_result.reference_null_values))

        return result
