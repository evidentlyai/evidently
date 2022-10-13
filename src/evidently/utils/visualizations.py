from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
from plotly import graph_objs as go

from evidently.options.color_scheme import ColorOptions
from evidently.utils.types import ColumnDistribution
from evidently.utils.types import Numeric


def get_distribution_plot(
    current: ColumnDistribution,
    reference: Optional[ColumnDistribution] = None,
    orientation="v",
    color_options: Optional[ColorOptions] = None,
):
    current_df = pd.DataFrame(current, columns=["x", "count"])

    if reference is not None:
        reference_df = pd.DataFrame(reference, columns=["x", "count"])

    else:
        reference_df = None

    return plot_distr(current_df, reference_df, orientation, color_options)


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


def plot_distribution_with_range(
    *,
    distribution_data: pd.Series,
    left: Optional[Numeric] = None,
    right: Optional[Numeric] = None,
    orientation: str = "v",
    color_options: Optional[ColorOptions] = None,
) -> go.Figure:
    """Get a plot with distribution and range from `left` to `right` markers"""

    if color_options is None:
        color_options = ColorOptions()

    fig = plot_distr(distribution_data, None, orientation, color_options)

    if left is not None:
        fig.add_vline(x=left, line_width=2, line_dash="dash", line_color="black")

    if right is not None:
        fig.add_vline(x=right, line_width=2, line_dash="dash", line_color="black")

    if left and right:
        fig.add_vrect(x0=left, x1=right, fillcolor=color_options.fill_color, opacity=0.25, line_width=0)

    return fig


def make_hist_for_num_plot(curr: pd.Series, ref: pd.Series = None) -> Dict[str, pd.DataFrame]:
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


def make_hist_for_cat_plot(curr: pd.Series, ref: pd.Series = None, normalize: bool = False) -> Dict[str, pd.Series]:
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
    *, column_name: str, column_type: str, current: pd.Series, reference: pd.Series
) -> Dict[str, Union[pd.Series, pd.DataFrame]]:
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
