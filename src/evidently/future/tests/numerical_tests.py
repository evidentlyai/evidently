from typing import Union

from ..metrics import MetricCalculationBase
from ..metrics.base import MetricTest
from ..metrics.base import MetricTestResult
from ..metrics.base import SingleValue
from ..metrics.base import SingleValueTest
from ..metrics.base import TestStatus


class LessOrEqualMetricTest(MetricTest[SingleValueTest]):
    threshold: Union[int, float]

    def to_test(self) -> SingleValueTest:
        def func(metric: MetricCalculationBase, value: SingleValue):
            return MetricTestResult(
                "le",
                f"{metric.display_name()}: Less or Equal {self.threshold}",
                f"Actual value {value.value} {'<' if value.value < self.threshold else '>='} {self.threshold}",
                TestStatus.SUCCESS if value.value <= self.threshold else TestStatus.FAIL,
            )

        return func


def le(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return LessOrEqualMetricTest(threshold=threshold)


class GreaterOrEqualMetricTest(MetricTest[SingleValueTest]):
    threshold: Union[int, float]

    def to_test(self) -> SingleValueTest:
        def func(metric: MetricCalculationBase, value: SingleValue):
            return MetricTestResult(
                "ge",
                f"{metric.display_name()}: Greater or Equal {self.threshold}",
                f"Actual value {value.value} {'<' if value.value < self.threshold else '>='} {self.threshold}",
                TestStatus.SUCCESS if value.value >= self.threshold else TestStatus.FAIL,
            )

        return func


def ge(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return GreaterOrEqualMetricTest(threshold=threshold)
