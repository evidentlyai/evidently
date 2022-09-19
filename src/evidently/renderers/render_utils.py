import plotly.graph_objs as go

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
