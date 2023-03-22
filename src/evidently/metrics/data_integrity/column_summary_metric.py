import json
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype

from evidently.base_metric import ColumnMetric
from evidently.base_metric import ColumnMetricResult
from evidently.base_metric import InputData
from evidently.base_metric import MetricResultField
from evidently.calculations.data_quality import DataQualityGetPlotData
from evidently.calculations.data_quality import FeatureQualityStats
from evidently.calculations.data_quality import get_features_stats
from evidently.core import ColumnType
from evidently.features.non_letter_character_percentage_feature import NonLetterCharacterPercentage
from evidently.features.OOV_words_percentage_feature import OOVWordsPercentage
from evidently.features.text_length_feature import TextLength
from evidently.metric_results import Histogram
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.data_operations import process_columns
from evidently.utils.data_preprocessing import DataDefinition
from evidently.utils.types import Numeric
from evidently.utils.visualizations import plot_boxes
from evidently.utils.visualizations import plot_cat_cat_rel
from evidently.utils.visualizations import plot_cat_feature_in_time
from evidently.utils.visualizations import plot_distr
from evidently.utils.visualizations import plot_distr_with_log_button
from evidently.utils.visualizations import plot_num_feature_in_time
from evidently.utils.visualizations import plot_num_num_rel
from evidently.utils.visualizations import plot_time_feature_distr


class ColumnCharacteristics(MetricResultField):
    number_of_rows: int
    count: int
    missing: Optional[int]
    missing_percentage: Optional[float]


class NumericCharacteristics(ColumnCharacteristics):
    mean: Optional[Numeric]
    std: Optional[Numeric]
    min: Optional[Numeric]
    p25: Optional[Numeric]
    p50: Optional[Numeric]
    p75: Optional[Numeric]
    max: Optional[Numeric]
    unique: Optional[int]
    unique_percentage: Optional[float]
    infinite_count: Optional[int]
    infinite_percentage: Optional[float]
    most_common: Optional[Union[int, float]]
    most_common_percentage: Optional[float]


class CategoricalCharacteristics(ColumnCharacteristics):
    unique: Optional[int]
    unique_percentage: Optional[float]
    most_common: Optional[object]
    most_common_percentage: Optional[float]
    new_in_current_values_count: Optional[int] = None
    unused_in_current_values_count: Optional[int] = None


class DatetimeCharacteristics(ColumnCharacteristics):
    unique: Optional[int]
    unique_percentage: Optional[float]
    most_common: Optional[object]
    most_common_percentage: Optional[float]
    first: Optional[str]
    last: Optional[str]


class TextCharacteristics(ColumnCharacteristics):
    text_length_min: Optional[float]
    text_length_mean: Optional[float]
    text_length_max: Optional[float]
    oov_min: Optional[float]
    oov_mean: Optional[float]
    oov_max: Optional[float]
    non_letter_char_min: Optional[float]
    non_letter_char_mean: Optional[float]
    non_letter_char_max: Optional[float]


class DataInTime(MetricResultField):
    data_for_plots: Dict[str, Optional[pd.DataFrame]]
    freq: str
    datetime_name: str


class DataByTarget(MetricResultField):
    data_for_plots: Union[
        Dict[
            str,
            Union[
                Dict[str, Union[list, pd.DataFrame, np.ndarray, pd.Categorical]],
                pd.DataFrame,
            ],
        ],
        None,
    ]
    target_name: str
    target_type: str


class DataQualityPlot(MetricResultField):
    class Config:
        dict_include = False

    bins_for_hist: Optional[Histogram]
    data_in_time: Optional[DataInTime]
    data_by_target: Optional[DataByTarget]
    counts_of_values: Optional[Dict[str, pd.DataFrame]]


class ColumnSummaryResult(ColumnMetricResult):
    class Config:
        pd_exclude_fields = {"plot_data"}
        pd_name_mapping = {
            "reference_characteristics": "ref",
            "current_characteristics": "cur",
        }

    reference_characteristics: Optional[ColumnCharacteristics]
    current_characteristics: ColumnCharacteristics
    plot_data: DataQualityPlot


