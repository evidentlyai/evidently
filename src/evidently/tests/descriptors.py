from typing import Any
from typing import Set

from evidently.core.datasets import ColumnCondition
from evidently.tests.numerical_tests import ThresholdType


class EqualsColumnCondition(ColumnCondition):
    expected: Any

    def check(self, value: Any) -> bool:
        try:
            expected = type(value)(self.expected)
            return expected == value
        except (ValueError, TypeError):
            return False

    def get_default_alias(self, column: str) -> str:
        return f"{column}: equals {self.expected}"


class NotEqualsColumnCondition(ColumnCondition):
    expected: Any

    def check(self, value: Any) -> bool:
        try:
            expected = type(value)(self.expected)
            return expected != value
        except (ValueError, TypeError):
            return True

    def get_default_alias(self, column: str) -> str:
        return f"{column} not equals {self.expected}"


class LessColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value < self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}: less than {self.threshold}"


class LessEqualColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value <= self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}: less or equal to {self.threshold}"


class GreaterColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value > self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column} greater than {self.threshold}"


class GreaterEqualColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value >= self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}: greater or equal to {self.threshold}"


def _typed_values(cls, values):
    res = set()
    for value in values:
        try:
            res.add(cls(value))
        except ValueError:
            pass
    return res


class IsInColumnCondition(ColumnCondition):
    values: Set[Any]

    def check(self, value: Any) -> bool:
        return value in self.values or value in _typed_values(type(value), self.values)

    def get_default_alias(self, column: str) -> str:
        return f"{column} in list {self.values}"


class IsNotInColumnCondition(ColumnCondition):
    values: Set[Any]

    def check(self, value: Any) -> bool:
        return value not in self.values and value not in _typed_values(type(value), self.values)

    def get_default_alias(self, column: str) -> str:
        return f"{column} not in list {self.values}"
