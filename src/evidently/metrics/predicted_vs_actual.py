import dataclasses
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

import plotly.graph_objs as go
from scipy.stats import probplot

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class PlotData:
    type: str
    date_column: Optional[str]
    date: pd.Series
    target: pd.Series
    prediction: pd.Series
    length: int
    diff: pd.Series
    abs_perc_error: pd.Series
    qq_lines: tuple
    theoretical_q_x: np.array


@dataclasses.dataclass
class PredictedVsActualResult:
    reference_data: Optional[PlotData]
    current_data: PlotData


class PredictedVsActualMetric(Metric[PredictedVsActualResult]):
    def calculate(self, data: InputData) -> PredictedVsActualResult:
        columns = process_columns(data.current_data, data.column_mapping)

        target_name = columns.utility_columns.target
        prediction_name = columns.utility_columns.prediction
        if target_name is None or prediction_name is None or not isinstance(prediction_name, str):
            raise ValueError("expected target and prediction names to be set and present")
        ref_result = None
        if data.reference_data is not None:
            ref_result = _plot_data(data.reference_data, target_name, prediction_name, columns.utility_columns.date)
        current_result = _plot_data(data.current_data, target_name, prediction_name, columns.utility_columns.date)
        return PredictedVsActualResult(
            reference_data=ref_result,
            current_data=current_result,
        )


def _plot_data(dataset: pd.DataFrame, target_name: str, prediction_name: str, date_column: Optional[str]):
    dataset.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataset.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
    error = dataset[prediction_name] - dataset[target_name]
    qq_lines = probplot(error, dist="norm", plot=None)
    theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100)
    return PlotData(
        type="scatter",
        date_column=date_column,
        date=dataset[date_column] if date_column else dataset.index,
        target=dataset[target_name],
        prediction=dataset[prediction_name],
        length=dataset.shape[0],
        diff=error,
        abs_perc_error=(100.0 * np.abs(error) / dataset[target_name]),
        qq_lines=qq_lines,
        theoretical_q_x=theoretical_q_x,
    )


@default_renderer(wrap_type=PredictedVsActualMetric)
class PredictedVsActualRenderer(MetricRenderer):
    def render_html(self, obj: PredictedVsActualMetric) -> List[MetricHtmlInfo]:
        color_options = ColorOptions()
        generators = [
            _plot_data_to_plotly,
            _pred_vs_actual_in_time,
            _error_in_time,
            _abs_error_in_time,
            _error_distr,
            _error_norm,
        ]
        result = []
        for gen in generators:
            ref_data = obj.get_result().reference_data
            if ref_data is not None:
                result.append(MetricHtmlInfo(name="", info=gen(ref_data, "reference", color_options), details=[]))
            result.append(
                MetricHtmlInfo(name="", info=gen(obj.get_result().current_data, "current", color_options), details=[])
            )
        return result

    def render_json(self, obj) -> dict:
        return {}


