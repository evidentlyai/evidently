import collections
import re
from itertools import combinations
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Pattern
from typing import Tuple
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from dataclasses import dataclass
from dataclasses import fields

from evidently.calculations.data_quality import FeatureQualityStats
from evidently.calculations.data_quality import get_features_stats
# from evidently.calculations.data_quality import DataQualityPlot
from evidently.calculations.data_quality import DataQualityGetPlotData
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import rich_table_data
from evidently.utils.data_operations import process_columns
from evidently.utils.types import Numeric
from evidently.utils.visualizations import plot_distr, plot_num_feature_in_time, plot_cat_feature_in_time, plot_boxes, plot_num_num_rel, plot_cat_cat_rel, plot_time_feature_distr, plot_distr_with_log_button


@dataclass
class NumericCharacteristics:
    count: int
    mean: Optional[Numeric]
    std: Optional[Numeric]
    min: Optional[Numeric]
    p25: Optional[Numeric]
    p50: Optional[Numeric]
    p75: Optional[Numeric]
    max: Optional[Numeric]
    unique: Optional[int]
    unique_percentage: Optional[float]
    missing: Optional[int]
    missing_percentage: Optional[float]
    infinite_count: Optional[int]
    infinite_percentage: Optional[float]
    most_common: Optional[Union[int, float]]
    most_common_percentage: Optional[float]


@dataclass
class CategoricalCharacteristics:
    count: int
    unique: Optional[int]
    unique_percentage: Optional[float]
    most_common: Optional[object]
    most_common_percentage: Optional[float]
    missing: Optional[int]
    missing_percentage: Optional[float]
    new_in_current_values_count: Optional[int] = None
    unused_in_current_values_count: Optional[int] = None


@dataclass
class DatetimeCharacteristics:
    count: int
    unique: Optional[int]
    unique_percentage: Optional[float]
    most_common: Optional[object]
    most_common_percentage: Optional[float]
    missing: Optional[int]
    missing_percentage: Optional[float]
    first: Optional[str]
    last: Optional[str]


ColumnCharacteristics = Union[NumericCharacteristics, CategoricalCharacteristics, DatetimeCharacteristics]


@dataclass
class DataByTarget:
    data_for_plots: Dict[str, Dict[str, Union[list, str, pd.DataFrame]]]
    target_name: str
    target_type: str


@dataclass
class DataQualityPlot:
    bins_for_hist: Dict[str, pd.DataFrame]
    data_in_time: Optional[Dict[str, Union[pd.DataFrame, str]]]
    data_by_target: DataByTarget


@dataclass
class ColumnSummary:
    column_name: str
    column_type: str
    reference_characteristics: Optional[ColumnCharacteristics]
    current_characteristics: ColumnCharacteristics
    plot_data: DataQualityPlot


