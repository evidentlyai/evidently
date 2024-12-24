from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueMetricTest


class ColumnMin(Metric[SingleValue]):
    def __init__(self, column: str):
        super().__init__(f"min:{column}")
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.min()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Minimal value of {self._column}"


def column_min(column_name: str, tests: Optional[List[SingleValueMetricTest]] = None) -> ColumnMin:
    return ColumnMin(column_name).with_tests(tests)


class ColumnMean(Metric[SingleValue]):
    def __init__(self, column: str):
        super().__init__(f"mean:{column}")
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        value = current_data.column(self._column).data.mean()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Mean value of '{self._column}'"


def column_mean(column: str, tests: Optional[List[SingleValueMetricTest]] = None):
    return ColumnMean(column).with_tests(tests)


class ColumnMax(Metric[SingleValue]):
    def __init__(self, column: str):
        super().__init__(f"max:{column}")
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.max()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Maximum value of {self._column}"


def column_max(column_name: str, tests: Optional[List[SingleValueMetricTest]] = None) -> ColumnMax:
    return ColumnMax(column_name).with_tests(tests)
