import abc
from typing import ClassVar
from typing import Union

from ..metrics import MetricCalculationBase
from ..metrics.base import MetricTest
from ..metrics.base import MetricTestResult
from ..metrics.base import SingleValue
from ..metrics.base import SingleValueTest
from ..metrics.base import TestStatus
from ..metrics.base import Value


class ComparisonTest(MetricTest[SingleValueTest]):
    threshold: Union[int, float]
    __short_name__: ClassVar[str]
    __full_name__: ClassVar[str]

    @abc.abstractmethod
    def check(self, value: Value) -> bool:
        raise NotImplementedError

    def to_test(self) -> SingleValueTest:
        def func(metric: MetricCalculationBase, value: SingleValue):
            return MetricTestResult(
                self.__short_name__,
                f"{metric.display_name()}: {self.__full_name__} {self.threshold}",
                f"Actual value {value.value} {'<' if value.value < self.threshold else '>='} {self.threshold}",
                TestStatus.SUCCESS if self.check(value.value) else TestStatus.FAIL,
            )

        return func


class LessOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "le"
    __full_name__: ClassVar[str] = "Less or Equal"

    def check(self, value: Value):
        return value <= self.threshold


def le(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return LessOrEqualMetricTest(threshold=threshold)


class GreaterOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "ge"
    __full_name__: ClassVar[str] = "Greater or Equal"

    def check(self, value: Value):
        return value >= self.threshold


def ge(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return GreaterOrEqualMetricTest(threshold=threshold)


class GreaterThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "gt"
    __full_name__: ClassVar[str] = "Greater"

    def check(self, value: Value):
        return value > self.threshold


def gt(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return GreaterThanMetricTest(threshold=threshold)


class LessThanMetricTest(ComparisonTest):
    threshold: Union[int, float]
    __short_name__: ClassVar[str] = "lt"
    __full_name__: ClassVar[str] = "Less"

    def check(self, value: Value):
        return value < self.threshold


def lt(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return GreaterOrEqualMetricTest(threshold=threshold)


class EqualMetricTest(ComparisonTest):
    threshold: Union[int, float]
    __short_name__: ClassVar[str] = "eq"
    __full_name__: ClassVar[str] = "Equal"

    def check(self, value: Value):
        return value == self.threshold


def eq(threshold: Union[int, float]) -> MetricTest[SingleValueTest]:
    return GreaterOrEqualMetricTest(threshold=threshold)
