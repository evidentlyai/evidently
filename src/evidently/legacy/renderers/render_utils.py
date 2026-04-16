from typing import Optional

import plotly.graph_objs as go

from evidently.legacy.metric_results import Distribution
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.options import ColorOptions


def plot_distr(
    *,
    hist_curr: HistogramData,
    hist_ref: Optional[HistogramData] = None,
    orientation="v",
    color_options: ColorOptions,
    current_name: str = "Current",
    reference_name: str = "Reference",
):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name=current_name,
            x=hist_curr.x,
            y=hist_curr.count,
            marker_color=color_options.get_current_data_color(),
            orientation=orientation,
        )
    )
    if hist_ref is not None:
        fig.add_trace(
            go.Bar(
                name=reference_name,
                x=hist_ref.x,
                y=hist_ref.count,
                marker_color=color_options.get_reference_data_color(),
                orientation=orientation,
            )
        )

    return fig


def get_distribution_plot_figure(
    *,
    current_distribution: Distribution,
    reference_distribution: Optional[Distribution],
    color_options: ColorOptions,
    orientation: str = "v",
    current_name: str = "Current",
    reference_name: str = "Reference",
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name=current_name,
            x=current_distribution.x,
            y=current_distribution.y,
            marker_color=color_options.get_current_data_color(),
            orientation=orientation,
        )
    )
    if reference_distribution is not None:
        fig.add_trace(
            go.Bar(
                name=reference_name,
                x=reference_distribution.x,
                y=reference_distribution.y,
                marker_color=color_options.get_reference_data_color(),
                orientation=orientation,
            )
        )

    return fig
