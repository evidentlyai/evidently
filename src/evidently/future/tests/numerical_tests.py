import abc
from typing import ClassVar
from typing import Optional
from typing import Union

from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricTest
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import Reference
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueTest
from evidently.future.metric_types import TestStatus
from evidently.future.metric_types import Value
from evidently.future.report import Context


class ComparisonTest(MetricTest):
    threshold: Union[float, int, Reference]
    __short_name__: ClassVar[str]
    __full_name__: ClassVar[str]
    __reference_relation__: ClassVar[str]

    @abc.abstractmethod
    def check(self, value: Value, threshold: Value) -> bool:
        raise NotImplementedError

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            threshold = self.get_threshold(context, metric.id)
            return MetricTestResult(
                self.__short_name__,
                f"{metric.display_name()}: {self.__full_name__} {self.threshold}",
                f"Actual value {value.value} {'<' if value.value < threshold else '>='} {threshold}",
                TestStatus.SUCCESS if self.check(value.value, threshold) else TestStatus.FAIL,
            )

        return func

    def get_threshold(self, context: Context, metric: MetricId) -> Union[float, int]:
        if isinstance(self.threshold, Reference):
            return self.apply_reference(self.threshold, context.get_reference_metric_result(metric).value)
        return self.threshold

    def apply_reference(self, reference: Reference, value: Value) -> Value:
        if reference.relative is not None:
            return value + (1 if self.__reference_relation__ == "less" else -1) * (reference.relative * value)
        if reference.absolute is not None:
            return value + (1 if self.__reference_relation__ == "less" else -1) * reference.absolute


class LessOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "le"
    __full_name__: ClassVar[str] = "Less or Equal"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value) -> bool:
        return value <= threshold


def lte(threshold: Union[int, float, Reference]) -> MetricTest:
    return LessOrEqualMetricTest(threshold=threshold)


class GreaterOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "ge"
    __full_name__: ClassVar[str] = "Greater or Equal"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value >= threshold


def gte(threshold: Union[int, float, Reference]) -> MetricTest:
    return GreaterOrEqualMetricTest(threshold=threshold)


class GreaterThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "gt"
    __full_name__: ClassVar[str] = "Greater"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value > threshold


def gt(threshold: Union[int, float, Reference]) -> MetricTest:
    return GreaterThanMetricTest(threshold=threshold)


class LessThanMetricTest(ComparisonTest):
    threshold: Union[int, float]
    __short_name__: ClassVar[str] = "lt"
    __full_name__: ClassVar[str] = "Less"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value):
        return value < threshold


def lt(threshold: Union[int, float, Reference]) -> MetricTest:
    return GreaterOrEqualMetricTest(threshold=threshold)


class EqualMetricTest(MetricTest):
    expected: Union[int, float, Reference]
    epsilon: Optional[float] = None

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            if isinstance(self.expected, Reference):
                expected = context.get_reference_metric_result(metric.id).value
                if self.expected.relative is not None:
                    eps = self.epsilon + abs(expected * self.expected.relative)
                elif self.expected.absolute is not None:
                    eps = self.epsilon + abs(self.expected.absolute)
                else:
                    eps = self.epsilon
            else:
                expected = self.expected
                eps = self.epsilon
            if eps is not None and (isinstance(expected, str) or isinstance(value.value, str)):
                raise ValueError("eq test cannot accept epsilon if value is string")
            if eps is None and isinstance(value.value, float):
                eps = 1e-5
            if eps is None:
                is_equal = value.value == expected
            else:
                is_equal = abs(value.value - self.expected) <= eps
            return MetricTestResult(
                "eq",
                f"{metric.display_name()}: Equal {self.expected}"
                + (f" with epsilon {self.epsilon}" if self.epsilon is not None else ""),
                f"Actual value {value.value} {f', but expected {expected}' if not is_equal else ''}",
                TestStatus.SUCCESS if is_equal else TestStatus.FAIL,
            )

        return func


def eq(expected: Union[int, float, str, Reference], epsilon: Optional[float] = None) -> MetricTest:
    return EqualMetricTest(expected=expected, epsilon=epsilon)
