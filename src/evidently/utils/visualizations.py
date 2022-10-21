import json
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from evidently.renderers.html_widgets import plotly_figure

from evidently.options.color_scheme import ColorOptions
from evidently.model.widget import BaseWidgetInfo


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


def plot_conf_mtrx(curr_mtrx, ref_mtrx):
    if ref_mtrx is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    else:
        cols = 1
        subplot_titles = [""]
    fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
    trace = go.Heatmap(
        z=curr_mtrx.values,
        x=curr_mtrx.labels,
        y=curr_mtrx.labels,
        text=np.array(curr_mtrx.values).astype(str),
        texttemplate="%{text}",
        coloraxis="coloraxis",
    )
    fig.append_trace(trace, 1, 1)

    if ref_mtrx is not None:
        trace = go.Heatmap(
            z=ref_mtrx.values,
            x=ref_mtrx.labels,
            y=ref_mtrx.labels,
            text=np.array(ref_mtrx.values).astype(str),
            texttemplate="%{text}",
            coloraxis="coloraxis",
        )
        fig.append_trace(trace, 1, 2)
    fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
    return fig


def get_roc_auc_tab_data(curr_roc_curve: dict, ref_roc_curve: Optional[dict]) -> List[Tuple[str, BaseWidgetInfo]]:
    color_options = ColorOptions()
    additional_plots = []
    cols = 1
    subplot_titles = [""]
    if ref_roc_curve is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    for label in curr_roc_curve.keys():
        fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
        trace = go.Scatter(
            x=curr_roc_curve[label]["fpr"],
            y=curr_roc_curve[label]["tpr"],
            mode="lines",
            name="ROC",
            legendgroup="ROC",
            marker=dict(
                size=6,
                color=color_options.get_current_data_color(),
            ),
        )
        fig.append_trace(trace, 1, 1)
        fig.update_xaxes(title_text="False Positive Rate", row=1, col=1)
        if ref_roc_curve is not None:
            trace = go.Scatter(
                x=ref_roc_curve[label]["fpr"],
                y=ref_roc_curve[label]["tpr"],
                mode="lines",
                name="ROC",
                legendgroup="ROC",
                showlegend=False,
                marker=dict(
                    size=6,
                    color=color_options.get_current_data_color(),
                ),
            )
            fig.append_trace(trace, 1, 2)
            fig.update_xaxes(title_text="False Positive Rate", row=1, col=2)
        fig.update_layout(yaxis_title="True Positive Rate", showlegend=True)

        additional_plots.append((str(label), plotly_figure(title="", figure=fig)))
    return additional_plots


def get_pr_rec_plot_data(current_pr_curve: dict, reference_pr_curve: Optional[dict]) -> List[Tuple[str, BaseWidgetInfo]]:
    color_options = ColorOptions()
    additional_plots = []
    cols = 1
    subplot_titles = [""]
    if reference_pr_curve is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    for label in current_pr_curve.keys():
        fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
        trace = go.Scatter(
            x=current_pr_curve[label]["rcl"],
            y=current_pr_curve[label]["pr"],
            mode="lines",
            name="PR",
            legendgroup="PR",
            marker=dict(
                size=6,
                color=color_options.get_current_data_color(),
            ),
        )
        fig.append_trace(trace, 1, 1)
        fig.update_xaxes(title_text="Recall", row=1, col=1)
        if reference_pr_curve is not None:
            trace = go.Scatter(
                x=reference_pr_curve[label]["rcl"],
                y=reference_pr_curve[label]["pr"],
                mode="lines",
                name="PR",
                legendgroup="PR",
                showlegend=False,
                marker=dict(
                    size=6,
                    color=color_options.get_current_data_color(),
                ),
            )
            fig.append_trace(trace, 1, 2)
            fig.update_xaxes(title_text="Recall", row=1, col=2)
        fig.update_layout(yaxis_title="Precision", showlegend=True)

        additional_plots.append((str(label), plotly_figure(title="", figure=fig)))
    return additional_plots


def get_class_separation_plot_data(current_plot: pd.DataFrame, reference_plot: Optional[pd.DataFrame], target_name: str
                         ) -> List[Tuple[str, BaseWidgetInfo]]:
    color_options = ColorOptions()
    additional_plots = []
    cols = 1
    subplot_titles = [""]
    if reference_plot is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    for label in current_plot.columns.drop(target_name):
        fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)
        trace = go.Scatter(
            x=np.random.random(current_plot[current_plot[target_name] == label].shape[0]),
            y=current_plot[current_plot[target_name] == label][label],
            mode="markers",
            name=str(label),
            legendgroup=str(label),
            marker=dict(size=6, color=color_options.primary_color),
        )
        fig.append_trace(trace, 1, 1)

        trace = go.Scatter(
            x=np.random.random(current_plot[current_plot[target_name] != label].shape[0]),
            y=current_plot[current_plot[target_name] != label][label],
            mode="markers",
            name="other",
            legendgroup="other",
            marker=dict(size=6, color=color_options.secondary_color),
        )
        fig.append_trace(trace, 1, 1)
        fig.update_xaxes(dict(range=(-2, 3), showticklabels=False), row=1, col=1)

        if reference_plot is not None:
            trace = go.Scatter(
                x=np.random.random(reference_plot[reference_plot[target_name] == label].shape[0]),
                y=reference_plot[reference_plot[target_name] == label][label],
                mode="markers",
                name=str(label),
                legendgroup=str(label),
                showlegend=False,
                marker=dict(size=6, color=color_options.primary_color),
            )
            fig.append_trace(trace, 1, 2)

            trace = go.Scatter(
                x=np.random.random(reference_plot[reference_plot[target_name] != label].shape[0]),
                y=reference_plot[reference_plot[target_name] != label][label],
                mode="markers",
                name="other",
                legendgroup="other",
                showlegend=False,
                marker=dict(size=6, color=color_options.secondary_color),
            )
            fig.append_trace(trace, 1, 2)
            fig.update_xaxes(dict(range=(-2, 3), showticklabels=False), row=1, col=2)
        fig.update_layout(yaxis_title="Probability", showlegend=True)

        additional_plots.append((str(label), plotly_figure(title="", figure=fig)))
    return additional_plots