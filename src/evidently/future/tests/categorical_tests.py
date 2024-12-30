from typing import List
from typing import Union

from evidently.future.metrics import Metric
from evidently.future.metrics import SingleValue
from evidently.future.metrics import SingleValueMetricTest
from evidently.future.metrics.base import MetricTestResult
from evidently.tests.base_test import TestStatus


def is_in(values: List[Union[int, str]]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue) -> MetricTestResult:
        check_value = value.value in values
        return MetricTestResult(
            "is_in",
            f"{metric.display_name()}: Value in list [{', '.join(values)}]",
            f"Actual value: {value.value}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func


def not_in(values: List[Union[int, str]]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue) -> MetricTestResult:
        check_value = value.value not in values
        return MetricTestResult(
            "not_in",
            f"{metric.display_name()}: Value not in list [{', '.join(values)}]",
            f"Actual value: {value.value}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func
