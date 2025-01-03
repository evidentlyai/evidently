import abc
import typing
from typing import Generator
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently._pydantic_compat import PrivateAttr
from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metrics.base import Metric
from evidently.future.metrics.base import MetricCalculation
from evidently.future.metrics.base import MetricTestResult
from evidently.future.metrics.base import TResult
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context

TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)
TLegacyMetric = TypeVar("TLegacyMetric", bound=LegacyMetric)
TLegacyMetricCalculation = TypeVar("TLegacyMetricCalculation", bound="LegacyMetricCalculation")


class LegacyBasedMetric(
    Metric[TLegacyMetricCalculation], Generic[TLegacyMetricCalculation, TLegacyMetric, TLegacyResult], abc.ABC
):
    _metric: Optional[TLegacyMetric] = PrivateAttr(None)

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        return
        yield

    def _get_legacy_metric(self) -> TLegacyMetric:
        raise NotImplementedError

    def get_legacy_metric(self) -> TLegacyMetric:
        if self._metric is None:
            self._metric = self._get_legacy_metric()
        return self._metric


TLegacyBasedMetric = TypeVar("TLegacyBasedMetric", bound=LegacyBasedMetric)


class LegacyMetricCalculation(
    MetricCalculation[TResult, TLegacyBasedMetric],
    Generic[TResult, TLegacyMetric, TLegacyResult, TLegacyBasedMetric],
    abc.ABC,
):
    @property
    def legacy_metric(self) -> TLegacyMetric:
        return self.metric.get_legacy_metric()

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise NotImplementedError()

    def _call(self, context: "Context") -> TResult:
        result, render = context.get_legacy_metric(self.legacy_metric)
        return self.calculate_value(context, result, render)

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: TLegacyResult,
        render: List[BaseWidgetInfo],
    ) -> TResult:
        raise NotImplementedError()
