from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently import TaskType
from evidently.calculations.data_quality import DataQualityStats
from evidently.calculations.data_quality import calculate_correlations
from evidently.calculations.data_quality import calculate_data_quality_stats
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_task
from evidently.utils.visualizations import plot_distr


@dataclass
class DataQualityMetricsResults:
    columns: DatasetColumns
    features_stats: DataQualityStats
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]
    counts_of_values: Dict[str, Dict[str, pd.DataFrame]]
    correlations: Optional[Dict[str, pd.DataFrame]] = None
    reference_features_stats: Optional[DataQualityStats] = None


class DataQualityMetrics(Metric[DataQualityMetricsResults]):
    def calculate(self, data: InputData) -> DataQualityMetricsResults:
        if data.current_data is None:
            raise ValueError("Current dataset should be present")

        columns = process_columns(data.current_data, data.column_mapping)
        target_name = columns.utility_columns.target

        if data.column_mapping.task is None:
            if target_name is None:
                task = None

            else:
                if data.reference_data is None:
                    data_for_task_detection = data.current_data

                else:
                    data_for_task_detection = data.reference_data

                task = recognize_task(target_name, data_for_task_detection)

        else:
            task = data.column_mapping.task

        current_features_stats = calculate_data_quality_stats(data.current_data, columns, task)
        current_correlations = calculate_correlations(data.current_data, current_features_stats, target_name)
        reference_features_stats = None

        if data.reference_data is not None:
            reference_features_stats = calculate_data_quality_stats(data.reference_data, columns, task)

        # data for visualisation
        if data.reference_data is not None:
            reference_data = data.reference_data

        else:
            reference_data = None

        distr_for_plots = {}
        counts_of_values = {}
        target_prediction_columns = []

        if isinstance(columns.utility_columns.target, str):
            target_prediction_columns.append(columns.utility_columns.target)

        if isinstance(columns.utility_columns.prediction, str):
            target_prediction_columns.append(columns.utility_columns.prediction)

        num_columns = columns.num_feature_names
        cat_columns = columns.cat_feature_names

        if task == TaskType.REGRESSION_TASK:
            num_columns.extend(target_prediction_columns)

        if task == TaskType.CLASSIFICATION_TASK:
            cat_columns.extend(target_prediction_columns)

        for feature in num_columns:
            counts_of_value_feature = {}
            curr_feature = data.current_data[feature]
            current_counts = data.current_data[feature].value_counts(dropna=False).reset_index()
            current_counts.columns = ["x", "count"]
            counts_of_value_feature["current"] = current_counts

            ref_feature = None

            if reference_data is not None:
                ref_feature = reference_data[feature]

                reference_counts = ref_feature.value_counts(dropna=False).reset_index()
                reference_counts.columns = ["x", "count"]
                counts_of_value_feature["reference"] = reference_counts

            counts_of_values[feature] = counts_of_value_feature
            distr_for_plots[feature] = make_hist_for_num_plot(curr_feature, ref_feature)

        for feature in cat_columns:
            curr_feature = data.current_data[feature]
            ref_feature = None
            if reference_data is not None:
                ref_feature = reference_data[feature]
            counts_of_values[feature] = make_hist_for_cat_plot(curr_feature, ref_feature)
            distr_for_plots[feature] = counts_of_values[feature]

        return DataQualityMetricsResults(
            columns=columns,
            features_stats=current_features_stats,
            distr_for_plots=distr_for_plots,
            counts_of_values=counts_of_values,
            correlations=current_correlations,
            reference_features_stats=reference_features_stats,
        )


