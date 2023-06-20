import uuid
from typing import Dict
from typing import Iterable
from typing import List

import plotly.subplots
from plotly import graph_objs as go
from pydantic import BaseModel

from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
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

    def get(self, report: Report):
        # todo: make this more efficient
        for metric in report.as_dict()["metrics"]:
            if metric["metric"] == self.metric_id:
                # todo: nested path
                return metric["result"][self.field_path]
        return None


class DashboardPanel(BaseModel):
    id: uuid.UUID
    name: str
    filter: ReportFilter
    value: PanelValue

    def build_widget(self, reports: Iterable[Report]) -> BaseWidgetInfo:
        x, y = [], []
        for report in reports:
            if self.filter.filter(report):
                x.append(report.timestamp)
                y.append(self.value.get(report))

        scatter = go.Scatter(x=x, y=y)
        fig = plotly.subplots.make_subplots()
        fig.add_trace(scatter, 1, 1)
        return plotly_figure(title="kek", figure=fig)


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
