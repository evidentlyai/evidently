from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueCheck


class ColumnMax(Metric[SingleValue]):
    class Config:
        type_alias = "evidently:metric_v2:ColumnMax"

    def __init__(self, column: str, checks: Optional[List[SingleValueCheck]] = None):
        super().__init__(f"max:{column}", checks)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.max()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Maximum value of {self._column}"


def column_max(column_name: str, checks: Optional[List[SingleValueCheck]] = None) -> ColumnMax:
    return ColumnMax(column_name, checks)