@default_renderer(wrap_type=DataQualityMetrics)
class DataQualityMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("distr_for_plots", None)
        result.pop("counts_of_values", None)
        result.pop("correlations", None)
        return result

    @staticmethod
    def _get_data_quality_summary_table(metric_result: DataQualityMetricsResults) -> MetricHtmlInfo:
        headers = ["Quality Metric", "Current"]
        target_name = str(metric_result.columns.utility_columns.target)
        date_column = metric_result.columns.utility_columns.date

        all_features = metric_result.columns.get_all_features_list(cat_before_num=True, include_datetime_feature=True)

        if date_column:
            all_features = [date_column] + all_features

        number_of_variables = str(len(all_features))
        categorical_features = str(len(metric_result.columns.cat_feature_names))
        numeric_features = str(len(metric_result.columns.num_feature_names))
        datetime_features = str(len(metric_result.columns.datetime_feature_names))

        stats: List[List[str]] = [
            ["target column", target_name, target_name],
            ["date column", str(date_column), str(date_column)],
            ["number of variables", number_of_variables, number_of_variables],
            [
                "number of observations",
                str(metric_result.features_stats.rows_count),
                str(metric_result.reference_features_stats and metric_result.reference_features_stats.rows_count),
            ],
            [
                "categorical features",
                categorical_features,
                categorical_features,
            ],
            [
                "numeric features",
                numeric_features,
                numeric_features,
            ],
            [
                "datetime features",
                datetime_features,
                datetime_features,
            ],
        ]

        if metric_result.reference_features_stats is not None:
            headers.append("Reference")

        else:
            # remove reference values from stats
            stats = [item[:2] for item in stats]

        return MetricHtmlInfo(
            "data_quality_summary_table",
            table_data(title="Data Summary", column_names=headers, data=stats),
        )

    @staticmethod
    def _get_data_quality_distribution_graph(
        features_stat: Dict[str, Dict[str, pd.DataFrame]],
    ) -> List[MetricHtmlInfo]:
        result = []

        for column_name, stat in features_stat.items():
            curr_distr = stat["current"]
            ref_distr = stat.get("reference")
            fig = plot_distr(curr_distr, ref_distr)

            result.append(
                MetricHtmlInfo(
                    f"data_quality_{column_name}",
                    plotly_figure(title=f"Column: {column_name}", figure=fig),
                )
            )
        return result

    def render_html(self, obj: DataQualityMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        result = [
            MetricHtmlInfo(
                "data_quality_title",
                header_text(label="Data Quality Report"),
            ),
            self._get_data_quality_summary_table(metric_result=metric_result),
        ]
        result.extend(self._get_data_quality_distribution_graph(features_stat=metric_result.distr_for_plots))
        return result


@dataclass
class DataQualityStabilityMetricsResults:
    number_not_stable_target: Optional[int] = None
    number_not_stable_prediction: Optional[int] = None


class DataQualityStabilityMetrics(Metric[DataQualityStabilityMetricsResults]):
    """Calculates stability by target and prediction"""

    def calculate(self, data: InputData) -> DataQualityStabilityMetricsResults:
        result = DataQualityStabilityMetricsResults()
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        columns = [column for column in data.current_data.columns if column not in (target_name, prediction_name)]

        if not columns:
            result.number_not_stable_target = 0
            result.number_not_stable_prediction = 0
            return result

        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]

        if target_name in data.current_data:
            result.number_not_stable_target = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]

        if prediction_name in data.current_data:
            result.number_not_stable_prediction = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [prediction_name], keep=False)].index
            ).shape[0]

        return result


