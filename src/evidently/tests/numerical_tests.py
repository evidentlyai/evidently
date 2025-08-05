import abc
from typing import ClassVar
from typing import Union

from evidently.core.metric_types import DatasetType
from evidently.core.metric_types import MetricCalculationBase
from evidently.core.metric_types import MetricTest
from evidently.core.metric_types import MetricTestResult
from evidently.core.metric_types import MetricValueLocation
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueTest
from evidently.core.metric_types import TestStatus
from evidently.core.metric_types import Value
from evidently.core.report import Context
from evidently.core.tests import ApproxValue
from evidently.core.tests import Reference
from evidently.core.tests import ThresholdType
from evidently.core.tests import ThresholdValue


class ComparisonTest(MetricTest):
    threshold: ThresholdType
    __short_name__: ClassVar[str]
    __full_name__: ClassVar[str]
    __reference_relation__: ClassVar[str]

    @abc.abstractmethod
    def check(self, value: Value, threshold: ThresholdValue) -> bool:
        raise NotImplementedError

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            threshold = self.get_threshold(context, value.get_metric_value_location())
            title_threshold = f"{threshold:0.3f}"
            if isinstance(self.threshold, Reference):
                if isinstance(threshold, ApproxValue):
                    title_threshold += f"Reference {threshold:0.3f} ± {threshold.tolerance:0.3f}"
                else:
                    title_threshold = f"Reference {threshold:0.3f}"
            return MetricTestResult(
                id=self.__short_name__,
                name=f"{value.display_name}: {self.__full_name__} {title_threshold}",
                description=f"Actual value {value.value:0.3f} {'<' if value.value < threshold else '>='} {threshold:0.3f}",
                status=TestStatus.SUCCESS if self.check(value.value, threshold) else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
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

    def check(self, value: Value, threshold: ThresholdValue) -> bool:
        return value <= threshold


class GreaterOrEqualMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "ge"
    __full_name__: ClassVar[str] = "Greater or Equal"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: ThresholdValue):
        return value >= threshold


class GreaterThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "gt"
    __full_name__: ClassVar[str] = "Greater"
    __reference_relation__: ClassVar[str] = "greater"

    def check(self, value: Value, threshold: ThresholdValue):
        return value > threshold


class LessThanMetricTest(ComparisonTest):
    __short_name__: ClassVar[str] = "lt"
    __full_name__: ClassVar[str] = "Less"
    __reference_relation__ = "less"

    def check(self, value: Value, threshold: ThresholdValue):
        return value < threshold


class EqualMetricTestBase(MetricTest, abc.ABC):
    expected: ThresholdType

    def is_equal(self, context: Context, value: SingleValue):
        expected: Union[float, int, ApproxValue]
        if isinstance(self.expected, Reference):
            result = value.get_metric_value_location().value(context, DatasetType.Reference)
            expected = ApproxValue(result.value, self.expected.relative, self.expected.absolute)
        else:
            expected = self.expected
        title_expected = f"{expected:0.3f}"
        return expected, title_expected, expected == value.value


class EqualMetricTest(EqualMetricTestBase):
    expected: ThresholdType

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, title_expected, is_equal = self.is_equal(context, value)
            return MetricTestResult(
                id="eq",
                name=f"{metric.display_name()}: Equal {title_expected}",
                description=f"Actual value {value.value:0.3f}"
                f" {f', but expected {expected:0.3f}' if not is_equal else f' expected {expected:0.3f}'}",
                status=TestStatus.SUCCESS if is_equal else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func


class NotEqualMetricTest(EqualMetricTestBase):
    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue):
            expected, title_expected, is_equal = self.is_equal(context, value)
            return MetricTestResult(
                id="not_eq",
                name=f"{metric.display_name()}: Not equal {title_expected}",
                description=f"Actual value {value.value}"
                f" {f', but expected not {expected:0.3f}' if is_equal else f' not equal to {expected:0.3f}'}",
                status=TestStatus.SUCCESS if not is_equal else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func
