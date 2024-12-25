from typing import List
from typing import Optional

from evidently.v2.datasets import Dataset
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueMetricTest
from evidently.v2.metrics.base import SingleValueMetric


class MinValue(SingleValueMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"min:{column}")
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.min()
        result = SingleValue(value)
        return result

    def display_name(self) -> str:
        return f"Minimal value of {self._column}"


class MeanValue(SingleValueMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"mean:{column}")
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        value = current_data.column(self._column).data.mean()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Mean value of {self._column}"


class MaxValue(SingleValueMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"max:{column}")
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.max()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Maximum value of {self._column}"


class StdValue(SingleValueMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"std:{column}")
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.std()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Std value of {self._column}"


class MedianValue(SingleValueMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"median:{column}")
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.median()
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Median value of {self._column}"


class QuantileValue(SingleValueMetric):
    def __init__(self, column: str, quantile: float = 0.5, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"quantile:{quantile}:{column}")
        self.with_tests(tests)
        self._quantile = quantile
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        data = current_data.column(self._column)
        value = data.data.quantile(self._quantile)
        return SingleValue(value)

    def display_name(self) -> str:
        return f"Quantile {self._quantile} of {self._column}"
