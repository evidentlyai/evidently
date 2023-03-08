from evidently.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import (
    TestValueMAE,
    TestValueMAPE,
    TestValueMeanError,
    TestValueRMSE,
)
from evidently.utils.data_operations import DatasetColumns


class RegressionTestPreset(TestPreset):
    """
    Regression performance tests.

    Contains tests:
    - `TestValueMeanError`
    - `TestValueMAE`
    - `TestValueRMSE`
    - `TestValueMAPE`
    """

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestValueMeanError(),
            TestValueMAE(),
            TestValueRMSE(),
            TestValueMAPE(),
        ]
