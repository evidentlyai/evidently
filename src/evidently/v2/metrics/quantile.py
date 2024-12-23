from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueCheck


class ColumnQuantile(Metric[SingleValue]):
    class Config:
        type_alias = "evidently:metric_v2:ColumnQuantile"

    def __init__(self, column: str, quantile: float, checks: Optional[List[SingleValueCheck]] = None):
        super().__init__(f"quantile:{quantile}:{column}", checks)
        self._quantile = quantile
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.quantile(self._quantile)
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Quantile {self._quantile} of {self._column}"


def column_quantile(
    column_name: str, quantile: float, checks: Optional[List[SingleValueCheck]] = None
) -> ColumnQuantile:
    return ColumnQuantile(column_name, quantile, checks)
