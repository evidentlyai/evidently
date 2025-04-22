from typing import Any

from evidently.core.datasets import DescriptorCondition


class EqualsDescriptorCondition(DescriptorCondition):
    expected: Any

    def check(self, value: Any) -> bool:
        return self.expected == value

    def get_default_alias(self, column: str) -> str:
        return f"{column}_test_equals_{self.expected}"
