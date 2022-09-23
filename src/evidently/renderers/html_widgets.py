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


class GraphData:
    title: str
    data: dict
    layout: dict

    def __init__(self, title: str, data: dict, layout: dict):
        """
        create GraphData object for usage in plotly_graph_tabs or plotly_data.

        Args:
            title: title of graph
            data: plotly figure data
            layout: plotly figure layout
        """
        self.title = title
        self.data = data
        self.layout = layout

    @staticmethod
    def figure(title: str, figure: go.Figure):
        """
        create GraphData from plotly figure itself
        Args:
            title: title of graph
            figure: plotly figure for getting data from
        """
        data = figure.to_plotly_json()
        return GraphData(title, data["data"], data["layout"])


def plotly_graph(*, graph_data: GraphData, size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    """
    generate plotly plot with given GraphData object.

    Args:
        graph_data: plot data for widget
        size: size of widget to render

    Example:
        >>> figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
        >>> f_dict = figure.to_plotly_json()
        >>> bar_graph_data = GraphData(title="Some plot title", data=f_dict["data"], layout=f_dict["layout"])
        >>> widget_info = plotly_graph(graph_data=bar_graph_data, size=WidgetSize.FULL)
    """
    return BaseWidgetInfo(
        title=graph_data.title,
        type=WidgetType.BIG_GRAPH.value,
        size=size.value,
        params={"data": graph_data.data, "layout": graph_data.layout},
    )


def plotly_data(*, title: str, data: dict, layout: dict, size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    """
    generate plotly plot with given data and layout (can be generated from plotly).

    Args:
        title: widget title
        data: plotly figure data
        layout: plotly figure layout
        size: widget size

    Example:
        >>> figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
        >>> f_dict = figure.to_plotly_json()
        >>> widget_info = plotly_data(title="Some plot title", data=f_dict["data"], layout=f_dict["layout"])
    """
    return plotly_graph(graph_data=GraphData(title, data, layout), size=size)


def plotly_figure(*, title: str, figure: go.Figure, size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    """
    generate plotly plot based on given plotly figure object.

    Args:
        title: title of widget
        figure: plotly figure which should be rendered as widget
        size: size of widget, default to WidgetSize.FULL

    Example:
        >>> bar_figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
        >>> widget_info = plotly_figure(title="Bar plot widget", figure=bar_figure, size=WidgetSize.FULL)
    """
    return plotly_graph(graph_data=GraphData.figure(title=title, figure=figure), size=size)


def plotly_graph_tabs(*, title: str, figures: List[GraphData], size: WidgetSize = WidgetSize.FULL) -> BaseWidgetInfo:
    """
    generate Tab widget with multiple graphs

    Args:
        title: widget title
        figures: list of graphs with tab titles
        size: widget size

    Example:
        >>> bar_figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
        >>> line_figure = go.Figure(go.Line(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
        >>> widget_info = plotly_graph_tabs(
        ...     title="Tabbed widget",
        ...     figures=[GraphData.figure("Bar", bar_figure), GraphData.figure("Line", line_figure)],
        ... )
    """
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
        """
        creates CounterData for counter widget with given label and value.

        Args:
            label: counter label
            value: counter value
        """
        self.label = label
        self.value = value

    @staticmethod
    def float(label: str, value: float, precision: int) -> "CounterData":
        """
        create CounterData for float value with given precision.

        Args:
            label: counter label
            value: float value of counter
            precision: decimal precision
        """
        return CounterData(label, f"{value:.{precision}}")


def counter(
    *,
    counters: List[CounterData],
    title: str = "",
    size: WidgetSize = WidgetSize.FULL,
) -> BaseWidgetInfo:
    """
    generate widget with given counters

    Args:
        title: widget title
        counters: list of counters in widget
        size: widget size
    """
    return BaseWidgetInfo(
        title=title,
        type=WidgetType.COUNTER.value,
        size=size.value,
        params={"counters": [{"value": item.value, "label": item.label} for item in counters]},
    )


def header_text(*, label: str, size: WidgetSize = WidgetSize.FULL):
    """
    generate widget with some text as header

    Args:
        label: text to display
        size: widget size
    """
    return BaseWidgetInfo(
        title="",
        type=WidgetType.COUNTER.value,
        size=size.value,
        params={"counters": [{"value": "", "label": label}]},
    )


def table_data(
    *, column_names: Iterable[str], data: Iterable[Iterable], title: str = "", size: WidgetSize = WidgetSize.FULL
) -> BaseWidgetInfo:
    """
    generate simple table with given columns and data

    Args:
        column_names: list of column names in display order
        data: list of data rows (lists of object to show in table in order of columns), object will be converted to str
        title: widget title
        size: widget size

    Example:
        >>> columns = ["Column A", "Column B"]
        >>> in_table_data = [[1, 2], [3, 4]]
        >>> widget_info = table_data(column_names=columns, data=in_table_data, title="Table")
    """
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
    """
    generate widget with rich table: with additional column types and details for rows

    Args:
         title: widget title
         size: widget size
         rows_per_page: maximum number per page to show
         columns: list of columns in table
         data: list of dicts with data (key-value pairs, keys is according to ColumnDefinition.field_name)

    Example:
        >>> columns_def = [
        ...     ColumnDefinition("Column A", "field_1"),
        ...     ColumnDefinition("Column B", "field_2", ColumnType.HISTOGRAM,
        ...                      options={"xField": "x", "yField": "y", "color": "#ed0400"}),
        ...     ColumnDefinition("Column C", "field_3", sort=SortDirection.ASC),
        ... ]
        >>> in_table_data = [
        ...     dict(field_1="a", field_2=dict(x=[1, 2, 3], y=[10, 11, 3]), field_3="2"),
        ...     dict(field_1="b", field_2=dict(x=[1, 2, 3], y=[10, 11, 3]), field_3="1"),
        ... ]
        >>> widget_info = rich_table_data(title="Rich table", rows_per_page=10, columns=columns_def, data=in_table_data)
    """
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
    y: List[Union[int, float]]


def histogram(
    title: str,
    primary_hist: HistogramData,
    secondary_hist: Optional[HistogramData],
    *,
    color_options: Optional[ColorOptions] = None,
    orientation: str = "v",
    size: WidgetSize = WidgetSize.FULL,
) -> BaseWidgetInfo:
    """
    generate widget with one or two histogram

    Args:
        title: widget title
        primary_hist: first histogram to show in widget
        secondary_hist: optional second histogram to show in widget
        orientation: bars orientation in histograms
        color_options: color options to use for widgets
        size: widget size
    Example:
        >>> ref_hist = HistogramData("Histogram 1", x=["a", "b", "c"], y=[1, 2, 3])
        >>> curr_hist = HistogramData("Histogram 2", x=["a", "b", "c"], y=[3, 2 ,1])
        >>> widget_info = histogram("Histogram example", ref_hist, curr_hist)
    """
    color_options = color_options if color_options is not None else ColorOptions()
    figure = go.Figure()
    curr_bar = go.Bar(
        name=primary_hist.name,
        x=primary_hist.x,
        y=primary_hist.y,
        marker_color=color_options.get_current_data_color(),
        orientation=orientation,
    )
    figure.add_trace(curr_bar)
    if secondary_hist is not None:
        ref_bar = go.Bar(
            name=secondary_hist.name,
            x=secondary_hist.x,
            y=secondary_hist.y,
            marker_color=color_options.get_reference_data_color(),
            orientation=orientation,
        )
        figure.add_trace(ref_bar)

    return plotly_figure(title=title, figure=figure, size=size)
