import abc
import typing
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metrics import Metric
from evidently.future.metrics.base import MetricId
from evidently.future.metrics.base import TResult
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context

TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)


class LegacyBasedMetric(Metric[TResult], Generic[TResult, TLegacyResult], abc.ABC):
    def __init__(self, metric_id: MetricId, metric: LegacyMetric[TLegacyResult]):
        super().__init__(metric_id)
        self._metric = metric

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    def _call(self, context: "Context") -> TResult:
        result, render = context.get_legacy_metric(self._metric)
        return self.calculate_value(context, result, render)

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: TLegacyResult,
        render: List[BaseWidgetInfo],
    ) -> TResult:
        raise NotImplementedError()
