from typing import List
from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics import SingleValue
from evidently.future.metrics import SingleValueMetricTest
from evidently.future.metrics.base import SingleValueCalculation


class RowCount(SingleValueCalculation):
    def __init__(self, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__("row_count")
        self.with_tests(tests)

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().row_count)

    def display_name(self) -> str:
        return "Row count in dataset"


class ColumnCount(SingleValueCalculation):
    def __init__(self, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__("column_count")
        self.with_tests(tests)

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        return SingleValue(current_data.stats().column_count)

    def display_name(self) -> str:
        return "Column count in dataset"
