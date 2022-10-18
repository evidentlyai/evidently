import json
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots

from evidently.options.color_scheme import ColorOptions


def plot_distr(hist_curr, hist_ref=None, orientation="v", color_options: Optional[ColorOptions] = None):
    color_options = color_options or ColorOptions()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="current",
            x=hist_curr["x"],
            y=hist_curr["count"],
            marker_color=color_options.get_current_data_color(),
            orientation=orientation,
        )
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(
                name="reference",
                x=hist_ref["x"],
                y=hist_ref["count"],
                marker_color=color_options.get_reference_data_color(),
                orientation=orientation,
            )
        )

    return fig


def plot_distr_subplots(
    hist_curr, hist_ref=None, xaxis_name: str = "", yaxis_name: str = "", same_color: Optional[str] = None
):
    color_options = ColorOptions()
    if same_color is None:
        curr_color = color_options.get_current_data_color()
        ref_color = color_options.get_reference_data_color()
    else:
        curr_color = same_color
        ref_color = same_color

    cols = 1
    subplot_titles: Union[list, str] = ""

    if hist_ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]

    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    trace = go.Bar(x=hist_curr["x"], y=hist_curr["count"], marker_color=curr_color, showlegend=False)
    fig.append_trace(trace, 1, 1)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)

    if hist_ref is not None:
        trace = go.Bar(x=hist_ref["x"], y=hist_ref["count"], marker_color=ref_color, showlegend=False)
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_layout(yaxis_title=yaxis_name)
    fig = json.loads(fig.to_json())
    return fig


def make_hist_for_num_plot(curr: pd.Series, ref: pd.Series = None):
    result = {}
    if ref is not None:
        ref = ref.dropna()
    bins = np.histogram_bin_edges(pd.concat([curr.dropna(), ref]), bins="doane")
    curr_hist = np.histogram(curr, bins=bins)
    result["current"] = make_hist_df(curr_hist)
    if ref is not None:
        ref_hist = np.histogram(ref, bins=bins)
        result["reference"] = make_hist_df(ref_hist)
    return result


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None, normalize: bool = False):
    result = {}
    hist_df = curr.value_counts(normalize=normalize, dropna=False).reset_index()
    hist_df.columns = ["x", "count"]
    result["current"] = hist_df
    if ref is not None:
        hist_df = ref.value_counts(normalize=normalize).reset_index()
        hist_df.columns = ["x", "count"]
        result["reference"] = hist_df
    return result


def get_distribution_for_column(
    *, column_name: str, column_type: str, current: pd.Series, reference: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    if column_type == "cat":
        return make_hist_for_cat_plot(current, reference)

    elif column_type == "num":
        return make_hist_for_num_plot(current, reference)

    else:
        raise ValueError(f"Cannot get distribution for column {column_name} with type {column_type}")


def make_hist_df(hist: Tuple[np.array, np.array]) -> pd.DataFrame:
    hist_df = pd.DataFrame(
        np.array([hist[1][:-1], hist[0], [f"{x[0]}-{x[1]}" for x in zip(hist[1][:-1], hist[1][1:])]]).T,
        columns=["x", "count", "range"],
    )

    hist_df["x"] = hist_df["x"].astype(float)
    hist_df["count"] = hist_df["count"].astype(int)
    return hist_df


def plot_scatter(
    curr: Dict[str, list],
    ref: Optional[Dict[str, list]],
    x: str,
    y: str,
    xaxis_name: str = None,
    yaxis_name: str = None,
):
    color_options = ColorOptions()
    cols = 1
    if xaxis_name is None:
        xaxis_name = x
    if yaxis_name is None:
        yaxis_name = y
    if ref is not None:
        cols = 2
    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True)
    trace = go.Scatter(
        x=curr[x],
        y=curr[y],
        mode="markers",
        marker_color=color_options.get_current_data_color(),
        name="current",
    )
    fig.append_trace(trace, 1, 1)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[x],
            y=ref[y],
            mode="markers",
            marker_color=color_options.get_reference_data_color(),
            name="reference",
        )
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_layout(yaxis_title=yaxis_name, legend={"itemsizing": "constant"})
    fig.update_traces(marker_size=4)
    fig = json.loads(fig.to_json())
    return fig


def plot_pred_actual_time(
    curr: Dict[str, pd.Series],
    ref: Optional[Dict[str, pd.Series]],
    x_name: str = "x",
    xaxis_name: str = "",
    yaxis_name: str = "",
):
    color_options = ColorOptions()
    cols = 1
    subplot_titles: Union[list, str] = ""

    if ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]

    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    for name, color in zip(
        ["Predicted", "Actual"], [color_options.get_current_data_color(), color_options.get_reference_data_color()]
    ):
        trace = go.Scatter(x=curr[x_name], y=curr[name], mode="lines", marker_color=color, name=name, legendgroup=name)
        fig.append_trace(trace, 1, 1)

        if ref is not None:
            trace = go.Scatter(
                x=ref[x_name],
                y=ref[name],
                mode="lines",
                marker_color=color,
                name=name,
                legendgroup=name,
                showlegend=False,
            )
            fig.append_trace(trace, 1, 2)

    # Add zero trace
    trace = go.Scatter(
        x=curr[x_name],
        y=[0] * curr[x_name].shape[0],
        mode="lines",
        marker_color=color_options.zero_line_color,
        showlegend=False,
    )
    fig.append_trace(trace, 1, 1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[x_name],
            y=[0] * ref[x_name].shape[0],
            mode="lines",
            marker_color=color_options.zero_line_color,
            showlegend=False,
        )
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)

    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    fig.update_layout(yaxis_title=yaxis_name)
    fig.update_traces(marker_size=6)
    fig = json.loads(fig.to_json())
    return fig