def _error_norm(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    error_norm = go.Figure()
    sample_quantile_trace = go.Scatter(
        x=plot_data.qq_lines[0][0],
        y=plot_data.qq_lines[0][1],
        mode="markers",
        name="Dataset Quantiles",
        marker=dict(size=6, color=color_options.primary_color),
    )

    theoretical_quantile_trace = go.Scatter(
        x=plot_data.theoretical_q_x,
        y=plot_data.qq_lines[1][0] * plot_data.theoretical_q_x + plot_data.qq_lines[1][1],
        mode="lines",
        name="Theoretical Quantiles",
        marker=dict(size=6, color=color_options.secondary_color),
    )

    error_norm.add_trace(sample_quantile_trace)
    error_norm.add_trace(theoretical_quantile_trace)

    error_norm.update_layout(
        xaxis_title="Theoretical Quantiles",
        yaxis_title="Dataset Quantiles",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    error_norm_json = error_norm.to_plotly_json()

    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Error Normality",
        type="big_graph",
        size=1,
        params={"data": error_norm_json["data"], "layout": error_norm_json["layout"]},
    )


def _error_in_time(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    error_in_time = go.Figure()

    error_trace = go.Scatter(
        x=plot_data.date,
        y=plot_data.diff,
        mode="lines",
        name="Predicted - Actual",
        marker=dict(size=6, color=color_options.primary_color),
    )

    zero_trace = go.Scatter(
        x=plot_data.date,
        y=[0] * plot_data.length,
        mode="lines",
        opacity=0.5,
        marker=dict(
            size=6,
            color=color_options.zero_line_color,
        ),
        showlegend=False,
    )

    error_in_time.add_trace(error_trace)
    error_in_time.add_trace(zero_trace)

    error_in_time.update_layout(
        xaxis_title="Timestamp" if plot_data.date_column else "Index",
        yaxis_title="Error",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    error_in_time_json = error_in_time.to_plotly_json()

    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Error (Predicted - Actual)",
        type="big_graph",
        size=1,
        params={"data": error_in_time_json["data"], "layout": error_in_time_json["layout"]},
        additionalGraphs=[],
    )


def _error_distr(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    error_distr = go.Figure()

    error = plot_data.diff

    error_distr.add_trace(
        go.Histogram(x=error, marker_color=color_options.primary_color, name="error distribution", histnorm="percent")
    )

    error_distr.update_layout(
        xaxis_title="Error (Predicted - Actual)",
        yaxis_title="Percentage",
    )

    error_distr_json = error_distr.to_plotly_json()

    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Error Distribution",
        type="big_graph",
        size=1,
        params={"data": error_distr_json["data"], "layout": error_distr_json["layout"]},
    )


def _abs_error_in_time(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    abs_perc_error_time = go.Figure()
    error_trace = go.Scatter(
        x=plot_data.date,
        y=plot_data.abs_perc_error,
        mode="lines",
        name="Absolute Percentage Error",
        marker=dict(size=6, color=color_options.primary_color),
    )

    zero_trace = go.Scatter(
        x=plot_data.date,
        y=[0] * plot_data.length,
        mode="lines",
        opacity=0.5,
        marker=dict(
            size=6,
            color=color_options.zero_line_color,
        ),
        showlegend=False,
    )

    abs_perc_error_time.add_trace(error_trace)
    abs_perc_error_time.add_trace(zero_trace)

    abs_perc_error_time.update_layout(
        xaxis_title="Timestamp" if plot_data.length else "Index",
        yaxis_title="Percent",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    abs_perc_error_time_json = abs_perc_error_time.to_plotly_json()

    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Absolute Percentage Error",
        type="big_graph",
        size=1,
        params={"data": abs_perc_error_time_json["data"], "layout": abs_perc_error_time_json["layout"]},
        additionalGraphs=[],
    )


def _pred_vs_actual_in_time(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    pred_actual_time = go.Figure()

    target_trace = go.Scatter(
        x=plot_data.date,
        y=plot_data.target,
        mode="lines",
        name="Actual",
        marker=dict(size=6, color=color_options.secondary_color),
    )

    pred_trace = go.Scatter(
        x=plot_data.date,
        y=plot_data.prediction,
        mode="lines",
        name="Predicted",
        marker=dict(size=6, color=color_options.primary_color),
    )

    zero_trace = go.Scatter(
        x=plot_data.date,
        y=[0] * plot_data.length,
        mode="lines",
        opacity=0.5,
        marker=dict(
            size=6,
            color=color_options.zero_line_color,
        ),
        showlegend=False,
    )

    pred_actual_time.add_trace(target_trace)
    pred_actual_time.add_trace(pred_trace)
    pred_actual_time.add_trace(zero_trace)

    pred_actual_time.update_layout(
        xaxis_title="Timestamp" if plot_data.date_column else "Index",
        yaxis_title="Value",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    pred_actual_time_json = pred_actual_time.to_plotly_json()

    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Predicted vs Actual in Time",
        type="big_graph",
        size=1,
        params={"data": pred_actual_time_json["data"], "layout": pred_actual_time_json["layout"]},
    )


def _plot_data_to_plotly(plot_data: PlotData, dataset_name: str, color_options: ColorOptions):
    pred_actual = go.Figure()

    pred_actual.add_trace(
        go.Scatter(
            x=plot_data.target,
            y=plot_data.prediction,
            mode="markers",
            name=dataset_name,
            marker=dict(color=color_options.primary_color, showscale=False),
        )
    )

    pred_actual.update_layout(
        xaxis_title="Actual value",
        yaxis_title="Predicted value",
        xaxis=dict(showticklabels=True),
        yaxis=dict(showticklabels=True),
    )

    pred_actual_json = pred_actual.to_plotly_json()
    return BaseWidgetInfo(
        title=f"{dataset_name.title()}: Predicted vs Actual",
        type="big_graph",
        size=1,
        params={"data": pred_actual_json["data"], "layout": pred_actual_json["layout"]},
    )
