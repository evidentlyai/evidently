from typing import Union

from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestF1Score
from evidently.tests import TestLogLoss
from evidently.tests import TestPrecisionScore
from evidently.tests import TestRecallScore
from evidently.tests import TestRocAuc
from evidently.utils.data_operations import DatasetColumns


class BinaryClassificationTopKTestPreset(TestPreset):
    def __init__(self, k: Union[float, int]):
        super().__init__()
        self.k = k

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        return [
            TestAccuracyScore(k=self.k),
            TestPrecisionScore(k=self.k),
            TestRecallScore(k=self.k),
            TestF1Score(k=self.k),
            TestColumnValueDrift(column_name=target),
            TestRocAuc(),
            TestLogLoss(),
        ]
