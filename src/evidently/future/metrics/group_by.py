from typing import Callable
from typing import Optional
from typing import Sequence

from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
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


def _patched_display_name(original: Callable[[], str], metric: GroupByMetric) -> Callable[[], str]:
    def _wrapped():
        return f"{original()} group by '{metric.column_name}' for label: '{metric.label}'"

    return _wrapped


class GroupByMetricCalculation(MetricCalculation[TResult, GroupByMetric]):
    _calculation: Optional[MetricCalculation[TResult, GroupByMetric]] = None

    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        curr = current_data.subdataset(self.metric.column_name, self.metric.label)
        ref = reference_data.subdataset(self.metric.column_name, self.metric.label) if reference_data else None
        dn = self.calculation.display_name
        self.calculation.display_name = _patched_display_name(dn, self.metric)  # type: ignore[method-assign]
        res = self.calculation.calculate(context, curr, ref)
        if isinstance(res, tuple):
            curr_res, ref_res = res
        else:
            curr_res, ref_res = res, None
        curr_res.set_display_name(self.display_name())
        if ref_res is not None:
            ref_res.set_display_name(self.display_name())
        return curr_res, ref_res

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
        super().__init__(True)

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        labels = context.column(self._column_name).labels()
        return [GroupByMetric(metric=self._metric, column_name=self._column_name, label=label) for label in labels]

    def label_metric(self, label: object) -> Metric:
        return GroupByMetric(metric=self._metric, column_name=self._column_name, label=label)