@default_renderer(wrap_type=DataQualityStabilityMetrics)
class DataQualityStabilityMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityStabilityMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())

    def render_html(self, obj: DataQualityStabilityMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        result = [
            MetricHtmlInfo(
                "data_quality_stability_title",
                header_text(label="Data Stability Metrics"),
            ),
            MetricHtmlInfo(
                "data_quality_stability_info",
                counter(
                    counters=[
                        CounterData("Not stable target", str(metric_result.number_not_stable_target)),
                        CounterData("Not stable prediction", str(metric_result.number_not_stable_prediction)),
                    ]
                ),
            ),
        ]
        return result


@dataclass
class DataQualityValueListMetricsResults:
    column_name: str
    number_in_list: int
    number_not_in_list: int
    share_in_list: float
    share_not_in_list: float
    counts_of_value: Dict[str, pd.DataFrame]
    rows_count: int
    values: List[str]


class DataQualityValueListMetrics(Metric[DataQualityValueListMetricsResults]):
    """Calculates count and shares of values in the predefined values list"""

    column_name: str
    values: Optional[list]

    def __init__(self, column_name: str, values: Optional[list] = None) -> None:
        self.values = values
        self.column_name = column_name

    def calculate(self, data: InputData) -> DataQualityValueListMetricsResults:
        if self.values is None:
            if data.reference_data is None:
                raise ValueError("Reference or values list should be present")
            self.values = data.reference_data[self.column_name].unique()

        rows_count = data.current_data.shape[0]
        values_in_list = data.current_data[self.column_name].isin(self.values).sum()
        number_not_in_list = rows_count - values_in_list
        counts_of_value = {}
        current_counts = data.current_data[self.column_name].value_counts(dropna=False).reset_index()
        current_counts.columns = ["x", "count"]
        counts_of_value["current"] = current_counts

        if data.reference_data is not None and self.values is not None:
            reference_counts = data.reference_data[self.column_name].value_counts(dropna=False).reset_index()
            reference_counts.columns = ["x", "count"]
            counts_of_value["reference"] = reference_counts

        return DataQualityValueListMetricsResults(
            column_name=self.column_name,
            number_in_list=values_in_list,
            number_not_in_list=rows_count - values_in_list,
            share_in_list=values_in_list / rows_count,
            share_not_in_list=number_not_in_list / rows_count,
            counts_of_value=counts_of_value,
            rows_count=rows_count,
            values=[str(value) for value in self.values],
        )


@default_renderer(wrap_type=DataQualityValueListMetrics)
class DataQualityValueListMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueListMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("counts_of_value", None)
        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, metrics: DataQualityValueListMetricsResults) -> MetricHtmlInfo:
        matched_stat = [
            ("Values from the list", metrics.number_in_list),
            ("Share from the list", np.round(metrics.share_in_list, 3)),
            ("Values not in the list", metrics.number_not_in_list),
            ("Share not in the list", np.round(metrics.share_not_in_list, 3)),
            ("Rows count", metrics.rows_count),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return MetricHtmlInfo(
            name=f"data_quality_values_list_stat_{dataset_name.lower()}",
            info=table_data(
                title=f"{dataset_name.capitalize()}: Values list statistic",
                column_names=matched_stat_headers,
                data=matched_stat,
            ),
        )

    def render_html(self, obj: DataQualityValueListMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        values_list_info = ",".join(metric_result.values)
        result = [
            MetricHtmlInfo(
                "data_quality_values_list_title",
                header_text(label=f"Data Value List Metrics for the column: {metric_result.column_name}"),
            ),
            MetricHtmlInfo(
                "data_quality_values_list_info",
                header_text(label=f"Values: {values_list_info}"),
            ),
            self._get_table_stat(dataset_name="current", metrics=metric_result),
        ]
        return result


@dataclass
class DataQualityValueRangeMetricsResults:
    column_name: str
    range_left_value: float
    range_right_value: float
    number_in_range: int
    number_not_in_range: int
    share_in_range: float
    share_not_in_range: float
    distr_for_plot: Dict[str, pd.DataFrame]
    rows_count: int
    ref_min: Optional[float] = None
    ref_max: Optional[float] = None


class DataQualityValueRangeMetrics(Metric[DataQualityValueRangeMetricsResults]):
    """Calculates count and shares of values in the predefined values range"""

    column_name: str
    left: Optional[float]
    right: Optional[float]

    def __init__(self, column_name: str, left: Optional[float] = None, right: Optional[float] = None) -> None:
        self.left = left
        self.right = right
        self.column_name = column_name

    def calculate(self, data: InputData) -> DataQualityValueRangeMetricsResults:
        if (self.left is None or self.right is None) and data.reference_data is None:
            raise ValueError("Reference should be present")

        ref_min = None
        ref_max = None

        if data.reference_data is not None:
            ref_min = data.reference_data[self.column_name].min()
            ref_max = data.reference_data[self.column_name].max()

        if self.left is None and data.reference_data is not None:
            self.left = ref_min

        if self.right is None and data.reference_data is not None:
            self.right = ref_max

        rows_count = data.current_data[self.column_name].dropna().shape[0]

        if self.left is None or self.right is None:
            raise ValueError("Cannot define one or both of range parameters")

        number_in_range = (
            data.current_data[self.column_name]
            .dropna()
            .between(left=float(self.left), right=float(self.right), inclusive="both")
            .sum()
        )
        number_not_in_range = rows_count - number_in_range

        # visualisation
        curr_feature = data.current_data[self.column_name]

        ref_feature = None
        if data.reference_data is not None:
            ref_feature = data.reference_data[self.column_name]

        distr_for_plot = make_hist_for_num_plot(curr_feature, ref_feature)

        return DataQualityValueRangeMetricsResults(
            column_name=self.column_name,
            range_left_value=self.left,
            range_right_value=self.right,
            number_in_range=number_in_range,
            number_not_in_range=number_not_in_range,
            share_in_range=number_in_range / rows_count,
            share_not_in_range=number_not_in_range / rows_count,
            distr_for_plot=distr_for_plot,
            rows_count=rows_count,
            ref_min=ref_min,
            ref_max=ref_max,
        )


@default_renderer(wrap_type=DataQualityValueRangeMetrics)
class DataQualityValueRangeMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueRangeMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("distr_for_plot", None)
        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, metrics: DataQualityValueRangeMetricsResults) -> MetricHtmlInfo:
        matched_stat = [
            ("Values from the range", metrics.number_in_range),
            ("Share from the range", np.round(metrics.share_in_range, 3)),
            ("Values not in the range", metrics.number_not_in_range),
            ("Share not in the range", np.round(metrics.share_not_in_range, 3)),
            ("Rows count", metrics.rows_count),
        ]

        matched_stat_headers = ["Metric", "Value"]
        return MetricHtmlInfo(
            name=f"data_quality_values_range_stat_{dataset_name.lower()}",
            info=table_data(
                title=f"{dataset_name.capitalize()}: Values statistic",
                column_names=matched_stat_headers,
                data=matched_stat,
            ),
        )

    def render_html(self, obj: DataQualityValueRangeMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        left = metric_result.range_left_value
        right = metric_result.range_right_value
        result = [
            MetricHtmlInfo(
                "data_quality_value_range_title",
                header_text(label=f"Data Value Range Metrics for the column: {column_name}"),
            ),
            MetricHtmlInfo(
                "data_quality_value_range_title",
                header_text(label=f"Range is from {left} to {right}"),
            ),
            self._get_table_stat(dataset_name="current", metrics=metric_result),
        ]
        return result


@dataclass
class DataQualityValueQuantileMetricsResults:
    column_name: str
    # calculated value of the quantile
    value: float
    # range of the quantile (from 0 to 1)
    quantile: float
    distr_for_plot: Dict[str, pd.DataFrame]
    ref_value: Optional[float]


class DataQualityValueQuantileMetrics(Metric[DataQualityValueQuantileMetricsResults]):
    """Calculates quantile with specified range"""

    column_name: str
    quantile: float

    def __init__(self, column_name: str, quantile: float) -> None:
        if quantile is not None:
            if not 0 <= quantile <= 1:
                raise ValueError("Quantile should all be in the interval [0, 1].")

        self.column_name = column_name
        self.quantile = quantile

    def calculate(self, data: InputData) -> DataQualityValueQuantileMetricsResults:
        curr_feature = data.current_data[self.column_name]
        ref_feature = None
        ref_value = None

        if data.reference_data is not None:
            ref_feature = data.reference_data[self.column_name]
            ref_value = data.reference_data[self.column_name].quantile(self.quantile)

        distr_for_plot = make_hist_for_num_plot(curr_feature, ref_feature)
        return DataQualityValueQuantileMetricsResults(
            column_name=self.column_name,
            value=data.current_data[self.column_name].quantile(self.quantile),
            quantile=self.quantile,
            distr_for_plot=distr_for_plot,
            ref_value=ref_value,
        )


@default_renderer(wrap_type=DataQualityValueQuantileMetrics)
class DataQualityValueQuantileMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityValueQuantileMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("distr_for_plot", None)
        return result

    def render_html(self, obj: DataQualityValueQuantileMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()
        column_name = metric_result.column_name
        counters = [
            CounterData.float(label="Quantile", value=metric_result.quantile, precision=3),
            CounterData.float(label="Current dataset value", value=metric_result.value, precision=3),
        ]

        if metric_result.ref_value:
            counters.append(
                CounterData.float(label="Reference dataset value", value=metric_result.ref_value, precision=3),
            )

        result = [
            MetricHtmlInfo(
                "data_quality_value_quantile_title",
                header_text(label=f"Data Value Quantile Metrics for the column: {column_name}"),
            ),
            MetricHtmlInfo(
                "data_quality_value_quantile_stat",
                counter(counters=counters),
            ),
        ]
        return result


@dataclass
class DataCorrelation:
    num_features: Optional[List[str]]
    correlation_matrix: pd.DataFrame
    target_prediction_correlation: Optional[float] = None
    abs_max_target_features_correlation: Optional[float] = None
    abs_max_prediction_features_correlation: Optional[float] = None
    abs_max_correlation: Optional[float] = None
    abs_max_num_features_correlation: Optional[float] = None


@dataclass
class DataQualityCorrelationMetricsResults:
    current: DataCorrelation
    reference: Optional[DataCorrelation]


class DataQualityCorrelationMetrics(Metric[DataQualityCorrelationMetricsResults]):
    """Calculate different correlations with target, predictions and features"""

    method: str

    def __init__(self, method: str = "pearson") -> None:
        self.method = method

    def _get_correlations(
        self,
        dataset: pd.DataFrame,
        target_name: Optional[str],
        prediction_name: Optional[Union[str, Sequence[str]]],
        num_features: Optional[List[str]],
        is_classification_task: bool,
    ) -> DataCorrelation:
        correlation_matrix = dataset.corr(method=self.method)
        correlation_matrix_for_plot = correlation_matrix.copy()
        # fill diagonal with 1 values for getting abs max values
        np.fill_diagonal(correlation_matrix.values, 0)

        if num_features is None:
            num_features = [i for i in correlation_matrix if i not in [target_name, prediction_name]]

        if prediction_name in correlation_matrix and target_name in correlation_matrix:
            target_prediction_correlation = correlation_matrix.loc[prediction_name, target_name]

        else:
            target_prediction_correlation = None

        if target_name in correlation_matrix:
            abs_max_target_features_correlation = correlation_matrix.loc[target_name, num_features].abs().max()

        else:
            abs_max_target_features_correlation = None

        if prediction_name in correlation_matrix:
            abs_max_prediction_features_correlation = correlation_matrix.loc[prediction_name, num_features].abs().max()

        else:
            abs_max_prediction_features_correlation = None

        if is_classification_task is not None:
            corr_features = num_features

        else:
            corr_features = num_features + [target_name, prediction_name]

        abs_max_correlation = correlation_matrix.loc[corr_features, corr_features].abs().max().max()

        abs_max_num_features_correlation = correlation_matrix.loc[num_features, num_features].abs().max().max()

        return DataCorrelation(
            num_features=num_features,
            correlation_matrix=correlation_matrix_for_plot,
            target_prediction_correlation=target_prediction_correlation,
            abs_max_target_features_correlation=abs_max_target_features_correlation,
            abs_max_prediction_features_correlation=abs_max_prediction_features_correlation,
            abs_max_correlation=abs_max_correlation,
            abs_max_num_features_correlation=abs_max_num_features_correlation,
        )

    def calculate(self, data: InputData) -> DataQualityCorrelationMetricsResults:
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        num_features: Optional[List[str]] = data.column_mapping.numerical_features
        is_classification_task = data.column_mapping.is_classification_task()

        current_correlations = self._get_correlations(
            dataset=data.current_data,
            target_name=target_name,
            prediction_name=prediction_name,
            num_features=num_features,
            is_classification_task=is_classification_task,
        )

        if data.reference_data is not None:
            reference_correlation: Optional[DataCorrelation] = self._get_correlations(
                dataset=data.reference_data,
                target_name=target_name,
                prediction_name=prediction_name,
                num_features=num_features,
                is_classification_task=is_classification_task,
            )

        else:
            reference_correlation = None

        return DataQualityCorrelationMetricsResults(
            current=current_correlations,
            reference=reference_correlation,
        )


@default_renderer(wrap_type=DataQualityCorrelationMetrics)
class DataQualityCorrelationMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityCorrelationMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result["current"].pop("correlation_matrix", None)

        if result["reference"]:
            result["reference"].pop("correlation_matrix", None)

        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, correlation: DataCorrelation) -> MetricHtmlInfo:
        matched_stat = [
            ("Abs max correlation", np.round(correlation.abs_max_correlation, 3)),
            ("Abs max num features correlation", np.round(correlation.abs_max_num_features_correlation, 3)),
        ]
        if correlation.abs_max_target_features_correlation is not None:
            matched_stat.append(
                ("Abs max target features correlation", np.round(correlation.abs_max_target_features_correlation, 3))
            )
        if correlation.abs_max_prediction_features_correlation is not None:
            matched_stat.append(
                (
                    "Abs max prediction features correlation",
                    np.round(correlation.abs_max_prediction_features_correlation, 3),
                )
            )

        matched_stat_headers = ["Metric", "Value"]
        return MetricHtmlInfo(
            name=f"data_quality_correlation_stat_{dataset_name.lower()}",
            info=table_data(
                title=f"{dataset_name.capitalize()}: Correlation statistic",
                column_names=matched_stat_headers,
                data=matched_stat,
            ),
        )

    def render_html(self, obj: DataQualityCorrelationMetrics) -> List[MetricHtmlInfo]:
        metric_result = obj.get_result()

        result = [
            MetricHtmlInfo(
                "data_quality_correlation_title",
                header_text(label="Data Correlation Metrics"),
            ),
            self._get_table_stat(dataset_name="current", correlation=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_table_stat(dataset_name="reference", correlation=metric_result.reference))

        return result
