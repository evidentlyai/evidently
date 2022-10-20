import json
from itertools import combinations
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass
from dataclasses import fields
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype

from evidently.calculations.data_integration import get_number_of_empty_columns
from evidently.calculations.data_quality import DataQualityGetPlotData
from evidently.calculations.data_quality import FeatureQualityStats
from evidently.calculations.data_quality import get_features_stats
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import rich_table_data
from evidently.renderers.html_widgets import table_data
from evidently.utils.data_operations import process_columns
from evidently.utils.types import Numeric
from evidently.utils.visualizations import plot_boxes
from evidently.utils.visualizations import plot_cat_cat_rel
from evidently.utils.visualizations import plot_cat_feature_in_time
from evidently.utils.visualizations import plot_distr
from evidently.utils.visualizations import plot_distr_with_log_button
from evidently.utils.visualizations import plot_num_feature_in_time
from evidently.utils.visualizations import plot_num_num_rel
from evidently.utils.visualizations import plot_time_feature_distr


@dataclass
class NumericCharacteristics:
    number_of_rows: int
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
    number_of_rows: int
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
    number_of_rows: int
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
class DataInTime:
    data_for_plots: Dict[str, pd.DataFrame]
    freq: str
    datetime_name: str


@dataclass
class DataByTarget:
    data_for_plots: Dict[str, Dict[str, Union[list, pd.DataFrame]]]
    target_name: str
    target_type: str