class ColumnSummaryMetric(Metric[ColumnSummary]):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def calculate(self, data: InputData) -> ColumnSummary:
        columns = process_columns(data.current_data, data.column_mapping)
        # define target type and prediction type. TODO move it to process_columns func
        column_type = None
        if columns.utility_columns.target is not None:
            target_name = columns.utility_columns.target
            if data.column_mapping.task == 'regression' or is_numeric_dtype(data.current_data[target_name]):
                target_type = 'num'
            elif data.column_mapping.task == 'classification' or is_string_dtype(data.current_data[target_name]):
                target_type = 'cat'
            elif data.current_data[columns.utility_columns.target].nunique() <= 5:
                target_type = 'cat'
            else:
                target_type = 'num'
            if target_name == self.column_name:
                column_type = target_type

        if columns.utility_columns.prediction is not None:
            if (
                isinstance(columns.utility_columns.prediction, str)
                and columns.utility_columns.prediction == self.column_name
            ):
                if is_string_dtype(data.current_data[columns.utility_columns.prediction]):
                    column_type = 'cat'
                if is_numeric_dtype(data.current_data[columns.utility_columns.prediction]):
                    column_type = 'num'
            if (
                isinstance(columns.utility_columns.prediction, list)
                and self.column_name in columns.utility_columns.prediction
            ):
                column_type = 'num'
        if self.column_name in columns.num_feature_names:
            column_type = "num"
        elif self.column_name in columns.cat_feature_names:
            column_type = "cat"
        elif (
            self.column_name in columns.datetime_feature_names
            or (columns.utility_columns.date is not None and columns.utility_columns.date == self.column_name)
        ):
            column_type = "datetime"
        if column_type is None:
            raise ValueError(f"column {self.column_name} not in num, cat or datetime features lists")

        reference_data = None
        ref_characteristics = None
        if data.reference_data is not None:
            reference_data = data.reference_data
            ref_characteristics = self.map_data(get_features_stats(data.reference_data[self.column_name], column_type))
        curr_characteristics = self.map_data(get_features_stats(data.current_data[self.column_name], column_type))

        if data.reference_data is not None and column_type == "cat":
            current_values_set = set(data.current_data[self.column_name].unique())
            reference_values_set = set(data.reference_data[self.column_name].unique())
            unique_in_current = current_values_set - reference_values_set
            new_in_current_values_count: int = len(unique_in_current)
            unique_in_reference = reference_values_set - current_values_set
            unused_in_current_values_count: int = len(unique_in_reference)
            if any(pd.isnull(list(unique_in_current))) and any(pd.isnull(list(unique_in_reference))):
                new_in_current_values_count -= 1
                unused_in_current_values_count -= 1

            curr_characteristics.new_in_current_values_count = new_in_current_values_count
            curr_characteristics.unused_in_current_values_count = unused_in_current_values_count

        # plot data
        gpd = DataQualityGetPlotData()
        bins_for_hist = gpd.calculate_main_plot(data.current_data, reference_data, self.column_name,
                                                column_type)
        data_in_time = None
        if columns.utility_columns.date is not None and columns.utility_columns.date != self.column_name:
            data_in_time = gpd.calculate_data_in_time(data.current_data, reference_data, self.column_name,
                                                      column_type, columns.utility_columns.date)
        data_by_target = None
        if (
            columns.utility_columns.target is not None
            and columns.utility_columns.target != self.column_name
            and column_type != 'datetime'
        ):

            data_for_plots = gpd.calculate_data_by_target(data.current_data, reference_data, self.column_name, column_type,
                                                          target_name, target_type)
            data_by_target = DataByTarget(
                data_for_plots=data_for_plots,
                target_name=target_name,
                target_type=target_type
            )

        plot_data = DataQualityPlot(
            bins_for_hist=bins_for_hist,
            data_in_time=data_in_time,
            data_by_target=data_by_target
        )

        return ColumnSummary(
            column_name=self.column_name,
            column_type=column_type,
            reference_characteristics=ref_characteristics,
            current_characteristics=curr_characteristics,
            plot_data=plot_data
        )

    @staticmethod
    def map_data(stats: FeatureQualityStats) -> ColumnCharacteristics:
        if stats.feature_type == "num":
            if isinstance(stats.max, str) or isinstance(stats.min, str):
                raise ValueError("max / min stats should be int or float type, but got str")
            return NumericCharacteristics(
                count=stats.count,
                mean=stats.mean,
                std=stats.std,
                min=stats.min,
                max=stats.max,
                p25=stats.percentile_25,
                p50=stats.percentile_50,
                p75=stats.percentile_75,
                unique=stats.unique_count,
                unique_percentage=stats.unique_percentage,
                missing=stats.missing_count,
                missing_percentage=stats.missing_percentage,
                infinite_count=stats.infinite_count,
                infinite_percentage=stats.infinite_percentage,
                most_common=stats.most_common_value,
                most_common_percentage=stats.most_common_value_percentage,
            )
        if stats.feature_type == "cat":
            return CategoricalCharacteristics(
                count=stats.count,
                unique=stats.unique_count,
                unique_percentage=stats.unique_percentage,
                most_common=stats.most_common_value,
                most_common_percentage=stats.most_common_value_percentage,
                missing=stats.missing_count,
                missing_percentage=stats.missing_percentage,
                # new_categories=[],
            )
        if stats.feature_type == "datetime":
            if not isinstance(stats.min, str) or not isinstance(stats.max, str):
                raise ValueError(f"min / max expected to be str for datetime, got {type(stats.min)}/{type(stats.max)}")
            return DatetimeCharacteristics(
                count=stats.count,
                unique=stats.unique_count,
                unique_percentage=stats.unique_percentage,
                most_common=stats.most_common_value,
                most_common_percentage=stats.most_common_value_percentage,
                missing=stats.missing_count,
                missing_percentage=stats.missing_percentage,
                first=stats.min,
                last=stats.max,
            )
        raise ValueError(f"unknown feature type {stats.feature_type}")


