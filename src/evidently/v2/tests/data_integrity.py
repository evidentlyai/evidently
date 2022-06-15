from evidently.v2.metrics.base_metric import NumberRange

from .base_test import Test, TestResult

class TestNumberOfColumns(Test):
    def __init__(self, range: NumberRange):
        self.range = range.get_range()


    def check(self, metrics: dict, tests: dict):
        results = DataIntegerityMetrics.get_results(metrics)
        passed = True if self.range[0] is None else results.
        return TestResult("test_numder_of_columns",
                          "",
                          "SUCCESS")