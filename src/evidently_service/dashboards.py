import uuid
from typing import Dict
from typing import Iterable

import plotly.subplots
from plotly import graph_objs as go
from pydantic import BaseModel

from evidently.model.dashboard import DashboardInfo
from evidently.renderers.html_widgets import plotly_figure
from evidently.report import Report


class ReportFilter(BaseModel):
    metadata_values: Dict[str, str]

    def filter(self, report: Report):
        return all(report.metadata.get(key) == value for key, value in self.metadata_values.items())


class DashboardValue(BaseModel):
    metric_id: str
    field_path: str

    def get(self, report: Report):
        # todo: make this more efficient
        for metric in report.as_dict()["metrics"]:
            if metric["metric"] == self.metric_id:
                # todo: nested path
                return metric["result"][self.field_path]
        return None


class DashboardConfig(BaseModel):
    id: uuid.UUID
    name: str
    filter: ReportFilter
    value: DashboardValue

    def build_dashboard_info(self, reports: Iterable[Report]) -> DashboardInfo:
        x, y = [], []
        for report in reports:
            if self.filter.filter(report):
                x.append(report.timestamp)
                y.append(self.value.get(report))

        print(x)
        print(y)
        scatter = go.Scatter(x=x, y=y)
        fig = plotly.subplots.make_subplots()
        fig.add_trace(scatter, 1, 1)
        return DashboardInfo(self.name, widgets=[plotly_figure(title="kek", figure=fig)])