@default_renderer(wrap_type=ColumnSummaryMetric)
class ColumnSummaryMetricRenderer(MetricRenderer):

    def render_html(self, obj: ColumnSummaryMetric) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        column_type = metric_result.column_type
        column_name = metric_result.column_name
        # main plot
        bins_for_hist = metric_result.plot_data.bins_for_hist
        hist_curr = bins_for_hist["current"]
        hist_ref = None
        metrics_values_headers = [""]
        if "reference" in bins_for_hist.keys():
            hist_ref = bins_for_hist["reference"]
            metrics_values_headers = ["current", "reference"]

        if column_type == 'cat':
            fig = plot_distr(hist_curr, hist_ref)
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig = json.loads(fig.to_json())
        if column_type == "num":
            ref_log = None
            if "reference_log" in bins_for_hist.keys():
                ref_log = bins_for_hist["reference_log"]
            fig = plot_distr_with_log_button(hist_curr, bins_for_hist["current_log"], hist_ref, ref_log)
        if column_type == 'datetime':
            fig = plot_time_feature_distr(hist_curr, hist_ref, column_name)

        # additional plots
        additional_graphs = []
        parts = []
        if metric_result.plot_data.data_in_time is not None:
            if column_type == "num":
                feature_in_time_figure = plot_num_feature_in_time(
                    metric_result.plot_data.data_in_time["current"],
                    metric_result.plot_data.data_in_time["reference"],
                    column_name,
                    metric_result.plot_data.data_in_time["datetime_name"],
                    metric_result.plot_data.data_in_time["freq"]
                )
            if column_type == "cat":
                feature_in_time_figure = plot_cat_feature_in_time(
                    metric_result.plot_data.data_in_time["current"],
                    metric_result.plot_data.data_in_time["reference"],
                    column_name,
                    metric_result.plot_data.data_in_time["datetime_name"],
                    metric_result.plot_data.data_in_time["freq"]
                )
            additional_graphs.append(
                AdditionalGraphInfo(
                    column_name + "_in_time",
                    {
                        "data": feature_in_time_figure["data"],
                        "layout": feature_in_time_figure["layout"],
                    },
                )
            )
            parts.append({"title": column_name + " in time", "id": column_name + "_in_time"})

        if metric_result.plot_data.data_by_target is not None:
            ref_data_by_target = None
            if "reference" in metric_result.plot_data.data_by_target.data_for_plots.keys():
                ref_data_by_target = metric_result.plot_data.data_by_target.data_for_plots["reference"]
            target_type = metric_result.plot_data.data_by_target.target_type
            target_name = metric_result.plot_data.data_by_target.target_name
            if column_type == "num" and target_type == "cat":
                feature_by_target_figure = plot_boxes(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    column_name,
                    target_name
                )
            if column_type == "cat" and target_type == "num":
                feature_by_target_figure = plot_boxes(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name
                )
            if column_type == "num" and target_type == "num":
                feature_by_target_figure = plot_num_num_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name
                )
            if column_type == "cat" and target_type == "cat":
                feature_by_target_figure = plot_cat_cat_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name
                )

            additional_graphs.append(
                AdditionalGraphInfo(
                    column_name + "_by_target",
                    {
                        "data": feature_by_target_figure["data"],
                        "layout": feature_by_target_figure["layout"],
                    },
                )
            )
            parts.append({"title": column_name + " by target", "id": column_name + "_by_target"})

        wi = BaseWidgetInfo(
            type="rich_data",
            title="",
            size=2,
            params={
                "header": metric_result.column_name,
                "description": column_type,
                "metricsValuesHeaders": metrics_values_headers,
                "metrics": self._metrics_fot_table(column_type, metric_result),
                "graph": {"data": fig["data"], "layout": fig["layout"]},
                "details": {"parts": parts, "insights": []},
            },
            additionalGraphs=additional_graphs,
        )
        result = [
            MetricHtmlInfo(
                name="",
                info=wi,
            )]
        return result

    @staticmethod
    def _get_stats_with_names(
        stats_list: List[Tuple[str, str, Optional[str]]],
        current_stats: ColumnCharacteristics,
        reference_stats: Optional[ColumnCharacteristics],
    ) -> List[dict]:
        def get_values_as_string(stats_dict, field_name, field_percentage_name) -> str:
            field_value = stats_dict[field_name]

            if field_value is None:
                field_value = ""

            if field_percentage_name is None:
                return str(field_value)

            else:
                return f"{field_value} ({stats_dict[field_percentage_name]}%)"

        result = []
        
        current_stats_dict = {field.name: getattr(current_stats, field.name) for field in fields(current_stats)}

        if reference_stats is None:
            reference_stats_dict = None

        else:
            reference_stats_dict = {field.name: getattr(reference_stats, field.name) for field in fields(reference_stats)}

        for stat_label, stat_field, stat_field_percentage in stats_list:
            values = [get_values_as_string(current_stats_dict, stat_field, stat_field_percentage)]

            if reference_stats_dict is not None:
                values.append(get_values_as_string(reference_stats_dict, stat_field, stat_field_percentage))

            result.append(
                {
                    "label": stat_label,
                    "values": values,
                }
            )
        return result

    def _metrics_fot_table(self, column_type: str, data_quality_results: ColumnSummary):
        current_stats = data_quality_results.current_characteristics

        reference_stats = None

        if data_quality_results.reference_characteristics is not None:
            reference_stats = data_quality_results.reference_characteristics

        metrics = []
        if column_type == 'cat':
            # mapping for category stats: (label, field_name_for_main_value, field_name_for_percentage)
            cat_features = [
                ("count", "count", None),
                ("unique", "unique", "unique_percentage"),
                ("most common", "most_common", "most_common_percentage"),
                ("missing", "missing", "missing_percentage"),
            ]

            if reference_stats:
                cat_features.append(("new categories", "new_in_current_values_count", None))
                cat_features.append(("missing categories", "unused_in_current_values_count", None))

            metrics.extend(self._get_stats_with_names(cat_features, current_stats, reference_stats))

        elif column_type == 'num':
            # mapping for num stats: (label, field_name_for_main_value, field_name_for_percentage)
            num_features = [
                ("count", "count", None),
                ("mean", "mean", None),
                ("std", "std", None),
                ("min", "min", None),
                ("25%", "p25", None),
                ("50%", "p50", None),
                ("75%", "p75", None),
                ("max", "max", None),
                ("unique", "unique", "unique_percentage"),
                ("most common", "most_common", "most_common_percentage"),
                ("missing", "missing", "missing_percentage"),
                ("infinite", "infinite_count", "infinite_percentage"),
            ]
            metrics.extend(self._get_stats_with_names(num_features, current_stats, reference_stats))

        elif column_type == 'datetime':
            # mapping for datetime stats: (label, field_name_for_main_value, field_name_for_percentage)
            datetime_features = [
                ("count", "count", None),
                ("unique", "unique", "unique_percentage"),
                ("most common", "most_common", "most_common_percentage"),
                ("missing", "missing", "missing_percentage"),
                ("first", "first", None),
                ("last", "last", None),
            ]
            metrics.extend(self._get_stats_with_names(datetime_features, current_stats, reference_stats))

        return metrics



        # result = [
        #     MetricHtmlInfo(
        #         name="data_integrity_null_values_title",
        #         info=rich_table_data(label="Data Integrity Metric: Null Values Statistic"),
        #     ),
            
        # ]

        # if metric_result.reference_null_values is not None:
        #     result.append(self._get_table_stat(dataset_name="reference", stats=metric_result.reference_null_values))

        


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
