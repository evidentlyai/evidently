from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueCheck


class ColumnMean(Metric[SingleValue]):
    _column: str

    def __init__(self, column: str, checks: Optional[List[SingleValueCheck]] = None):
        super().__init__(f"mean:{column}", checks)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        value = current_data.column(self._column).data.mean()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Mean value of '{self._column}'"


def column_mean(column: str, checks: Optional[List[SingleValueCheck]] = None):
    return ColumnMean(column, checks)
