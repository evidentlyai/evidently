from typing import Generator
from typing import List
from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics.base import Metric
from evidently.future.metrics.base import MetricCalculation
from evidently.future.metrics.base import MetricTestResult
from evidently.future.metrics.base import TResult
from evidently.future.metrics.container import MetricContainer
from evidently.future.report import Context


class GroupByMetric(Metric):
    metric: Metric

    column_name: str
    label: object

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        pass


class GroupByMetricCalculation(MetricCalculation[TResult, GroupByMetric]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        curr = current_data.subdataset(self.metric.column_name, self.metric.label)
        ref = reference_data.subdataset(self.metric.column_name, self.metric.label) if reference_data else None
        return self.metric.metric.to_calculation().calculate(curr, ref)

    def display_name(self) -> str:
        return f"{self.metric.metric.to_calculation().display_name()} group by '{self.metric.column_name}' for label: '{self.metric.label}'"

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return self.metric.metric.get_tests(value)

    @property
    def column_name(self) -> str:
        return self.metric.column_name


class GroupBy(MetricContainer):
    def __init__(self, metric: Metric, column_name: str):
        self._column_name = column_name
        self._metric = metric

    def generate_metrics(self, context: Context) -> List[Metric]:
        labels = context.column(self._column_name).labels()
        return [GroupByMetric(metric=self._metric, column_name=self._column_name, label=label) for label in labels]

    def label_metric(self, label: object) -> Metric:
        return GroupByMetric(metric=self._metric, column_name=self._column_name, label=label)
