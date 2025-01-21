import abc
import typing
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.base_metric import InputData
from evidently.base_metric import Metric as LegacyMetric
from evidently.base_metric import MetricResult as LegacyMetricResult
from evidently.future.datasets import Dataset
from evidently.future.metric_types import MetricCalculation
from evidently.future.metric_types import TMetric
from evidently.future.metric_types import TMetricResult
from evidently.future.metric_types import TResult
from evidently.future.report import _default_input_data_generator
from evidently.model.widget import BaseWidgetInfo

if typing.TYPE_CHECKING:
    from evidently.future.report import Context

TLegacyResult = TypeVar("TLegacyResult", bound=LegacyMetricResult)
TLegacyMetric = TypeVar("TLegacyMetric", bound=LegacyMetric)
TLegacyMetricCalculation = TypeVar("TLegacyMetricCalculation", bound="LegacyMetricCalculation")


class LegacyMetricCalculation(
    MetricCalculation[TResult, TMetric],
    Generic[TResult, TMetric, TLegacyResult, TLegacyMetric],
    abc.ABC,
):
    @abc.abstractmethod
    def legacy_metric(self) -> TLegacyMetric:
        raise NotImplementedError()

    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]) -> TMetricResult:
        result, render = context.get_legacy_metric(self.legacy_metric(), self._gen_input_data)
        self.calculate_value(context, result, render)
        current, reference = self.calculate_value(context, result, render)
        add_cur, add_ref = self.get_additional_widgets(context)
        current.widget += add_cur
        if reference is not None:
            reference.widget += add_ref
        return current, reference

    def get_additional_widgets(self, context: "Context") -> typing.Tuple[List[BaseWidgetInfo], List[BaseWidgetInfo]]:
        return [], []

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: TLegacyResult,
        render: List[BaseWidgetInfo],
    ) -> TMetricResult:
        raise NotImplementedError()

    def _gen_input_data(self, context: "Context") -> InputData:
        default_input_data = _default_input_data_generator(context)
        return default_input_data
