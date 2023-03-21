import json
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots

from evidently.metric_results import Distribution
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.metric_results import Label
from evidently.metric_results import ScatterData
from evidently.options.color_scheme import ColorOptions


def plot_distr(
    *, hist_curr: HistogramData, hist_ref: Optional[HistogramData] = None, orientation="v", color_options: ColorOptions
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="current",
            x=hist_curr.x,
            y=hist_curr.count,
            marker_color=color_options.get_current_data_color(),
            orientation=orientation,
        )
    )
    cats = list(hist_curr.x)
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(
                name="reference",
                x=hist_ref.x,
                y=hist_ref.count,
                marker_color=color_options.get_reference_data_color(),
                orientation=orientation,
            )
        )
        cats = cats + list(np.setdiff1d(hist_ref.x, cats))

    if "other" in cats:
        cats.remove("other")
        cats = cats + ["other"]
        fig.update_xaxes(categoryorder="array", categoryarray=cats)

    return fig


def plot_distr_with_log_button(
    curr_data: HistogramData,
    curr_data_log: HistogramData,
    ref_data: Optional[HistogramData],
    ref_data_log: Optional[HistogramData],
    color_options: ColorOptions,
):
    traces = []
    visible = [True, False]
    traces.append(
        go.Bar(
            x=curr_data.x,
            y=curr_data.count,
            marker_color=color_options.get_current_data_color(),
            name="current",
        )
    )
    traces.append(
        go.Bar(
            x=curr_data_log.x,
            y=curr_data_log.count,
            visible=False,
            marker_color=color_options.get_current_data_color(),
            name="current",
        )
    )
    if ref_data is not None:
        traces.append(
            go.Bar(
                x=ref_data.x,
                y=ref_data.count,
                marker_color=color_options.get_reference_data_color(),
                name="reference",
            )
        )
        visible.append(True)
        if ref_data_log is not None:
            traces.append(
                go.Bar(
                    x=ref_data_log.x,
                    y=ref_data_log.count,
                    visible=False,
                    marker_color=color_options.get_reference_data_color(),
                    name="reference",
                )
            )
            visible.append(False)

    updatemenus = [
        dict(
            type="buttons",
            direction="right",
            x=1.0,
            yanchor="top",
            buttons=list(
                [
                    dict(
                        label="Linear Scale",
                        method="update",
                        args=[{"visible": visible}],
                    ),
                    dict(
                        label="Log Scale",
                        method="update",
                        args=[{"visible": [not x for x in visible]}],
                    ),
                ]
            ),
        )
    ]
    layout = dict(updatemenus=updatemenus)

    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig = json.loads(fig.to_json())
    return fig


def plot_distr_subplots(
    *,
    hist_curr: HistogramData,
    hist_ref: Optional[HistogramData] = None,
    xaxis_name: str = "",
    yaxis_name: str = "",
    same_color: bool = False,
    color_options: ColorOptions,
):
    if same_color is None:
        curr_color = color_options.get_current_data_color()
        ref_color = color_options.get_reference_data_color()

    else:
        curr_color = color_options.get_current_data_color()
        ref_color = curr_color

    cols = 1
    subplot_titles: Union[list, str] = ""

    if hist_ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]

    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    trace = go.Bar(x=hist_curr.x, y=hist_curr.count, marker_color=curr_color, showlegend=False)
    fig.add_trace(trace, 1, 1)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)

    if hist_ref is not None:
        trace = go.Bar(x=hist_ref.x, y=hist_ref.count, marker_color=ref_color, showlegend=False)
        fig.add_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_layout(yaxis_title=yaxis_name)
    fig = json.loads(fig.to_json())
    return fig


