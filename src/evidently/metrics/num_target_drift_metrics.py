from typing import List
from typing import Optional
from typing import Sequence

import dataclasses
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from dataclasses import dataclass

from evidently.calculations.data_drift import DataDriftMetrics
from evidently.calculations.data_drift import calculate_data_drift_for_numeric_feature
from evidently.calculations.data_quality import get_rows_count
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.options import ColorOptions
from evidently.options import DataDriftOptions
from evidently.options import QualityMetricsOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_data
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


@dataclass
class NumTargetDriftAnalyzerResults:
    columns: DatasetColumns
    target_output_distr: Optional[dict] = None
    prediction_output_distr: Optional[dict] = None
    target_values_plot: Optional[dict] = None
    prediction_values_plot: Optional[dict] = None
    reference_data_count: int = 0
    current_data_count: int = 0
    target_metrics: Optional[DataDriftMetrics] = None
    prediction_metrics: Optional[DataDriftMetrics] = None


class NumTargetDriftMetrics(Metric[NumTargetDriftAnalyzerResults]):
    def __init__(
        self,
        options: Optional[DataDriftOptions] = None,
        quality_metrics_options: Optional[QualityMetricsOptions] = None,
    ):
        if options is None:
            options = DataDriftOptions()
        self.options = options
        if quality_metrics_options is None:
            quality_metrics_options = QualityMetricsOptions()
        self.quality_metrics_options = quality_metrics_options

    def get_parameters(self) -> tuple:
        return ()

    def calculate(self, data: InputData) -> NumTargetDriftAnalyzerResults:
        """Calculate the target and prediction drifts.

        With default options, uses a two sample Kolmogorov-Smirnov test at a 0.95 confidence level.

        Notes:
            You can also provide a custom function that computes a statistic by adding special
            `DataDriftOptions` object to the `option_provider` of the class.::

                options = DataDriftOptions(num_target_stattest_func=...)
                analyzer.options_prover.add(options)

            Such a function takes two arguments:::

                def(reference_data: pd.Series, current_data: pd.Series):
                   ...

            and returns arbitrary number (like a p_value from the other tests ;-))
        Args:
            data: data for metric calculations.
        Returns:
            A dictionary that contains some meta information as well as `metrics` for either target or prediction
            columns or both. The `*_drift` column in `metrics` contains a computed p_value from tests.
        Raises:
            ValueError when target or predictions columns are not numerical.
        """
        if data.reference_data is None:
            raise ValueError("reference_data should be present")

        if data.current_data is None:
            raise ValueError("current_data should be present")

        columns = process_columns(data.reference_data, data.column_mapping)
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        if not isinstance(target_column, str) and isinstance(columns.utility_columns.target, Sequence):
            raise ValueError("target should not be a sequence")

        if not isinstance(prediction_column, str) and isinstance(prediction_column, Sequence):
            raise ValueError("prediction should not be a sequence")

        if set(columns.num_feature_names) - set(data.current_data.columns):
            raise ValueError(
                f"Some numerical features in current data {data.current_data.columns}"
                f"are not present in columns.num_feature_names"
            )

        result = NumTargetDriftAnalyzerResults(
            columns=columns,
            reference_data_count=get_rows_count(data.reference_data),
            current_data_count=get_rows_count(data.current_data),
        )

        threshold = self.options.num_target_threshold

        if target_column is not None:
            result.target_metrics = calculate_data_drift_for_numeric_feature(
                current_data=data.current_data,
                reference_data=data.reference_data,
                column_name=target_column,
                numeric_columns=columns.num_feature_names,
                stattest=self.options.num_target_stattest_func,
                threshold=threshold,
            )
            result.target_output_distr = _dist_plot(
                target_column,
                data.reference_data,
                data.current_data,
                self.quality_metrics_options,
                ColorOptions(),
            )
            result.target_values_plot = _values_plots(
                columns.utility_columns.date,
                target_column,
                "target",
                data.reference_data,
                data.current_data,
                ColorOptions(),
                self.quality_metrics_options,
            )

        if prediction_column is not None:
            result.prediction_metrics = calculate_data_drift_for_numeric_feature(
                current_data=data.current_data,
                reference_data=data.reference_data,
                column_name=prediction_column,
                numeric_columns=columns.num_feature_names,
                stattest=self.options.num_target_stattest_func,
                threshold=threshold,
            )
            result.prediction_output_distr = _dist_plot(
                prediction_column,
                data.reference_data,
                data.current_data,
                self.quality_metrics_options,
                ColorOptions(),
            )
            result.prediction_values_plot = _values_plots(
                columns.utility_columns.date,
                prediction_column,
                "prediction",
                data.reference_data,
                data.current_data,
                ColorOptions(),
                self.quality_metrics_options,
            )

        return result


