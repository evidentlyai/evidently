from typing import Dict
from typing import List
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently.future.metric_types import ByLabelCountValue
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import CountValue
from evidently.future.metric_types import MeanStdValue
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import SingleValue
from evidently.model.widget import BaseWidgetInfo


class ReportItem(BaseModel):
    pass


class ReportModel(BaseModel):
    items: List[ReportItem]


class SnapshotModel(BaseModel):
    report: ReportModel
    metric_results: Dict[MetricId, Union[SingleValue, ByLabelValue, CountValue, MeanStdValue, ByLabelCountValue]]
    top_level_metrics: List[MetricId]
    widgets: List[BaseWidgetInfo]