def plot_num_feature_in_time(
    curr_data: pd.DataFrame,
    ref_data: Optional[pd.DataFrame],
    feature_name: str,
    datetime_name: str,
    freq: str,
    color_options: ColorOptions,
):
    """
    Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curr_data.sort_values(datetime_name)[datetime_name],
            y=curr_data.sort_values(datetime_name)[feature_name],
            line=dict(color=color_options.get_current_data_color(), shape="spline"),
            name="current",
        )
    )
    if ref_data is not None:
        fig.add_trace(
            go.Scatter(
                x=ref_data.sort_values(datetime_name)[datetime_name],
                y=ref_data.sort_values(datetime_name)[feature_name],
                line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                name="reference",
            )
        )

    fig.update_layout(yaxis_title="Mean " + feature_name + " per " + freq)
    feature_in_time_figure = json.loads(fig.to_json())
    return feature_in_time_figure


def plot_time_feature_distr(current: HistogramData, reference: Optional[HistogramData], color_options: ColorOptions):
    """
    Accepts current and reference data as pandas dataframes with two columns: feature_name, "number_of_items"
    """
    curr_data = current.to_df().sort_values("x")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=curr_data["x"],
            y=curr_data["count"],
            line=dict(color=color_options.get_current_data_color(), shape="spline"),
            name="current",
        )
    )
    if reference is not None:
        ref_data = reference.to_df().sort_values("x")

        fig.add_trace(
            go.Scatter(
                x=ref_data["x"],
                y=ref_data["count"],
                line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                name="reference",
            )
        )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig = json.loads(fig.to_json())
    return fig


def plot_cat_feature_in_time(
    curr_data: pd.DataFrame,
    ref_data: Optional[pd.DataFrame],
    feature_name: str,
    datetime_name: str,
    freq: str,
    color_options: ColorOptions,
):
    """
    Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.
    """
    title = "current"
    fig = go.Figure()
    values = curr_data[feature_name].astype(str).unique()
    if ref_data is not None:
        values = np.union1d(curr_data[feature_name].astype(str).unique(), ref_data[feature_name].astype(str).unique())
    for i, val in enumerate(values):
        fig.add_trace(
            go.Bar(
                x=curr_data.loc[curr_data[feature_name].astype(str) == val, datetime_name],
                y=curr_data.loc[curr_data[feature_name].astype(str) == val, "num"],
                name=str(val),
                marker_color=color_options.color_sequence[i],
                legendgroup=str(val),
            )
        )
        if ref_data is not None:
            title = "reference/current"
            fig.add_trace(
                go.Bar(
                    x=ref_data.loc[ref_data[feature_name].astype(str) == val, datetime_name],
                    y=ref_data.loc[ref_data[feature_name].astype(str) == val, "num"],
                    name=str(val),
                    marker_color=color_options.color_sequence[i],
                    # showlegend=False,
                    legendgroup=str(val),
                    opacity=0.6,
                )
            )
    fig.update_traces(marker_line_width=0.01)
    fig.update_layout(
        barmode="stack",
        bargap=0,
        yaxis_title="count category values per " + freq,
        title=title,
    )
    feature_in_time_figure = json.loads(fig.to_json())
    return feature_in_time_figure


def plot_boxes(
    curr_for_plots: dict, ref_for_plots: Optional[dict], yaxis_title: str, xaxis_title: str, color_options: ColorOptions
):
    """
    Accepts current and reference data as dicts with box parameters ("mins", "lowers", "uppers", "means", "maxs")
    and name of boxes parameter - "values"
    """
    fig = go.Figure()
    trace = go.Box(
        lowerfence=curr_for_plots["mins"],
        q1=curr_for_plots["lowers"],
        q3=curr_for_plots["uppers"],
        median=curr_for_plots["means"],
        upperfence=curr_for_plots["maxs"],
        x=curr_for_plots["values"],
        name="current",
        marker_color=color_options.get_current_data_color(),
    )
    fig.add_trace(trace)
    if ref_for_plots is not None:
        trace = go.Box(
            lowerfence=curr_for_plots["mins"],
            q1=ref_for_plots["lowers"],
            q3=ref_for_plots["uppers"],
            median=ref_for_plots["means"],
            upperfence=ref_for_plots["maxs"],
            x=ref_for_plots["values"],
            name="reference",
            marker_color=color_options.get_reference_data_color(),
        )
        fig.add_trace(trace)
        fig.update_layout(boxmode="group")
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title, boxmode="group")
    fig = json.loads(fig.to_json())
    return fig


def make_hist_for_num_plot(curr: pd.Series, ref: pd.Series = None) -> Histogram:
    if ref is not None:
        ref = ref.dropna()
    bins = np.histogram_bin_edges(pd.concat([curr.dropna(), ref]), bins="doane")
    curr_hist = np.histogram(curr, bins=bins)
    current = make_hist_df(curr_hist)
    reference = None
    if ref is not None:
        ref_hist = np.histogram(ref, bins=bins)
        reference = make_hist_df(ref_hist)
    return Histogram(current=HistogramData.from_df(current), reference=HistogramData.from_df(reference))


def plot_cat_cat_rel(
    curr: pd.DataFrame, ref: pd.DataFrame, target_name: str, feature_name: str, color_options: ColorOptions
):
    """
    Accepts current and reference data as pandas dataframes with two columns: feature_name and "count_objects".
    """
    cols = 1
    subplot_titles: Union[list, str] = ""
    if ref is not None:
        cols = 2
        subplot_titles = ["current", "reference"]
    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True, subplot_titles=subplot_titles)
    for i, val in enumerate(curr[target_name].astype(str).unique()):
        trace = go.Bar(
            x=curr.loc[curr[target_name] == val, feature_name],
            y=curr.loc[curr[target_name] == val, "count_objects"],
            marker_color=color_options.color_sequence[i],
            name=str(val),
            legendgroup=str(val),
        )
        fig.add_trace(trace, 1, 1)

    if ref is not None:
        for i, val in enumerate(ref[target_name].astype(str).unique()):
            trace = go.Bar(
                x=ref.loc[ref[target_name] == val, feature_name],
                y=ref.loc[ref[target_name] == val, "count_objects"],
                marker_color=color_options.color_sequence[i],
                opacity=0.6,
                name=str(val),
                legendgroup=str(val),
            )
            fig.add_trace(trace, 1, 2)
    fig.update_layout(yaxis_title="count")
    fig = json.loads(fig.to_json())
    return fig


def plot_num_num_rel(
    curr: Dict[str, list],
    ref: Optional[Dict[str, list]],
    target_name: str,
    column_name: str,
    color_options: ColorOptions,
):
    cols = 1
    if ref is not None:
        cols = 2
    fig = make_subplots(rows=1, cols=cols, shared_yaxes=True)
    trace = go.Scatter(
        x=curr[column_name],
        y=curr[target_name],
        mode="markers",
        marker_color=color_options.get_current_data_color(),
        name="current",
    )
    fig.add_trace(trace, 1, 1)
    fig.update_xaxes(title_text=column_name, row=1, col=1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[column_name],
            y=ref[target_name],
            mode="markers",
            marker_color=color_options.get_reference_data_color(),
            name="reference",
        )
        fig.add_trace(trace, 1, 2)
        fig.update_xaxes(title_text=column_name, row=1, col=2)
    fig.update_layout(yaxis_title=target_name, legend={"itemsizing": "constant"})
    fig.update_traces(marker_size=4)
    fig = json.loads(fig.to_json())
    return fig


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None, normalize: bool = False, dropna=False) -> Histogram:
    hist_df = curr.astype(str).value_counts(normalize=normalize, dropna=dropna).reset_index()
    hist_df.columns = ["x", "count"]
    current = HistogramData.from_df(hist_df)

    reference = None
    if ref is not None:
        hist_df = ref.astype(str).value_counts(normalize=normalize, dropna=dropna).reset_index()
        hist_df.columns = ["x", "count"]
        reference = HistogramData.from_df(hist_df)
    return Histogram(current=current, reference=reference)


def get_distribution_for_category_column(column: pd.Series, normalize: bool = False) -> Distribution:
    value_counts = column.value_counts(normalize=normalize, dropna=False)
    return Distribution(
        x=value_counts.index.values,
        y=value_counts.values,
    )


def get_distribution_for_numerical_column(
    column: pd.Series,
    bins: Optional[Union[list, np.ndarray]] = None,
) -> Distribution:
    if bins is None:
        bins = np.histogram_bin_edges(column, bins="doane")

    histogram = np.histogram(column, bins=bins)
    return Distribution(
        x=histogram[1],
        y=histogram[0],
    )


def get_distribution_for_column(
    *, column_type: str, current: pd.Series, reference: Optional[pd.Series] = None
) -> Tuple[Distribution, Optional[Distribution]]:
    reference_distribution: Optional[Distribution] = None

    if column_type == "cat":
        current_distribution = get_distribution_for_category_column(current)

        if reference is not None:
            reference_distribution = get_distribution_for_category_column(reference)

    elif column_type == "num":
        if reference is not None:
            bins = np.histogram_bin_edges(pd.concat([current.dropna(), reference.dropna()]), bins="doane")
            reference_distribution = get_distribution_for_numerical_column(reference, bins)

        else:
            bins = np.histogram_bin_edges(current.dropna(), bins="doane")

        current_distribution = get_distribution_for_numerical_column(current, bins)

    else:
        raise ValueError(f"Cannot get distribution for a column with type {column_type}")

    return current_distribution, reference_distribution


def make_hist_df(hist: Tuple[np.ndarray, np.ndarray]) -> pd.DataFrame:
    hist_df = pd.DataFrame(
        np.array([hist[1][:-1], hist[0], [f"{x[0]}-{x[1]}" for x in zip(hist[1][:-1], hist[1][1:])]]).T,
        columns=["x", "count", "range"],
    )

    hist_df["x"] = hist_df["x"].astype(float)
    hist_df["count"] = hist_df["count"].astype(int)
    return hist_df


def plot_scatter(
    *,
    curr: Dict[str, ScatterData],
    ref: Optional[Dict[str, ScatterData]],
    x: str,
    y: str,
    xaxis_name: str = None,
    yaxis_name: str = None,
    color_options: ColorOptions,
):
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
    fig.add_trace(trace, 1, 1)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[x],
            y=ref[y],
            mode="markers",
            marker_color=color_options.get_reference_data_color(),
            name="reference",
        )
        fig.add_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_layout(yaxis_title=yaxis_name, legend={"itemsizing": "constant"})
    fig.update_traces(marker_size=4)
    fig = json.loads(fig.to_json())
    return fig


def plot_pred_actual_time(
    *,
    curr: Dict[Label, pd.Series],
    ref: Optional[Dict[Label, pd.Series]],
    x_name: str = "x",
    xaxis_name: str = "",
    yaxis_name: str = "",
    color_options: ColorOptions,
):
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
        fig.add_trace(trace, 1, 1)

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
            fig.add_trace(trace, 1, 2)

    # Add zero trace
    trace = go.Scatter(
        x=curr[x_name],
        y=[0] * curr[x_name].shape[0],
        mode="lines",
        marker_color=color_options.zero_line_color,
        showlegend=False,
    )
    fig.add_trace(trace, 1, 1)
    if ref is not None:
        trace = go.Scatter(
            x=ref[x_name],
            y=[0] * ref[x_name].shape[0],
            mode="lines",
            marker_color=color_options.zero_line_color,
            showlegend=False,
        )
        fig.add_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)

    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    fig.update_layout(yaxis_title=yaxis_name)
    fig.update_traces(marker_size=6)
    fig = json.loads(fig.to_json())
    return fig


def plot_line_in_time(
    *,
    curr: Dict[Label, pd.Series],
    ref: Optional[Dict[Label, pd.Series]],
    x_name: str,
    y_name: str,
    xaxis_name: str = "",
    yaxis_name: str = "",
    color_options: ColorOptions,
):
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
    fig.add_trace(trace, 1, 1)
    # Add zero trace
    trace = go.Scatter(
        x=curr[x_name],
        y=[0] * curr[x_name].shape[0],
        mode="lines",
        marker_color=color_options.zero_line_color,
        showlegend=False,
    )
    fig.add_trace(trace, 1, 1)

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
        fig.add_trace(trace, 1, 2)
        # Add zero trace
        trace = go.Scatter(
            x=ref[x_name],
            y=[0] * ref[x_name].shape[0],
            mode="lines",
            marker_color=color_options.zero_line_color,
            showlegend=False,
        )
        fig.add_trace(trace, 1, 2)
        fig.update_xaxes(title_text=xaxis_name, row=1, col=2)
    fig.update_xaxes(title_text=xaxis_name, row=1, col=1)
    fig.update_layout(yaxis_title=yaxis_name)
    fig.update_traces(marker_size=6)
    fig = json.loads(fig.to_json())
    return fig


def plot_scatter_for_data_drift(
    curr_y: list, curr_x: list, y0: float, y1: float, y_name: str, x_name: str, color_options: ColorOptions
):
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
        x=[str(item) for item in curr_mtrx.labels],
        y=[str(item) for item in curr_mtrx.labels],
        text=np.array(curr_mtrx.values).astype(str),
        texttemplate="%{text}",
        coloraxis="coloraxis",
    )
    fig.add_trace(trace, 1, 1)

    if ref_mtrx is not None:
        trace = go.Heatmap(
            z=ref_mtrx.values,
            x=[str(item) for item in ref_mtrx.labels],
            y=[str(item) for item in ref_mtrx.labels],
            text=np.array(ref_mtrx.values).astype(str),
            texttemplate="%{text}",
            coloraxis="coloraxis",
        )
        fig.add_trace(trace, 1, 2)
    fig.update_layout(coloraxis={"colorscale": "RdBu_r"})
    return fig