def plot_line_in_time(
    curr: Dict[str, pd.Series],
    ref: Optional[Dict[str, pd.Series]],
    y_name: str,
    x_name: str = "x",
    xaxis_name: str = "",
    yaxis_name: str = "",
):
    color_options = ColorOptions()
    cols = 1
    subplot_titles: Union[list, str] = ""

    if ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]

    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    trace = go.Scatter(
        x=curr[x_name],
        y=curr[y_name],
        mode="lines",
        marker_color=color_options.get_current_data_color(),
        name=y_name,
        legendgroup=y_name,
    )
    fig.append_trace(trace, 1, 1)
    # Add zero trace
    trace = go.Scatter(
        x=curr[x_name],
        y=[0] * curr[x_name].shape[0],
        mode="lines",
        marker_color=color_options.zero_line_color,
        showlegend=False,
    )
    fig.append_trace(trace, 1, 1)

    if ref is not None:
        trace = go.Scatter(
            x=ref[x_name],
            y=ref[y_name],
            mode="lines",
            marker_color=color_options.get_current_data_color(),
            name=y_name,
            legendgroup=y_name,
            showlegend=False,
        )
        fig.append_trace(trace, 1, 2)
        # Add zero trace
        trace = go.Scatter(
            x=ref[x_name],
            y=[0] * ref[x_name].shape[0],
            mode="lines",
            marker_color=color_options.zero_line_color,
            showlegend=False,
        )
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    fig.update_layout(yaxis_title=yaxis_name)
    fig.update_traces(marker_size=6)
    fig = json.loads(fig.to_json())
    return fig


def plot_error_bias_colored_scatter(
    curr_scatter_data: Dict[str, Dict[str, pd.Series]], ref_scatter_data: Optional[Dict[str, Dict[str, pd.Series]]]
):
    color_options = ColorOptions()
    cols = 1
    subplot_titles: Union[list, str] = ""

    if ref_scatter_data is not None:
        cols = 2
        subplot_titles = ["current", "reference"]

    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)

    for name, color in zip(
        ["Underestimation", "Overestimation", "Majority"],
        [color_options.underestimation_color, color_options.overestimation_color, color_options.majority_color],
    ):
        trace = go.Scatter(
            x=curr_scatter_data[name]["Actual value"],
            y=curr_scatter_data[name]["Predicted value"],
            mode="markers",
            name=name,
            legendgroup=name,
            marker_color=color
            # marker=dict(color=color_options.underestimation_color, showscale=False),
        )
        fig.append_trace(trace, 1, 1)
    fig.update_xaxes(title_text="Actual value", row=1, col=1)

    if ref_scatter_data is not None:
        for name, color in zip(
            ["Underestimation", "Overestimation", "Majority"],
            [color_options.underestimation_color, color_options.overestimation_color, color_options.majority_color],
        ):
            trace = go.Scatter(
                x=ref_scatter_data[name]["Actual value"],
                y=ref_scatter_data[name]["Predicted value"],
                mode="markers",
                name=name,
                legendgroup=name,
                showlegend=False,
                marker_color=color
                # marker=dict(color=color_options.underestimation_color, showscale=False),
            )
            fig.append_trace(trace, 1, 2)
        fig.update_xaxes(title_text="Actual value", row=1, col=2)

    fig.update_layout(
        yaxis_title="Predicted value",
        xaxis=dict(showticklabels=True),
        yaxis=dict(showticklabels=True),
    )
    fig = json.loads(fig.to_json())
    return fig


def plot_scatter_for_data_drift(curr_y: list, curr_x: list, y0: float, y1: float, y_name: str, x_name: str):
    color_options = ColorOptions()

    fig = go.Figure()

    fig.add_trace(
        go.Scattergl(
            x=curr_x,
            y=curr_y,
            mode="markers",
            name="Current",
            marker=dict(size=6, color=color_options.get_current_data_color()),
        )
    )

    x0 = np.max(curr_x)

    fig.add_trace(
        go.Scattergl(
            x=[x0, x0],
            y=[y0, y1],
            mode="markers",
            name="Current",
            marker=dict(size=0.01, color=color_options.non_visible_color, opacity=0.005),
            showlegend=False,
        )
    )

    fig.update_layout(
        xaxis_title=x_name,
        yaxis_title=y_name,
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
                y0=y0,
                x1=1,
                y1=y1,
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
                y0=(y0 + y1) / 2,
                x1=1,  # max(testset_agg_by_date.index),
                y1=(y0 + y1) / 2,
                line=dict(color=color_options.zero_line_color, width=3),
            ),
        ],
    )
    return fig
