from typing import Union

from ..metrics.base import CheckResult
from ..metrics.base import SingleValue
from ..metrics.base import SingleValueCheck
from ..metrics.base import TestStatus


def le(threshold: Union[int, float]) -> SingleValueCheck:
    def func(value: SingleValue):
        return CheckResult(
            f"Less or Equal {threshold}",
            "",
            TestStatus.SUCCESS if value.value <= threshold else TestStatus.FAIL,
        )

    return func


def ge(threshold: Union[int, float]) -> SingleValueCheck:
    def func(value: SingleValue):
        return CheckResult(
            f"Greater or Equal {threshold}",
            "",
            TestStatus.SUCCESS if value.value >= threshold else TestStatus.FAIL,
        )

    return func
