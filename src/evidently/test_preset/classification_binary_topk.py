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
    """
    Binary Classification Tests for Top K threshold.
    Args:
        stattest: stattest for `TestColumnDrift`
        stattest_threshold: threshold for stattest

    Contains:
    - `TestColumnDrift` for target
    - `TestPrecisionScore`
    - `TestRecallScore`
    - `TestF1Score`
    - `TestAccuracyScore`
    """

    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        k: Union[float, int],
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        super().__init__()
        self.k = k
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        return [
            TestAccuracyScore(k=self.k),
            TestPrecisionScore(k=self.k),
            TestRecallScore(k=self.k),
            TestF1Score(k=self.k),
            TestColumnDrift(column_name=target, stattest=self.stattest, stattest_threshold=self.stattest_threshold),
            TestRocAuc(),
            TestLogLoss(),
        ]
