from typing import Dict
from typing import List

from evidently._pydantic_compat import BaseModel
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult


class ReportItem(BaseModel):
    pass


class ReportModel(BaseModel):
    items: List[ReportItem]


class SnapshotModel(BaseModel):
    report: ReportModel
    metric_results: Dict[MetricId, MetricResult]
    top_level_metrics: List[MetricId]
    # widgets: List[BaseWidgetInfo]
