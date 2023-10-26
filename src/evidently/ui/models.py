import dataclasses
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently._pydantic_compat import BaseModel
from evidently.base_metric import Metric
from evidently.model.dashboard import DashboardInfo
from evidently.report import Report
from evidently.suite.base_suite import MetadataValueType
from evidently.test_suite import TestSuite
from evidently.ui.workspace import Project


class MetricModel(BaseModel):
    id: str

    @classmethod
    def from_metric(cls, metric: Metric):
        return cls(id=metric.get_id())


class ReportModel(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime
    metrics: List[MetricModel]
    metadata: Dict[str, MetadataValueType]
    tags: List[str]

    @classmethod
    def from_report(cls, report: Report):
        return cls(
            id=report.id,
            timestamp=report.timestamp,
            metrics=[MetricModel.from_metric(m) for m in report._first_level_metrics],
            metadata=report.metadata,
            tags=report.tags,
        )


class TestSuiteModel(BaseModel):
    id: uuid.UUID
    timestamp: datetime.datetime
    metadata: Dict[str, MetadataValueType]
    tags: List[str]

    @classmethod
    def from_report(cls, report: TestSuite):
        return cls(id=report.id, timestamp=report.timestamp, metadata=report.metadata, tags=report.tags)


class DashboardInfoModel(BaseModel):
    name: str
    widgets: List[Any]
    min_timestamp: Optional[datetime.datetime] = None
    max_timestamp: Optional[datetime.datetime] = None

    @classmethod
    def from_dashboard_info(cls, dashboard_info: DashboardInfo):
        return cls(**dataclasses.asdict(dashboard_info))

    @classmethod
    def from_project_with_time_range(
        cls,
        project: Project,
        timestamp_start: Optional[datetime.datetime] = None,
        timestamp_end: Optional[datetime.datetime] = None,
    ):
        time_range: Dict[str, Optional[datetime.datetime]]
        reports = project.reports_and_test_suites
        if len(reports) == 0:
            time_range = {"min_timestamp": None, "max_timestamp": None}
        else:
            time_range = dict(
                min_timestamp=min(r.timestamp for r in reports.values()),
                max_timestamp=max(r.timestamp for r in reports.values()),
            )

        info = project.build_dashboard_info(timestamp_start=timestamp_start, timestamp_end=timestamp_end)

        return cls(**dataclasses.asdict(info), **time_range)
