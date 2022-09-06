from typing import List
from typing import Optional
from typing import Union

import dataclasses

import plotly.graph_objs as go

from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


def plotly_figure(title: str, figure: go.Figure, size: int = 2) -> BaseWidgetInfo:
    fig_json = figure.to_plotly_json()
    return BaseWidgetInfo(
        title=title,
        type="big_graph",
        size=size,
        params={"data": fig_json["data"], "layout": fig_json["layout"]},
    )


@dataclasses.dataclass
class HistogramData:
    name: str
    x: list
    count: List[Union[int, float]]


def histogram(
        title: str,
        primary_hist: HistogramData,
        secondary_hist: Optional[HistogramData],
        *,
        color_options: Optional[ColorOptions] = None,
        orientation: str = "v",
        size: int = 2) -> BaseWidgetInfo:
    color_options = color_options if color_options is not None else ColorOptions()
    figure = go.Figure()
    curr_bar = go.Bar(
        name=primary_hist.name,
        x=primary_hist.x,
        y=primary_hist.count,
        marker_color=color_options.get_current_data_color(),
        orientation=orientation
    )
    figure.add_trace(curr_bar)
    if secondary_hist is not None:
        ref_bar = go.Bar(
            name=secondary_hist.name,
            x=secondary_hist.x,
            y=secondary_hist.count,
            marker_color=color_options.get_reference_data_color(),
            orientation=orientation
        )
        figure.add_trace(ref_bar)

    return plotly_figure(title, figure, size)
