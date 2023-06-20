import uuid
from enum import Enum
from typing import Dict
from typing import Iterable
from typing import List

from plotly import graph_objs as go
from pydantic import BaseModel

from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EnumValueMixin
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_figure
from evidently.report import Report
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import T


class ReportFilter(BaseModel):
    metadata_values: Dict[str, str]

    def filter(self, report: Report):
        return all(report.metadata.get(key) == value for key, value in self.metadata_values.items())


class PanelValue(BaseModel):
    metric_id: str
    field_path: str

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


class DashboardPanel(EnumValueMixin):
    id: uuid.UUID
    title: str
    filter: ReportFilter
    values: List[PanelValue]
    plot_type: PlotType
    size: WidgetSize = WidgetSize.FULL

    def build_widget(self, reports: Iterable[Report]) -> BaseWidgetInfo:
        x, ys = [], [[] for _ in range(len(self.values))]
        for report in reports:
            if not self.filter.filter(report):
                continue
            x.append(report.timestamp)
            for i, value in enumerate(self.values):
                ys[i].append(value.get(report))

        fig = go.Figure()
        for y in ys:
            plot = self.plot_type_cls(x=x, y=y)
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


class DashboardConfig(BaseModel):
    name: str
    panels: List[DashboardPanel]

    def build_dashboard_info(self, reports: Iterable[Report]) -> DashboardInfo:
        return DashboardInfo(self.name, widgets=[p.build_widget(reports) for p in self.panels])


class Dashboard(Display):
    def __init__(self, config: DashboardConfig):
        super().__init__()
        self.reports = []
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
