from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueCheck


class ColumnMin(Metric[SingleValue]):
    column: str

    def __init__(self, column: str, checks: Optional[List[SingleValueCheck]] = None):
        self.column = column
        super().__init__(f"min:{column}", checks)

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self.column)
        value = data.data.min()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Minimal value of {self.column}"


def column_min(column_name: str, checks: Optional[List[SingleValueCheck]] = None) -> ColumnMin:
    return ColumnMin(column_name, checks)
