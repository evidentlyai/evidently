from typing import Optional
from typing import Union

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore
from evidently.tests import TestColumnDrift
from evidently.tests import TestF1Score
from evidently.tests import TestLogLoss
from evidently.tests import TestPrecisionScore
from evidently.tests import TestRecallScore
from evidently.tests import TestRocAuc
from evidently.utils.data_operations import DatasetColumns


class BinaryClassificationTopKTestPreset(TestPreset):
    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        k: Union[float, int],
        probas_threshold: Optional[float] = None,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        super().__init__()
        self.k = k
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold
        self.probas_threshold = probas_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        return [
            TestAccuracyScore(probas_threshold=self.probas_threshold, k=self.k),
            TestPrecisionScore(probas_threshold=self.probas_threshold, k=self.k),
            TestRecallScore(probas_threshold=self.probas_threshold, k=self.k),
            TestF1Score(probas_threshold=self.probas_threshold, k=self.k),
            TestColumnDrift(
                column_name=target, stattest=self.stattest, stattest_threshold=self.stattest_threshold
            ),
            TestRocAuc(),
            TestLogLoss(),
        ]
