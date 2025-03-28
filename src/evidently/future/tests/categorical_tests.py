from typing import List
from typing import Union

from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricTest
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueTest
from evidently.future.report import Context
from evidently.tests.base_test import TestStatus


class IsInMetricTest(MetricTest):
    values: List[Union[int, str]]

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue) -> MetricTestResult:
            check_value = value.value in self.values
            return MetricTestResult(
                id="is_in",
                name=f"{metric.display_name()}: Value in list [{', '.join(str(x) for x in self.values)}]",
                description=f"Actual value: {value.value}",
                status=TestStatus.SUCCESS if check_value else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func


def is_in(values: List[Union[int, str]], is_critical: bool = True) -> MetricTest:
    return IsInMetricTest(values=values, is_critical=is_critical)


class NotInMetricTest(MetricTest):
    values: List[Union[int, str]]

    def to_test(self) -> SingleValueTest:
        def func(context: Context, metric: MetricCalculationBase, value: SingleValue) -> MetricTestResult:
            check_value = value.value not in self.values
            return MetricTestResult(
                id="not_in",
                name=f"{metric.display_name()}: Value not in list [{', '.join(str(x) for x in self.values)}]",
                description=f"Actual value: {value.value}",
                status=TestStatus.SUCCESS if check_value else TestStatus.FAIL,
                metric_config=metric.to_metric_config(),
                test_config=self.dict(),
            )

        return func


def not_in(values: List[Union[int, str]], is_critical: bool = True) -> MetricTest:
    return NotInMetricTest(values=values, is_critical=is_critical)
