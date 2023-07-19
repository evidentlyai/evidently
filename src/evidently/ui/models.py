import dataclasses
import datetime
import uuid
from typing import Any
from typing import List

from pydantic import BaseModel

from evidently.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.test_suite import TestSuite


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
