import abc
from typing import ClassVar
from typing import Union

from evidently.future.metric_types import DatasetType
from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricTest
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import MetricValueLocation
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueTest
from evidently.future.metric_types import TestStatus
from evidently.future.metric_types import Value
from evidently.future.report import Context
from evidently.future.tests.reference import Reference
from evidently.utils.types import ApproxValue

ThresholdType = Union[float, int, ApproxValue, Reference]


class ComparisonTest(MetricTest):
    threshold: ThresholdType
    __short_name__: ClassVar[str]
    __full_name__: ClassVar[str]
    __reference_relation__: ClassVar[str]

    @abc.abstractmethod
    def check(self, value: Value, threshold: Value) -> bool:
        raise NotImplementedError

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            threshold = self.get_threshold(context, value.metric_value_location)
            title_threshold = f"{threshold:0.2f}"
            if isinstance(self.threshold, Reference):
                title_threshold = "Reference"
                if isinstance(threshold, ApproxValue):
                    title_threshold += f" ± {threshold.tolerance}"
            return MetricTestResult(
                self.__short_name__,
                f"{value.display_name()}: {self.__full_name__} {title_threshold}",
                f"Actual value {value.value} {'<' if value.value < threshold else '>='} {threshold}",
                TestStatus.SUCCESS if self.check(value.value, threshold) else TestStatus.FAIL,
            )

        return func

    def get_threshold(self, context: Context, metric_location: MetricValueLocation) -> Union[float, int, ApproxValue]:
        if isinstance(self.threshold, Reference):
            if context._input_data[1] is None:
                raise ValueError("No Reference dataset provided, but tests contains Reference thresholds")
            value = metric_location.value(context, DatasetType.Reference).value
            return ApproxValue(value, self.threshold.relative, self.threshold.absolute)
        return self.threshold


class LessOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "le"
    __full_name__: ClassVar[str] = "Less or Equal"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value) -> bool:
        return value <= threshold


def lte(threshold: ThresholdType, is_critical: bool = True) -> MetricTest:
    return LessOrEqualMetricTest(threshold=threshold, is_critical=is_critical)


class GreaterOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "ge"
    __full_name__: ClassVar[str] = "Greater or Equal"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value >= threshold


def gte(threshold: ThresholdType, is_critical: bool = True) -> MetricTest:
    return GreaterOrEqualMetricTest(threshold=threshold, is_critical=is_critical)


class GreaterThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "gt"
    __full_name__: ClassVar[str] = "Greater"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: Value):
        return value > threshold


def gt(threshold: ThresholdType, is_critical: bool = True) -> MetricTest:
    return GreaterThanMetricTest(threshold=threshold, is_critical=is_critical)


class LessThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "lt"
    __full_name__: ClassVar[str] = "Less"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: Value):
        return value < threshold


def lt(threshold: ThresholdType, is_critical: bool = True) -> MetricTest:
    return LessThanMetricTest(threshold=threshold, is_critical=is_critical)


class EqualMetricTestBase(MetricTest, abc.ABC):
    expected: ThresholdType

    def is_equal(self, context: Context, value: SingleValue):
        expected: Union[float, int, ApproxValue]
        if isinstance(self.expected, Reference):
            result = value.metric_value_location.value(context, DatasetType.Reference)
            expected = ApproxValue(result.value, self.expected.relative, self.expected.absolute)
        else:
            expected = self.expected
        title_expected = f"{expected:0.2f}"
        if isinstance(self.expected, Reference):
            title_expected = "Reference"
            if isinstance(expected, ApproxValue):
                title_expected += f" ± {expected.tolerance}"
        return expected, title_expected, expected == value.value


class EqualMetricTest(EqualMetricTestBase):
    expected: ThresholdType

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, title_expected, is_equal = self.is_equal(context, value)
            return MetricTestResult(
                "eq",
                f"{metric.display_name()}: Equal {title_expected}",
                f"Actual value {value.value} {f', but expected {expected}' if not is_equal else ''}",
                TestStatus.SUCCESS if is_equal else TestStatus.FAIL,
            )

        return func


def eq(expected: ThresholdType, is_critical: bool = True) -> MetricTest:
    return EqualMetricTest(expected=expected, is_critical=is_critical)


class NotEqualMetricTest(EqualMetricTestBase):
    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, title_expected, is_equal = self.is_equal(context, value)
            return MetricTestResult(
                "not_eq",
                f"{metric.display_name()}: Not equal {title_expected}",
                f"Actual value {value.value} {f', but expected not {expected}' if is_equal else ''}",
                TestStatus.SUCCESS if not is_equal else TestStatus.FAIL,
            )

        return func


def not_eq(expected: ThresholdType, is_critical: bool = True) -> MetricTest:
    return NotEqualMetricTest(expected=expected, is_critical=is_critical)
