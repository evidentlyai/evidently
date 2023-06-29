import abc
import uuid
from enum import Enum
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

from plotly import graph_objs as go
from pydantic import BaseModel

from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import PolymorphicModel
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.report import Report
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import T


class ReportFilter(BaseModel):
    metadata_values: Dict[str, str]
    tag_values: List[str]

    def filter(self, report: Report):
        return all(report.metadata.get(key) == value for key, value in self.metadata_values.items()) and all(
            tag in report.tags for tag in self.tag_values
        )


class PanelValue(BaseModel):
    metric_id: str
    field_path: str
    legend: Optional[str] = None

    def get(self, report: Report):
        # todo: make this more efficient
        for metric in report.as_dict()["metrics"]:
            if metric["metric"] == self.metric_id:
                # todo: nested path
                return metric["result"][self.field_path]
        return None


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
        points = []
        for report in reports:
            if not self.filter.filter(report):
                continue
            points.append((report.timestamp, [value.get(report) for value in self.values]))

        points.sort(key=lambda x: x[0])
        x = [p[0] for p in points]
        ys = [[p[1][i] for p in points] for i in range(len(self.values))]
        fig = go.Figure()
        for val, y in zip(self.values, ys):
            plot = self.plot_type_cls(x=x, y=y, name=val.legend, legendgroup=val.legend)
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
        if self.plot_type == PlotType.HISTOGRAM:
            return go.Histogram
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
        ct = CounterData.float(self.title, value, 3) if isinstance(value, float) else CounterData.int(self.title, value)
        return counter(title=self.title, counters=[ct], size=self.size)

    def _get_counter_value(self, reports: Iterable[Report]):
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        if self.agg == CounterAgg.LAST:
            return max(((r.timestamp, self.value.get(r)) for r in reports), key=lambda x: x[0])[1]
        if self.agg == CounterAgg.SUM:
            return sum(self.value.get(r) or 0 for r in reports)
        raise ValueError(f"Unknown agg type {self.agg}")


class DashboardConfig(BaseModel):
    name: str
    panels: List[DashboardPanel]

    def build_dashboard_info(self, reports: Iterable[Report]) -> DashboardInfo:
        return DashboardInfo(self.name, widgets=[p.build_widget(reports) for p in self.panels])


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