def _dist_plot(
    column_name: str,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    quality_metrics_options: QualityMetricsOptions,
    color_options: ColorOptions,
):
    cut_quantile = quality_metrics_options.cut_quantile
    quantile = quality_metrics_options.get_cut_quantile(column_name)
    if cut_quantile and quantile is not None:
        side, q = quantile
        cqt = CutQuantileTransformer(side=side, q=q)
        cqt.fit(reference_data[column_name])
        reference_data_to_plot = cqt.transform(reference_data[column_name])
        current_data_to_plot = cqt.transform(current_data[column_name])
    else:
        reference_data_to_plot = reference_data[column_name]
        current_data_to_plot = current_data[column_name]

    output_distr = ff.create_distplot(
        [reference_data_to_plot, current_data_to_plot],
        ["Reference", "Current"],
        colors=[color_options.get_reference_data_color(), color_options.get_current_data_color()],
        show_rug=True,
    )

    output_distr.update_layout(
        xaxis_title="Value",
        yaxis_title="Share",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return output_distr.to_plotly_json()


def _values_plots(
    date_column: Optional[str],
    column_name: str,
    kind: str,
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    color_options: ColorOptions,
    quality_metrics_options: QualityMetricsOptions,
):
    conf_interval_n_sigmas = quality_metrics_options.conf_interval_n_sigmas
    utility_columns_date = date_column
    # plot values
    reference_mean = np.mean(reference_data[column_name])
    reference_std = np.std(reference_data[column_name], ddof=1)
    x_title = "Timestamp" if utility_columns_date else "Index"

    output_values = go.Figure()

    output_values.add_trace(
        go.Scattergl(
            x=reference_data[utility_columns_date] if utility_columns_date else reference_data.index,
            y=reference_data[column_name],
            mode="markers",
            name="Reference",
            marker=dict(size=6, color=color_options.get_reference_data_color()),
        )
    )

    output_values.add_trace(
        go.Scattergl(
            x=current_data[utility_columns_date] if utility_columns_date else current_data.index,
            y=current_data[column_name],
            mode="markers",
            name="Current",
            marker=dict(size=6, color=color_options.get_current_data_color()),
        )
    )

    if utility_columns_date:
        x0 = current_data[utility_columns_date].sort_values()[1]
    else:
        x0 = current_data.index.sort_values()[1]

    output_values.add_trace(
        go.Scatter(
            x=[x0, x0],
            y=[
                reference_mean - conf_interval_n_sigmas * reference_std,
                reference_mean + conf_interval_n_sigmas * reference_std,
            ],
            mode="markers",
            name="Current",
            marker=dict(size=0.01, color=color_options.non_visible_color, opacity=0.005),
            showlegend=False,
        )
    )

    output_values.update_layout(
        xaxis_title=x_title,
        yaxis_title=kind.title() + " Value",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        shapes=[
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="paper",
                # y-reference is assigned to the plot paper [0,1]
                yref="y",
                x0=0,
                y0=reference_mean - conf_interval_n_sigmas * reference_std,
                x1=1,
                y1=reference_mean + conf_interval_n_sigmas * reference_std,
                fillcolor=color_options.fill_color,
                opacity=0.5,
                layer="below",
                line_width=0,
            ),
            dict(
                type="line",
                name="Reference",
                xref="paper",
                yref="y",
                x0=0,  # min(testset_agg_by_date.index),
                y0=reference_mean,
                x1=1,  # max(testset_agg_by_date.index),
                y1=reference_mean,
                line=dict(color=color_options.zero_line_color, width=3),
            ),
        ],
    )

    return output_values.to_plotly_json()


