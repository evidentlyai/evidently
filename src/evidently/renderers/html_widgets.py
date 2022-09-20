import re
from enum import Enum
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union
from uuid import uuid4

import dataclasses
import plotly.graph_objs as go

from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import WidgetType
from evidently.options import ColorOptions


class WidgetSize(Enum):
    HALF = 1
    FULL = 2


def plotly_data(*, title: str, data: dict, layout: dict, size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.BIG_GRAPH.value,
        size=size.value,
        params={"data": data, "layout": layout},
    )


def plotly_figure(*, title: str, figure: go.Figure, size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    fig_json = figure.to_plotly_json()
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.BIG_GRAPH.value,
        size=size.value,
        params={"data": fig_json["data"], "layout": fig_json["layout"]},
    )


class GraphData:
    title: str
    data: dict
    layout: dict

    def __init__(self, title: str, data: dict, layout: dict):
        self.title = title
        self.data = data
        self.layout = layout

    @staticmethod
    def figure(title: str, figure: go.Figure):
        data = figure.to_plotly_json()
        return GraphData(title, data["data"], data["layout"])


def plotly_graph_tabs(*, title: str, figures: List[GraphData], size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.TABBED_GRAPH.value,
        size=size.value,
        params={
            "graphs": [
                {
                    "id": str(uuid4()),
                    "title": graph.title,
                    "graph": {
                        "data": graph.data,
                        "layout": graph.layout,
                    },
                }
                for graph in figures
            ]
        },
    )


class CounterData:
    label: str
    value: str

    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    @staticmethod
    def float(label: str, value: float, precision: int) -> "CounterData":
        return CounterData(label, f"{value:.{precision}}")


def counter(
    *,
    counters: List[CounterData],
    title: str = "",
    size: WidgetSize = WidgetSize.FULL,
) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.COUNTER.value,
        size=size.value,
        params={"counters": [{"value": item.value, "label": item.label} for item in counters]},
    )


def header_text(*, label: str, size: WidgetSize = WidgetSize.FULL):
    return BaseWidgetInfo(
        title="",
        type=WidgetType.COUNTER.value,
        size=size.value,
        params={"counters": [{"value": "", "label": label}]},
    )


def table_data(
    *, column_names: Iterable[str], data: Iterable[Iterable], title: str = "", size: WidgetSize = WidgetSize.FULL
) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.TABLE.value,
        params={
            "header": column_names,
            "data": [[str(item) for item in row] for row in data],
        },
        size=size.value,
    )


class ColumnType(Enum):
    STRING = "string"
    LINE = "line"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@dataclasses.dataclass
class ColumnDefinition:
    title: str
    field_name: str
    type: ColumnType = ColumnType.STRING
    sort: Optional[SortDirection] = None
    options: Optional[dict] = None

    def as_dict(self) -> dict:
        result: dict = {"title": self.title, "field": self.field_name}
        if self.type != ColumnType.STRING:
            result["type"] = self.type.value
        if self.sort is not None:
            result["sort"] = self.sort.value
        if self.options is not None:
            result["options"] = self.options
        return result


def rich_table_data(
    *,
    title: str = "",
    size: WidgetSize = WidgetSize.FULL,
    rows_per_page: int = 10,
    columns: List[ColumnDefinition],
    data: List[dict],
) -> BaseWidgetInfo:
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.BIG_TABLE.value,
        details="",
        alerts=[],
        alertsPosition="row",
        insights=[],
        size=size.value,
        params={
            "rowsPerPage": min(len(data), rows_per_page),
            "columns": [column.as_dict() for column in columns],
            "data": data,
        },
        additionalGraphs=[],
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
