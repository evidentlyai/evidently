from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from dataclasses import dataclass
from plotly import graph_objs as go

from evidently import TaskType
from evidently.calculations.data_quality import DataQualityStats
from evidently.calculations.data_quality import calculate_correlations
from evidently.calculations.data_quality import calculate_data_quality_stats
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
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
from evidently.utils.visualizations import make_hist_for_cat_plot
from evidently.utils.visualizations import make_hist_for_num_plot


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
        current_correlations = calculate_correlations(data.current_data, columns)
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
    def _get_data_quality_summary_table(metric_result: DataQualityMetricsResults) -> BaseWidgetInfo:
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

        return table_data(title="Data Summary", column_names=headers, data=stats)

    def plot_distr(self, hist_curr, hist_ref=None, orientation="v"):
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="current",
                x=hist_curr["x"],
                y=hist_curr["count"],
                marker_color=self.color_options.get_current_data_color(),
                orientation=orientation,
            )
        )
        if hist_ref is not None:
            fig.add_trace(
                go.Bar(
                    name="reference",
                    x=hist_ref["x"],
                    y=hist_ref["count"],
                    marker_color=self.color_options.get_reference_data_color(),
                    orientation=orientation,
                )
            )

        return fig

    def _get_data_quality_distribution_graph(
        self,
        features_stat: Dict[str, Dict[str, pd.DataFrame]],
    ) -> List[BaseWidgetInfo]:
        result = []

        for column_name, stat in features_stat.items():
            curr_distr = stat["current"]
            ref_distr = stat.get("reference")
            fig = self.plot_distr(curr_distr, ref_distr)

            result.append(plotly_figure(title=f"Column: {column_name}", figure=fig))
        return result

    def render_html(self, obj: DataQualityMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Data Quality Report"),
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

    def render_html(self, obj: DataQualityStabilityMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Data Stability Metrics"),
            counter(
                counters=[
                    CounterData("Not stable target", str(metric_result.number_not_stable_target)),
                    CounterData("Not stable prediction", str(metric_result.number_not_stable_prediction)),
                ]
            ),
        ]
        return result
