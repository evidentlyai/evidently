from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics.base import TResult
from evidently.v2.metrics.container import MetricContainer
from evidently.v2.report import Context


class GroupByMetric(Metric):
    class Config:
        type_alias = "evidently:metric_v2:GroupByMetric"

    def __init__(self, metric: Metric, column_name: str, label: object):
        super().__init__(f"{metric.id}:group_by:{label}")
        self._metric = metric
        self._column_name = column_name
        self._label = label

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        curr = current_data.subdataset(self._column_name, self._label)
        ref = reference_data.subdataset(self._column_name, self._label) if reference_data else None
        return self._metric.calculate(curr, ref)

    def display_name(self) -> str:
        return f"{self._metric.display_name()} group by '{self._column_name}' for label: '{self._label}'"

    @property
    def column_name(self) -> str:
        return self._column_name


class GroupBy(MetricContainer):
    def __init__(self, metric: Metric, column_name: str):
        self._column_name = column_name
        self._metric = metric

    def generate_metrics(self, context: Context) -> List[Metric]:
        labels = context.column(self._column_name).labels()
        return [GroupByMetric(self._metric, self._column_name, label) for label in labels]

    def label_metric(self, label: object) -> Metric:
        return GroupByMetric(self._metric, self._column_name, label)
