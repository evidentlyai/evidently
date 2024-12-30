from typing import Optional
from typing import Union

from ..metrics import Metric
from ..metrics.base import MetricTestResult
from ..metrics.base import SingleValue
from ..metrics.base import SingleValueMetricTest
from ..metrics.base import TestStatus


def lte(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        check_value = value.value <= threshold
        return MetricTestResult(
            "lte",
            f"{metric.display_name()}: Less or Equal {threshold}",
            f"Actual value {value.value} {'<=' if check_value else '>'} {threshold}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func


def lt(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        check_value = value.value < threshold
        return MetricTestResult(
            "lt",
            f"{metric.display_name()}: Less {threshold}",
            f"Actual value {value.value} {'<' if check_value else '>='} {threshold}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func


def gte(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        check_value = value.value >= threshold
        return MetricTestResult(
            "gte",
            f"{metric.display_name()}: Greater or Equal {threshold}",
            f"Actual value {value.value} {'>=' if check_value else '<'} {threshold}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func


def gt(threshold: Union[int, float]) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        check_value = value.value > threshold
        return MetricTestResult(
            "gt",
            f"{metric.display_name()}: Greater {threshold}",
            f"Actual value {value.value} {'>' if check_value else '<='} {threshold}",
            TestStatus.SUCCESS if check_value else TestStatus.FAIL,
        )

    return func


def eq(expected: Union[int, float, str], epsilon: Optional[float] = None) -> SingleValueMetricTest:
    def func(metric: Metric, value: SingleValue):
        eps = epsilon
        if eps is not None and (isinstance(expected, str) or isinstance(value.value, str)):
            raise ValueError("eq test cannot accept epsilon if value is string")
        if eps is None and isinstance(value.value, float):
            eps = 1e-5
        if eps is None:
            is_equal = value.value == expected
        else:
            is_equal = abs(value.value - expected) <= eps
        return MetricTestResult(
            "eq",
            f"{metric.display_name()}: Equal {expected}" + (f" with epsilon {eps}" if eps is not None else ""),
            f"Actual value {value.value} {f', but expected {expected}' if not is_equal else ''}",
            TestStatus.SUCCESS if is_equal else TestStatus.FAIL,
        )

    return func
