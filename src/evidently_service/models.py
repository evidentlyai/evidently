import datetime
from typing import List

from pydantic import BaseModel

from evidently.base_metric import Metric
from evidently.report import Report


class ProjectModel(BaseModel):
    project_name: str


class MetricModel(BaseModel):
    id: str

    @classmethod
    def from_metric(cls, metric: Metric):
        return cls(id=metric.get_id())


class ReportModel(BaseModel):
    timestamp: datetime.datetime
    metrics: List[MetricModel]

    @classmethod
    def from_report(cls, report: Report):
        return cls(timestamp=report.timestamp, metrics=[
            MetricModel.from_metric(m) for m in report._first_level_metrics
        ])