@default_renderer(wrap_type=NumTargetDriftMetrics)
class NumTargetDriftMetricsRenderer(MetricRenderer):
    def render_html(self, obj: NumTargetDriftMetrics) -> List[MetricHtmlInfo]:
        result = []
        target_output_distr = obj.get_result().target_output_distr
        target_metrics = obj.get_result().target_metrics
        target_values_plot = obj.get_result().target_values_plot
        color_options = ColorOptions()
        if target_output_distr is not None and target_metrics is not None and target_values_plot is not None:
            output_sim_test = "detected" if target_metrics.drift_detected else "not detected"
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_data(
                        title=f"Target Drift: {output_sim_test}, "
                        f" drift score={round(target_metrics.drift_score, 6)} ({target_metrics.stattest_name})",
                        data=target_output_distr["data"],
                        layout=target_output_distr["layout"],
                    ),
                )
            )

            result.append(_plot_correlations(target_metrics, color_options))
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_data(
                        title="Target Values",
                        size=WidgetSize.HALF,
                        data=target_values_plot["data"],
                        layout=target_values_plot["layout"],
                    ),
                ),
            )
        prediction_output_distr = obj.get_result().prediction_output_distr
        prediction_metrics = obj.get_result().prediction_metrics
        prediction_values_plot = obj.get_result().prediction_values_plot
        if (
            prediction_output_distr is not None
            and prediction_metrics is not None
            and prediction_values_plot is not None
        ):
            output_sim_test = "detected" if prediction_metrics.drift_detected else "not detected"
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_data(
                        title=f"Prediction Drift: {output_sim_test},"
                        f" drift score={round(prediction_metrics.drift_score, 6)}"
                        f" ({prediction_metrics.stattest_name})",
                        data=prediction_output_distr["data"],
                        layout=prediction_output_distr["layout"],
                    ),
                )
            )
            result.append(_plot_correlations(prediction_metrics, color_options))
            result.append(
                MetricHtmlInfo(
                    name="",
                    info=plotly_data(
                        title="Prediction Values",
                        size=WidgetSize.HALF,
                        data=prediction_values_plot["data"],
                        layout=prediction_values_plot["layout"],
                    ),
                ),
            )
        return result

    def render_json(self, obj: NumTargetDriftMetrics) -> dict:
        return dataclasses.asdict(obj.get_result())


def _plot_correlations(metrics: DataDriftMetrics, color_options: ColorOptions):
    output_corr = go.Figure()
    ref_output_corr = metrics.reference_correlations
    curr_output_corr = metrics.current_correlations

    if ref_output_corr is None or curr_output_corr is None:
        raise ValueError("expected correlation values")

    output_corr.add_trace(
        go.Bar(
            y=list(ref_output_corr.values()),
            x=list(ref_output_corr.keys()),
            marker_color=color_options.get_reference_data_color(),
            name="Reference",
        )
    )

    output_corr.add_trace(
        go.Bar(
            y=list(curr_output_corr.values()),
            x=list(curr_output_corr.keys()),
            marker_color=color_options.get_current_data_color(),
            name="Current",
        )
    )

    output_corr_json = output_corr.to_plotly_json()
    return MetricHtmlInfo(
        name="",
        info=plotly_data(
            title="Target Correlations",
            size=WidgetSize.HALF,
            data=output_corr_json["data"],
            layout=output_corr_json["layout"],
        ),
    )