@dataclass
class DataQualityPlot:
    bins_for_hist: Dict[str, pd.DataFrame]
    data_in_time: Optional[DataInTime]
    data_by_target: Optional[DataByTarget]
    counts_of_values: Optional[Dict[str, pd.DataFrame]]


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
        if self.column_name not in data.current_data.columns:
            raise ValueError(f"{self.column_name} not in current data")
        column_type = None
        target_name = columns.utility_columns.target
        target_type = None
        data_by_target = None
        if columns.utility_columns.target is not None:
            if data.column_mapping.task == "regression" or is_numeric_dtype(data.current_data[target_name]):
                target_type = "num"
            elif data.column_mapping.task == "classification" or is_string_dtype(data.current_data[target_name]):
                target_type = "cat"
            elif data.current_data[columns.utility_columns.target].nunique() <= 5:
                target_type = "cat"
            else:
                target_type = "num"
            if target_name == self.column_name:
                column_type = target_type

        if columns.utility_columns.prediction is not None:
            if (
                isinstance(columns.utility_columns.prediction, str)
                and columns.utility_columns.prediction == self.column_name
            ):
                if is_string_dtype(data.current_data[columns.utility_columns.prediction]):
                    column_type = "cat"
                if is_numeric_dtype(data.current_data[columns.utility_columns.prediction]):
                    column_type = "num"
            if (
                isinstance(columns.utility_columns.prediction, list)
                and self.column_name in columns.utility_columns.prediction
            ):
                column_type = "num"
        if self.column_name in columns.num_feature_names:
            column_type = "num"
        elif self.column_name in columns.cat_feature_names:
            column_type = "cat"
        elif self.column_name in columns.datetime_feature_names or (
            columns.utility_columns.date is not None and columns.utility_columns.date == self.column_name
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
            if not isinstance(curr_characteristics, CategoricalCharacteristics):
                raise ValueError(f"{self.column_name} should be categorical")
            curr_characteristics.new_in_current_values_count = new_in_current_values_count
            curr_characteristics.unused_in_current_values_count = unused_in_current_values_count

        # plot data
        gpd = DataQualityGetPlotData()
        bins_for_hist = gpd.calculate_main_plot(data.current_data, reference_data, self.column_name, column_type)
        data_in_time = None
        if (
            columns.utility_columns.date is not None
            and columns.utility_columns.date != self.column_name
            and column_type != "datetime"
        ):
            data_in_time = gpd.calculate_data_in_time(
                data.current_data,
                reference_data,
                self.column_name,
                column_type,
                columns.utility_columns.date,
            )
            data_in_time = DataInTime(
                data_for_plots={
                    "current": data_in_time["current"],
                    "reference": data_in_time["reference"],
                },
                freq=data_in_time["freq"],
                datetime_name=data_in_time["datetime_name"],
            )

        if (
            target_name is not None
            and target_type is not None
            and columns.utility_columns.target != self.column_name
            and column_type != "datetime"
        ):

            data_for_plots = gpd.calculate_data_by_target(
                data.current_data,
                reference_data,
                self.column_name,
                column_type,
                target_name,
                target_type,
            )
            data_by_target = DataByTarget(
                data_for_plots=data_for_plots,
                target_name=target_name,
                target_type=target_type,
            )
        counts_of_values = None
        if column_type in ["cat", "num"]:
            counts_of_values = {}
            current_counts = data.current_data[self.column_name].value_counts(dropna=False).reset_index()
            current_counts.columns = ["x", "count"]
            counts_of_values["current"] = current_counts.head(10)
            if reference_data is not None:
                reference_counts = data.reference_data[self.column_name].value_counts(dropna=False).reset_index()
                reference_counts.columns = ["x", "count"]
                counts_of_values["reference"] = reference_counts.head(10)

        plot_data = DataQualityPlot(
            bins_for_hist=bins_for_hist,
            data_in_time=data_in_time,
            data_by_target=data_by_target,
            counts_of_values=counts_of_values,
        )

        return ColumnSummary(
            column_name=self.column_name,
            column_type=column_type,
            reference_characteristics=ref_characteristics,
            current_characteristics=curr_characteristics,
            plot_data=plot_data,
        )

    @staticmethod
    def map_data(stats: FeatureQualityStats) -> ColumnCharacteristics:
        if stats.feature_type == "num":
            if isinstance(stats.max, str) or isinstance(stats.min, str) or isinstance(stats.most_common_value, str):
                raise ValueError("max / min stats should be int or float type, but got str")
            return NumericCharacteristics(
                number_of_rows=stats.number_of_rows,
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
                number_of_rows=stats.number_of_rows,
                count=stats.count,
                unique=stats.unique_count,
                unique_percentage=stats.unique_percentage,
                most_common=stats.most_common_value,
                most_common_percentage=stats.most_common_value_percentage,
                missing=stats.missing_count,
                missing_percentage=stats.missing_percentage,
            )
        if stats.feature_type == "datetime":
            if not isinstance(stats.min, str) or not isinstance(stats.max, str):
                raise ValueError(f"min / max expected to be str for datetime, got {type(stats.min)}/{type(stats.max)}")
            return DatetimeCharacteristics(
                number_of_rows=stats.number_of_rows,
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
    def render_html(self, obj: ColumnSummaryMetric) -> List[BaseWidgetInfo]:
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

        if column_type == "cat":
            fig = plot_distr(hist_curr, hist_ref)
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig = json.loads(fig.to_json())
        if column_type == "num":
            ref_log = None
            if "reference_log" in bins_for_hist.keys():
                ref_log = bins_for_hist["reference_log"]
            fig = plot_distr_with_log_button(hist_curr, bins_for_hist["current_log"], hist_ref, ref_log)
        if column_type == "datetime":
            fig = plot_time_feature_distr(hist_curr, hist_ref, column_name)

        # additional plots
        additional_graphs = []
        parts = []
        if metric_result.plot_data.data_in_time is not None:
            if column_type == "num":
                feature_in_time_figure = plot_num_feature_in_time(
                    metric_result.plot_data.data_in_time.data_for_plots["current"],
                    metric_result.plot_data.data_in_time.data_for_plots["reference"],
                    column_name,
                    metric_result.plot_data.data_in_time.datetime_name,
                    metric_result.plot_data.data_in_time.freq,
                )
            if column_type == "cat":
                feature_in_time_figure = plot_cat_feature_in_time(
                    metric_result.plot_data.data_in_time.data_for_plots["current"],
                    metric_result.plot_data.data_in_time.data_for_plots["reference"],
                    column_name,
                    metric_result.plot_data.data_in_time.datetime_name,
                    metric_result.plot_data.data_in_time.freq,
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
                    target_name,
                )
            if column_type == "cat" and target_type == "num":
                feature_by_target_figure = plot_boxes(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
                )
            if column_type == "num" and target_type == "num":
                feature_by_target_figure = plot_num_num_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
                )
            if column_type == "cat" and target_type == "cat":
                feature_by_target_figure = plot_cat_cat_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
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
        return [wi]

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
            reference_stats_dict = {
                field.name: getattr(reference_stats, field.name) for field in fields(reference_stats)
            }

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
        if column_type == "cat":
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

        elif column_type == "num":
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

        elif column_type == "datetime":
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
            number_of_empty_columns=get_number_of_empty_columns(dataset),
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
    def _get_metrics_table(dataset_name: str, metrics: DataIntegrityMetricsValues) -> BaseWidgetInfo:
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

        return table_data(column_names=headers, data=stats)

    def render_html(self, obj: DataIntegrityMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()

        result = [
            header_text(label="Data Integrity"),
            self._get_metrics_table(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        return result