class ColumnSummaryMetric(ColumnMetric[ColumnSummaryResult]):
    generated_text_features: Optional[Dict[str, Union[TextLength, NonLetterCharacterPercentage, OOVWordsPercentage]]]

    def __init__(self, column_name: str):
        self.column_name = column_name
        self.generated_text_features = None

    def required_features(self, data_definition: DataDefinition):
        column_type = data_definition.get_column(self.column_name).column_type
        if column_type == ColumnType.Text:
            self.generated_text_features = {
                "text_length": TextLength(self.column_name),
                "non_letter_char": NonLetterCharacterPercentage(self.column_name),
                "oov": OOVWordsPercentage(self.column_name),
            }
            return list(self.generated_text_features.values())
        return []

    def get_parameters(self) -> tuple:
        return (self.column_name,)

    @staticmethod
    def acceptable_types() -> List[ColumnType]:
        return [ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text]

    def calculate(self, data: InputData) -> ColumnSummaryResult:
        columns = process_columns(data.current_data, data.column_mapping)

        if self.column_name not in data.current_data:
            raise ValueError(f"Column '{self.column_name}' not found in current dataset.")

        if data.reference_data is not None and self.column_name not in data.reference_data:
            raise ValueError(f"Column '{self.column_name}' not found in reference dataset.")

        column_type = None
        target_name = columns.utility_columns.target
        target_type = None
        data_by_target = None

        # define target type and prediction type. TODO move it to process_columns func
        if columns.utility_columns.target is not None:
            reg_condition = data.column_mapping.task == "regression" or (
                is_numeric_dtype(data.current_data[target_name])
                and columns.task != "classification"
                and data.current_data[target_name].nunique() > 5
            )
            if reg_condition:
                target_type = "num"
            else:
                target_type = "cat"
            if target_name == self.column_name:
                column_type = target_type

        if columns.utility_columns.prediction is not None:
            if (
                isinstance(columns.utility_columns.prediction, str)
                and columns.utility_columns.prediction == self.column_name
            ):
                if (
                    is_string_dtype(data.current_data[columns.utility_columns.prediction])
                    or (
                        is_numeric_dtype(data.current_data[columns.utility_columns.prediction])
                        and columns.task != "classification"
                        and data.current_data[columns.utility_columns.prediction].nunique() < 5
                    )
                    or (
                        is_numeric_dtype(data.current_data[columns.utility_columns.prediction])
                        and columns.task == "classification"
                        and (
                            data.current_data[columns.utility_columns.prediction].max() > 1
                            or data.current_data[columns.utility_columns.prediction].min() < 0
                        )
                    )
                ):
                    column_type = "cat"
                else:
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
        elif self.column_name in columns.text_feature_names:
            column_type = "text"
        if column_type is None:
            raise ValueError(f"column {self.column_name} not in num, cat, text or datetime features lists")

        curr_characteristics: ColumnCharacteristics
        reference_data = None
        ref_characteristics: Optional[ColumnCharacteristics] = None
        if column_type == "text" and self.generated_text_features is not None:
            if data.reference_data is not None:
                ref_characteristics = self.get_text_stats(
                    "reference",
                    data,
                    data.reference_data[self.column_name],
                    self.generated_text_features,
                )
            curr_characteristics = self.get_text_stats(
                "current",
                data,
                data.current_data[self.column_name],
                self.generated_text_features,
            )
        else:
            if data.reference_data is not None:
                reference_data = data.reference_data
                ref_characteristics = self.map_data(
                    get_features_stats(data.reference_data[self.column_name], column_type)
                )
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
            if data.reference_data is not None:
                reference_counts = data.reference_data[self.column_name].value_counts(dropna=False).reset_index()
                reference_counts.columns = ["x", "count"]
                counts_of_values["reference"] = reference_counts.head(10)

        plot_data = DataQualityPlot(
            bins_for_hist=bins_for_hist,
            data_in_time=data_in_time,
            data_by_target=data_by_target,
            counts_of_values=counts_of_values,
        )

        return ColumnSummaryResult(
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

    def get_text_stats(
        self, dataset: str, data: InputData, text_feature: pd.Series, generated_text_features: dict
    ) -> TextCharacteristics:
        number_of_rows = len(text_feature)
        missing = text_feature.isna().sum()
        if dataset == "current":
            text_length = data.get_current_column(generated_text_features["text_length"].feature_name())
            oov = data.get_current_column(generated_text_features["oov"].feature_name())
            non_letter_char = data.get_current_column(generated_text_features["non_letter_char"].feature_name())
        else:
            text_length = data.get_reference_column(generated_text_features["text_length"].feature_name())
            oov = data.get_reference_column(generated_text_features["oov"].feature_name())
            non_letter_char = data.get_reference_column(generated_text_features["non_letter_char"].feature_name())

        return TextCharacteristics(
            number_of_rows=number_of_rows,
            count=text_feature.count(),
            missing=missing,
            missing_percentage=np.round(missing / number_of_rows, 3),
            text_length_min=text_length.min(),
            text_length_mean=np.round(text_length.mean(), 3),
            text_length_max=text_length.max(),
            oov_min=np.round(oov.min(), 3),
            oov_mean=np.round(oov.mean(), 3),
            oov_max=np.round(oov.max(), 3),
            non_letter_char_min=np.round(non_letter_char.min(), 3),
            non_letter_char_mean=np.round(non_letter_char.mean(), 3),
            non_letter_char_max=np.round(non_letter_char.max(), 3),
        )


@default_renderer(wrap_type=ColumnSummaryMetric)
class ColumnSummaryMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnSummaryMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        column_type = metric_result.column_type
        column_name = metric_result.column_name
        # main plot
        bins_for_hist: Histogram = metric_result.plot_data.bins_for_hist
        if bins_for_hist is not None:
            hist_curr = bins_for_hist.current
            hist_ref = None
            metrics_values_headers = [""]
            if bins_for_hist.reference is not None:
                hist_ref = bins_for_hist.reference
                metrics_values_headers = ["current", "reference"]

            if column_type == "cat":
                fig = plot_distr(
                    hist_curr=hist_curr,
                    hist_ref=hist_ref,
                    color_options=self.color_options,
                )
                fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig = json.loads(fig.to_json())
            if column_type == "num":
                if bins_for_hist.current_log is None:
                    raise ValueError("current_log should be present for num columns")
                ref_log = bins_for_hist.reference_log
                fig = plot_distr_with_log_button(
                    hist_curr,
                    bins_for_hist.current_log,
                    hist_ref,
                    ref_log,
                    color_options=self.color_options,
                )
            if column_type == "datetime":
                fig = plot_time_feature_distr(hist_curr, hist_ref, color_options=self.color_options)
            graph = {"data": fig["data"], "layout": fig["layout"]}
        else:
            graph = {}
            metrics_values_headers = [""]
            if metric_result.reference_characteristics is not None:
                metrics_values_headers = ["current", "reference"]

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
                    color_options=self.color_options,
                )
            if column_type == "cat":
                feature_in_time_figure = plot_cat_feature_in_time(
                    metric_result.plot_data.data_in_time.data_for_plots["current"],
                    metric_result.plot_data.data_in_time.data_for_plots["reference"],
                    column_name,
                    metric_result.plot_data.data_in_time.datetime_name,
                    metric_result.plot_data.data_in_time.freq,
                    color_options=self.color_options,
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

        if (
            metric_result.plot_data.data_by_target is not None
            and metric_result.plot_data.data_by_target.data_for_plots is not None
        ):
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
                    self.color_options,
                )
            if column_type == "cat" and target_type == "num":
                feature_by_target_figure = plot_boxes(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
                    self.color_options,
                )
            if column_type == "num" and target_type == "num":
                feature_by_target_figure = plot_num_num_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
                    color_options=self.color_options,
                )
            if column_type == "cat" and target_type == "cat":
                feature_by_target_figure = plot_cat_cat_rel(
                    metric_result.plot_data.data_by_target.data_for_plots["current"],
                    ref_data_by_target,
                    target_name,
                    column_name,
                    color_options=self.color_options,
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
        if column_type == "text":
            wi = BaseWidgetInfo(
                type="rich_data",
                title="",
                size=2,
                params={
                    "header": metric_result.column_name,
                    "description": column_type,
                    "metricsValuesHeaders": metrics_values_headers,
                    "metrics": self._metrics_fot_table(column_type, metric_result),
                    # "graph": graph,
                    "details": {"parts": parts, "insights": []},
                },
                additionalGraphs=additional_graphs,
            )
        else:
            wi = BaseWidgetInfo(
                type="rich_data",
                title="",
                size=2,
                params={
                    "header": metric_result.column_name,
                    "description": column_type,
                    "metricsValuesHeaders": metrics_values_headers,
                    "metrics": self._metrics_fot_table(column_type, metric_result),
                    "graph": graph,
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

        current_stats_dict = {field: getattr(current_stats, field) for field in current_stats.__fields__}

        if reference_stats is None:
            reference_stats_dict = None

        else:
            reference_stats_dict = {field: getattr(reference_stats, field) for field in reference_stats.__fields__}

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

    def _metrics_fot_table(self, column_type: str, data_quality_results: ColumnSummaryResult):
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

        elif column_type == "text":
            text_features = [
                ("count", "count", None),
                ("missing", "missing", "missing_percentage"),
                ("Text Length min", "text_length_min", None),
                ("Text Length mean", "text_length_mean", None),
                ("Text Length max", "text_length_max", None),
                ("OOV % min", "oov_min", None),
                ("OOV % mean", "oov_mean", None),
                ("OOV % max", "oov_max", None),
                ("Non Letter Character % min", "non_letter_char_min", None),
                ("Non Letter Character % mean", "non_letter_char_mean", None),
                ("Non Letter Character % max", "non_letter_char_max", None),
            ]
            metrics.extend(self._get_stats_with_names(text_features, current_stats, reference_stats))

        return metrics
