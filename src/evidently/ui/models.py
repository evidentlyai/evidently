import dataclasses
import datetime
import uuid
from typing import Any
from typing import List
from typing import Optional

from pydantic import BaseModel

from evidently.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.ui.workspace import Project


class ProjectModel(BaseModel):
    id: uuid.UUID
    project_name: str
    description: str
    date_from: Optional[datetime.datetime]
    date_to: Optional[datetime.datetime]

    @classmethod
    def from_project(cls, p: Project):
        return cls(id=p.id, project_name=p.name, date_from=p.date_from, date_to=p.date_to, description=p.description)


class MetricModel(BaseModel):
    id: str

    @classmethod
    def from_metric(cls, metric: Metric):
        return cls(id=metric.get_id())


class ReportModel(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime
    metrics: List[MetricModel]

    @classmethod
    def from_report(cls, report: Report):
        return cls(
            id=report.id,
            timestamp=report.timestamp,
            metrics=[MetricModel.from_metric(m) for m in report._first_level_metrics],
        )


class TestSuiteModel(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime

    @classmethod
    def from_report(cls, report: TestSuite):
        return cls(
            id=report.id,
            timestamp=report.timestamp,
        )


class DashboardInfoModel(BaseModel):
    name: str
    widgets: List[Any]

    @classmethod
    def from_dashboard_info(cls, dashboard_info: DashboardInfo):
        return cls(**dataclasses.asdict(dashboard_info))
