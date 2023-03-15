from evidently.base_metric import InputData
from evidently.metric_results import DatasetColumns
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestValueMAE
from evidently.tests import TestValueMAPE
from evidently.tests import TestValueMeanError
from evidently.tests import TestValueRMSE


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
