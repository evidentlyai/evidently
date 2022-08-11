from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset

from evidently.tests import TestValueMeanError, TestValueMAE, TestValueRMSE, TestValueMAPE


class Regression(TestPreset):
    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestValueMeanError(),
            TestValueMAE(),
            TestValueRMSE(),
            TestValueMAPE(),
        ]
