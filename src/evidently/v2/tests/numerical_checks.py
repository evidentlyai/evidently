from typing import Union

from ..metrics import Metric
from ..metrics.base import MetricTestResult
from ..metrics.base import SingleValue
from ..metrics.base import SingleValueMetricTest
from ..metrics.base import TestStatus


def le(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        return MetricTestResult(
            "le",
            f"{metric.display_name()}: Less or Equal {threshold}",
            f"Actual value {value.value} {'<' if value.value < threshold else '>='} {threshold}",
            TestStatus.SUCCESS if value.value <= threshold else TestStatus.FAIL,
        )

    return func


def ge(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        return MetricTestResult(
            "ge",
            f"{metric.display_name()}: Greater or Equal {threshold}",
            f"Actual value {value.value} {'<' if value.value < threshold else '>='} {threshold}",
            TestStatus.SUCCESS if value.value >= threshold else TestStatus.FAIL,
        )

    return func
