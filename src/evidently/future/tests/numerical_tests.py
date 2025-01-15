import abc
from typing import ClassVar
from typing import Optional
from typing import Union

from evidently.future.metric_types import DatasetType
from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricTest
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import MetricValueLocation
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
            threshold = self.get_threshold(context, value.metric_value_location)
            return MetricTestResult(
                self.__short_name__,
                f"{metric.display_name()}: {self.__full_name__} {self.threshold}",
                f"Actual value {value.value} {'<' if value.value < threshold else '>='} {threshold}",
                TestStatus.SUCCESS if self.check(value.value, threshold) else TestStatus.FAIL,
            )

        return func

    def get_threshold(self, context: Context, metric_location: MetricValueLocation) -> Union[float, int]:
        if isinstance(self.threshold, Reference):
            if context._input_data[1] is None:
                raise ValueError("No Reference dataset provided, but tests contains Reference thresholds")
            value = metric_location.value(context, DatasetType.Reference).value
            return self.apply_reference(self.threshold, value)
        return self.threshold

    def apply_reference(self, reference: Reference, value: Value) -> Value:
        if reference.relative is not None:
            return value + (1 if self.__reference_relation__ == "less" else -1) * (reference.relative * value)
        if reference.absolute is not None:
            return value + (1 if self.__reference_relation__ == "less" else -1) * reference.absolute
        return value


class LessOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "le"
    __full_name__: ClassVar[str] = "Less or Equal"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value) -> bool:
        return value <= threshold


def lte(threshold: Union[int, float, Reference], is_critical: bool = True) -> MetricTest:
    return LessOrEqualMetricTest(threshold=threshold, is_critical=is_critical)


class GreaterOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "ge"
    __full_name__: ClassVar[str] = "Greater or Equal"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value >= threshold


def gte(threshold: Union[int, float, Reference], is_critical: bool = True) -> MetricTest:
    return GreaterOrEqualMetricTest(threshold=threshold, is_critical=is_critical)


class GreaterThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "gt"
    __full_name__: ClassVar[str] = "Greater"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value > threshold


def gt(threshold: Union[int, float, Reference], is_critical: bool = True) -> MetricTest:
    return GreaterThanMetricTest(threshold=threshold, is_critical=is_critical)


class LessThanMetricTest(ComparisonTest):
    threshold: Union[int, float]
    __short_name__: ClassVar[str] = "lt"
    __full_name__: ClassVar[str] = "Less"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value):
        return value < threshold


def lt(threshold: Union[int, float, Reference], is_critical: bool = True) -> MetricTest:
    return GreaterOrEqualMetricTest(threshold=threshold, is_critical=is_critical)


class EqualMetricTestBase(MetricTest, abc.ABC):
    expected: Union[int, float, Reference]
    epsilon: Optional[float] = None

    def is_equal(self, context: Context, metric: MetricCalculationBase, value: SingleValue):
        if self.epsilon is None:
            eps = 1e-5
        else:
            eps = self.epsilon
        if isinstance(self.expected, Reference):
            result = context.get_reference_metric_result(metric.to_metric())
            assert isinstance(result, SingleValue)
            expected = result.value
            if self.expected.relative is not None:
                eps = eps + abs(expected * self.expected.relative)
            elif self.expected.absolute is not None:
                eps = eps + abs(self.expected.absolute)
        else:
            expected = self.expected
        if eps is not None and (isinstance(expected, str) or isinstance(value.value, str)):
            raise ValueError("eq test cannot accept epsilon if value is string")
        if eps is None and isinstance(value.value, float):
            eps = 1e-5
        if eps is None:
            return value.value == expected
        return expected, abs(value.value - self.expected) <= eps


class EqualMetricTest(EqualMetricTestBase):
    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, is_equal = self.is_equal(context, metric, value)
            return MetricTestResult(
                "eq",
                f"{metric.display_name()}: Equal {self.expected}"
                + (f" with epsilon {self.epsilon}" if self.epsilon is not None else ""),
                f"Actual value {value.value} {f', but expected {expected}' if not is_equal else ''}",
                TestStatus.SUCCESS if is_equal else TestStatus.FAIL,
            )

        return func


def eq(
    expected: Union[int, float, str, Reference], epsilon: Optional[float] = None, is_critical: bool = True
) -> MetricTest:
    return EqualMetricTest(expected=expected, epsilon=epsilon, is_critical=is_critical)


class NotEqualMetricTest(EqualMetricTestBase):
    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, is_equal = self.is_equal(context, metric, value)
            return MetricTestResult(
                "not_eq",
                f"{metric.display_name()}: Not equal {self.expected}"
                + (f" with epsilon {self.epsilon}" if self.epsilon is not None else ""),
                f"Actual value {value.value} {f', but expected not {expected}' if is_equal else ''}",
                TestStatus.SUCCESS if not is_equal else TestStatus.FAIL,
            )

        return func


def not_eq(
    expected: Union[int, float, str, Reference], epsilon: Optional[float] = None, is_critical: bool = True
) -> MetricTest:
    return NotEqualMetricTest(expected=expected, epsilon=epsilon, is_critical=is_critical)
