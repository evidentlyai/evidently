from typing import Optional

from evidently.v2.metrics.base_metric import NumberRange
from evidently.v2.metrics.data_integrity import DataIntegrityMetrics

from .base_test import Test, TestResult


class TestNumberOfColumns(Test):
    data_integrity: DataIntegrityMetrics

    def __init__(self,
                 count_range: NumberRange,
                 data_integrity_metric: Optional[DataIntegrityMetrics] = None):
        self.range = count_range.get_range()
        if data_integrity_metric is None:
            self.data_integrity = DataIntegrityMetrics()
        else:
            self.data_integrity = data_integrity_metric

    def check(self):
        results = self.data_integrity.get_result()
        passed = (True if self.range[0] is None else results.number_of_columns >= self.range[0]) and \
                 (True if self.range[1] is None else results.number_of_columns <= self.range[1])
        return TestResult("Test Number of Columns",
                          self._description(passed, number_of_columns=results.number_of_columns),
                          "SUCCESS" if passed else "FAIL")

    def _description(self, passed: bool, number_of_columns: int):
        if passed:
            return f"Number of columns ({number_of_columns}) is in range [{self.range[0], self.range[1]}]"
        return f"Number of columns ({number_of_columns}) is not in range [{self.range[0], self.range[1]}]"
