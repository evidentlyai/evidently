from typing import Optional

import plotly.graph_objs as go

from evidently.options import ColorOptions
from evidently.utils.visualizations import Distribution

RED = "#ed0400"
GREY = "#4d4d4d"
COLOR_DISCRETE_SEQUENCE = (
    "#ed0400",
    "#0a5f38",
    "#6c3461",
    "#6b8ba4",
)


def plot_distr(hist_curr, hist_ref=None, orientation="v"):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name="current", x=hist_curr["x"], y=hist_curr["count"], marker_color=RED, orientation=orientation)
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(name="reference", x=hist_ref["x"], y=hist_ref["count"], marker_color=GREY, orientation=orientation)
        )

    return fig


def get_distribution_plot_figure(
    current_distribution: Distribution,
    reference_distribution: Optional[Distribution],
    orientation: str = "v",
    color_options: Optional[ColorOptions] = None,
) -> go.Figure:
    fig = go.Figure()
    if color_options is None:
        color_options = ColorOptions()

    fig.add_trace(
        go.Bar(
            name="current",
            x=current_distribution.x,
            y=current_distribution.y,
            marker_color=color_options.current_data_color,
            orientation=orientation,
        )
    )
    if reference_distribution is not None:
        fig.add_trace(
            go.Bar(
                name="reference",
                x=reference_distribution.x,
                y=reference_distribution.y,
                marker_color=color_options.reference_data_color,
                orientation=orientation,
            )
        )

    return fig
