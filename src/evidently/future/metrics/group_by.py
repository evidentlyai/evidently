from typing import List
from typing import Optional
from typing import Sequence

from evidently.future.container import MetricContainer
from evidently.future.datasets import Dataset
from evidently.future.metric_types import BoundTest
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricCalculation
from evidently.future.metric_types import TResult
from evidently.future.report import Context


class GroupByMetric(Metric):
    metric: Metric

    column_name: str
    label: object

    def get_bound_tests(self, context: Context) -> Sequence[BoundTest]:
        return self.metric.get_bound_tests(context)


class GroupByMetricCalculation(MetricCalculation[TResult, GroupByMetric]):
    _calculation: Optional[MetricCalculation[TResult, GroupByMetric]] = None

    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        curr = current_data.subdataset(self.metric.column_name, self.metric.label)
        ref = reference_data.subdataset(self.metric.column_name, self.metric.label) if reference_data else None
        return self.calculation.calculate(context, curr, ref)

    def display_name(self) -> str:
        return (
            f"{self.calculation.display_name()} group by '{self.metric.column_name}' for label: '{self.metric.label}'"
        )

    @property
    def column_name(self) -> str:
        return self.metric.column_name

    @property
    def calculation(self) -> MetricCalculation:
        if self._calculation is None:
            self._calculation = self.metric.metric.to_calculation()
        return self._calculation


class GroupBy(MetricContainer):
    def __init__(self, metric: Metric, column_name: str):
        self._column_name = column_name
        self._metric = metric

    def generate_metrics(self, context: Context) -> List[Metric]:
        labels = context.column(self._column_name).labels()
        return [GroupByMetric(metric=self._metric, column_name=self._column_name, label=label) for label in labels]

    def label_metric(self, label: object) -> Metric:
        return GroupByMetric(metric=self._metric, column_name=self._column_name, label=label)
