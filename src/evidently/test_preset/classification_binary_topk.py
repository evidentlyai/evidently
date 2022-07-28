from typing import Union

from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore, TestF1Score, TestPrecisionScore, TestRecallScore, \
    TestFeatureValueDrift, TestRocAuc, TestLogLoss


class BinaryClassificationTopK(TestPreset):
    def __init__(self, k: Union[float, int]):
        super().__init__()
        self.k = k

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        return [
            TestAccuracyScore(k=self.k),
            TestPrecisionScore(k=self.k),
            TestRecallScore(k=self.k),
            TestF1Score(k=self.k),
            TestFeatureValueDrift(column_name=columns.utility_columns.target),
            TestRocAuc(),
            TestLogLoss()
        ]
