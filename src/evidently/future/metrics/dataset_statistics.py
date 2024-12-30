from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics import SingleValue
from evidently.future.metrics.base import SingleValueCalculation
from evidently.future.metrics.base import SingleValueMetric


class RowCount(SingleValueMetric):
    pass


class RowCountCalculation(SingleValueCalculation[RowCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().row_count)

    def display_name(self) -> str:
        return "Row count in dataset"


class ColumnCount(SingleValueMetric):
    pass


class ColumnCountCalculation(SingleValueCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().column_count)

    def display_name(self) -> str:
        return "Column count in dataset"
