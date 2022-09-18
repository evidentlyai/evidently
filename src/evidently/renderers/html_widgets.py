from enum import Enum
from typing import List
from typing import Optional
from typing import Union

import dataclasses
import plotly.graph_objs as go

from evidently.model.widget import BaseWidgetInfo, WidgetType
from evidently.options import ColorOptions


class WidgetSize(Enum):
    HALF = 1
    FULL = 2


def plotly_figure(
        *,
        title: str,
        figure: go.Figure,
        size: WidgetSize = WidgetSize.FULL
) -> BaseWidgetInfo:
    fig_json = figure.to_plotly_json()
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.BIG_GRAPH.value,
        size=size.value,
        params={"data": fig_json["data"], "layout": fig_json["layout"]},
    )


class CounterData:
    label: str
    value: str

    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    @staticmethod
    def float(label: str, value: float, precision: int) -> 'CounterData':
        return CounterData(label, f"{value:.{precision}}")


def counter(
        *,
        counters: List[CounterData],
        title: str,
        size: WidgetSize = WidgetSize.FULL,
) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.COUNTER.value,
        size=size.value,
        params={
            "counters": [{"value": item.value, "label": item.label} for item in counters]
        },
    )


def table_data(
        *,
        column_names: List[str],
        data: List[List[object]],
        size: WidgetSize = WidgetSize.FULL
) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title="",
        type=WidgetType.TABLE.value,
        params={
            "header": column_names,
            "data": [[str(item) for item in row] for row in data],
        },
        size=size.value,
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
        size: WidgetSize = WidgetSize.FULL,
) -> BaseWidgetInfo:
    color_options = color_options if color_options is not None else ColorOptions()
    figure = go.Figure()
    curr_bar = go.Bar(
        name=primary_hist.name,
        x=primary_hist.x,
        y=primary_hist.count,
        marker_color=color_options.get_current_data_color(),
        orientation=orientation,
    )
    figure.add_trace(curr_bar)
    if secondary_hist is not None:
        ref_bar = go.Bar(
            name=secondary_hist.name,
            x=secondary_hist.x,
            y=secondary_hist.count,
            marker_color=color_options.get_reference_data_color(),
            orientation=orientation,
        )
        figure.add_trace(ref_bar)

    return plotly_figure(title=title, figure=figure, size=size)
