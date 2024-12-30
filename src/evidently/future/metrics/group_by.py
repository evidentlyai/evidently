from typing import Generator
from typing import List
from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics import MetricCalculationBase
from evidently.future.metrics.base import MetricTestResult
from evidently.future.metrics.base import TResult
from evidently.future.metrics.container import MetricContainer
from evidently.future.report import Context


class GroupByMetricCalculationBase(MetricCalculationBase):
    def __init__(self, metric: MetricCalculationBase, column_name: str, label: object):
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

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return self._metric.get_tests(value)

    @property
    def column_name(self) -> str:
        return self._column_name


class GroupBy(MetricContainer):
    def __init__(self, metric: MetricCalculationBase, column_name: str):
        self._column_name = column_name
        self._metric = metric

    def generate_metrics(self, context: Context) -> List[MetricCalculationBase]:
        labels = context.column(self._column_name).labels()
        return [GroupByMetricCalculationBase(self._metric, self._column_name, label) for label in labels]

    def label_metric(self, label: object) -> MetricCalculationBase:
        return GroupByMetricCalculationBase(self._metric, self._column_name, label)
