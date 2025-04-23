from typing import Any
from typing import Set

from evidently.core.datasets import ColumnCondition
from evidently.tests.numerical_tests import ThresholdType


class EqualsColumnCondition(ColumnCondition):
    expected: Any

    def check(self, value: Any) -> bool:
        return self.expected == value

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_equals_{self.expected}"


class NotEqualsColumnCondition(ColumnCondition):
    expected: Any

    def check(self, value: Any) -> bool:
        return self.expected != value

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_not_equals_{self.expected}"


class LessColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value < self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_less_{self.threshold}"


class LessEqualColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value <= self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_less_or_equal_{self.threshold}"


class GreaterColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value > self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_greater_{self.threshold}"


class GreaterEqualColumnCondition(ColumnCondition):
    threshold: ThresholdType

    def check(self, value: Any) -> bool:
        return value >= self.threshold

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_greater_or_equal_{self.threshold}"


class IsInColumnCondition(ColumnCondition):
    values: Set[Any]

    def check(self, value: Any) -> bool:
        return value in self.values

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_in_{self.values}"


class IsNotInColumnCondition(ColumnCondition):
    values: Set[Any]

    def check(self, value: Any) -> bool:
        return value not in self.values

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_not_in_{self.values}"
