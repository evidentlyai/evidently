from typing import Optional

from plotly import graph_objs as go

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

def plot_range(fig, left, right):
    fig = go.Figure(fig)
    fig.add_vrect(x0=left, x1=right, fillcolor="green", opacity=0.25, line_width=0)
    return fig
