import abc
import datetime
import traceback
import uuid
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import plotly.io as pio
from plotly import graph_objs as go
from pydantic import BaseModel
from pydantic import validator

from evidently.base_metric import Metric
from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import FieldPath
from evidently.pydantic_utils import PolymorphicModel
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.report import Report
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import T

COLOR_DISCRETE_SEQUENCE = (
    "#ed0400",
    "#0a5f38",
    "#6c3461",
    "#71aa34",
    "#6b8ba4",
    "#60460f",
    "#a00498",
    "#017b92",
    "#ffad01",
    "#464196",
)

pio.templates[pio.templates.default].layout.colorway = COLOR_DISCRETE_SEQUENCE


class ReportFilter(BaseModel):
    metadata_values: Dict[str, str]
    tag_values: List[str]

    def filter(self, report: Report):
        return all(report.metadata.get(key) == value for key, value in self.metadata_values.items()) and all(
            tag in report.tags for tag in self.tag_values
        )


def get_nested(d: dict, path: List[str]):
    if len(path) == 1:
        return d[path[0]]
    return get_nested(d[path[0]], path[1:])


_not_set = object()


def _getattr_or_getitem(obj: Any, item: str, default=_not_set):
    if isinstance(obj, dict):
        if default is _not_set:
            return obj[item]
        return obj.get(item, default)
    if default is _not_set:
        return getattr(obj, item)
    return getattr(obj, item, default)


def getattr_nested(obj: Any, path: List[str], default=_not_set):
    item = path[0]
    if len(path) == 1:
        return _getattr_or_getitem(obj, item, default)
    return getattr_nested(_getattr_or_getitem(obj, item, default), path[1:], default)


class PanelValue(BaseModel):
    field_path: Union[str, FieldPath]
    metric_id: Optional[str] = None
    metric_hash: Optional[int] = None
    metric_args: Dict[str, Union[EvidentlyBaseModel, Any]] = {}
    legend: Optional[str] = None

    @property
    def field_path_str(self):
        if isinstance(self.field_path, FieldPath):
            return self.field_path.get_path()
        return self.field_path

    @validator("field_path")
    def validate_field_path(cls, value):
        if isinstance(value, FieldPath):
            value = value.get_path()
        return value

    def metric_matched(self, metric: Metric) -> bool:
        if self.metric_hash is not None and hash(metric) == self.metric_hash:
            return True
        if self.metric_id is not None and self.metric_id != metric.get_id():
            return False
        for field, value in self.metric_args.items():
            try:
                if getattr_nested(metric, field.split(".")) != value:
                    return False
            except AttributeError:
                return False
        return True

    def get(self, report: Report) -> Dict[Metric, Any]:
        results = {}
        for metric in report._first_level_metrics:
            if self.metric_matched(metric):
                try:
                    results[metric] = getattr_nested(metric.get_result(), self.field_path_str.split("."))
                except AttributeError:
                    pass
        return results


class PlotType(Enum):
    # todo: move it to core lib?
    SCATTER = "scatter"
    BAR = "bar"
    LINE = "line"
    HISTOGRAM = "histogram"


class DashboardPanel(EnumValueMixin, PolymorphicModel):
    id: uuid.UUID = uuid.uuid4()
    title: str
    filter: ReportFilter
    size: WidgetSize = WidgetSize.FULL

    @abc.abstractmethod
    def build_widget(self, reports: Iterable[Report]) -> BaseWidgetInfo:
        raise NotImplementedError


class DashboardPanelPlot(DashboardPanel):
    values: List[PanelValue]
    plot_type: PlotType

    def build_widget(self, reports: Iterable[Report]) -> BaseWidgetInfo:

        points: List[Dict[Metric, List[Tuple[datetime.datetime, Any]]]] = [{} for _ in range(len(self.values))]
        for report in reports:
            if not self.filter.filter(report):
                continue
            for i, value in enumerate(self.values):
                for metric, metric_field_value in value.get(report).items():
                    if metric not in points[i]:
                        points[i][metric] = []
                    points[i][metric].append((report.timestamp, metric_field_value))

        fig = go.Figure(layout={"showlegend": True})
        for val, metric_pts in zip(self.values, points):
            if len(metric_pts) == 0:
                # no matching metrics, show error?
                continue

            for metric, pts in metric_pts.items():
                pts.sort(key=lambda x: x[0])
                params = []
                for name, value in metric.dict().items():
                    if name in ["type"]:
                        continue
                    if value is None:
                        continue
                    params.append(f"{name}: {value}")
                params_join = "<br>".join(params)
                hover = f"<b>Timestamp: %{{x}}</b><br><b>Value: %{{y}}</b><br>{params_join}<br>.{val.field_path}"
                if self.plot_type == PlotType.HISTOGRAM:
                    plot = go.Histogram(
                        x=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                    )
                else:
                    plot = self.plot_type_cls(
                        x=[p[0] for p in pts],
                        y=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                    )
                fig.add_trace(plot)
        return plotly_figure(title=self.title, figure=fig, size=self.size)

    @property
    def plot_type_cls(self):
        if self.plot_type == PlotType.SCATTER:
            return go.Scatter
        if self.plot_type == PlotType.BAR:
            return go.Bar
        if self.plot_type == PlotType.LINE:
            return go.Line
        raise ValueError(f"Unsupported plot type {self.plot_type}")


class CounterAgg(Enum):
    SUM = "sum"
    LAST = "last"
    NONE = "none"


class DashboardPanelCounter(DashboardPanel):
    agg: CounterAgg
    value: Optional[PanelValue] = None
    text: Optional[str] = None

    def build_widget(self, reports: Iterable[Report]) -> BaseWidgetInfo:
        if self.agg == CounterAgg.NONE:
            return counter(counters=[CounterData(self.title, self.text or "")], size=self.size)
        value = self._get_counter_value(reports)
        if isinstance(value, float):
            ct = CounterData.float(self.text or "", value, 3)
        else:
            ct = CounterData.int(self.text or "", value)
        return counter(title=self.title, counters=[ct], size=self.size)

    def _get_counter_value(self, reports: Iterable[Report]):
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        if self.agg == CounterAgg.LAST:
            return max(((r.timestamp, v) for r in reports for v in self.value.get(r).values()), key=lambda x: x[0])[1]
        if self.agg == CounterAgg.SUM:
            return sum(v or 0 for r in reports for v in self.value.get(r).values())
        raise ValueError(f"Unknown agg type {self.agg}")


class DashboardConfig(BaseModel):
    name: str
    panels: List[DashboardPanel]

    def build_dashboard_info(self, reports: Iterable[Report]) -> DashboardInfo:
        return DashboardInfo(self.name, widgets=[self.build_widget(p, reports) for p in self.panels])

    def build_widget(self, panel: DashboardPanel, reports: Iterable[Report]) -> BaseWidgetInfo:
        try:
            return panel.build_widget(reports)
        except Exception as e:
            traceback.print_exc()
            return counter(counters=[CounterData(f"{e.__class__.__name__}: {e.args[0]}", "Error")])

    def add_panel(self, panel: DashboardPanel):
        self.panels.append(panel)


class Dashboard(Display):
    def __init__(self, config: DashboardConfig):
        super().__init__()
        self.reports: List[Report] = []
        self.config = config

    def add_report(self, report: Report):
        self.reports.append(report)

    def as_dict(
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        raise NotImplementedError

    def _get_payload(self) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def _parse_payload(cls, payload: Dict) -> T:
        raise NotImplementedError

    def _build_dashboard_info(self):
        return "er_" + str(uuid.uuid4()).replace("-", ""), self.config.build_dashboard_info(self.reports), {}
