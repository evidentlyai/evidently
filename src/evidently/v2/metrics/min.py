from typing import List
from typing import Optional

from evidently.v2.checks.base import SingleValueCheck
from evidently.v2.datasets import Dataset
from evidently.v2.metrics.base import Metric
from evidently.v2.metrics.base import SingleValue


class MinMetric(Metric[SingleValue]):
    def __init__(self, column: str, checks: Optional[List[SingleValueCheck]] = None):
        super().__init__(f"min:{column}", checks if checks is not None else [])
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.min()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Minimal value of {self._column}"


def min_metric(column_name: str) -> MinMetric:
    return MinMetric(column_name)
