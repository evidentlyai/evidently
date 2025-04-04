from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.calculations.stattests import PossibleStatTestType
from evidently.legacy.test_preset.test_preset import AnyTest
from evidently.legacy.test_preset.test_preset import TestPreset
from evidently.legacy.tests import TestAccuracyScore
from evidently.legacy.tests import TestColumnDrift
from evidently.legacy.tests import TestF1Score
from evidently.legacy.tests import TestLogLoss
from evidently.legacy.tests import TestPrecisionScore
from evidently.legacy.tests import TestRecallScore
from evidently.legacy.tests import TestRocAuc
from evidently.legacy.utils.data_preprocessing import DataDefinition


class BinaryClassificationTopKTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:BinaryClassificationTopKTestPreset"

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

    k: int
    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        k: int,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        self.k = k
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        target = data_definition.get_target_column()
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        return [
            TestAccuracyScore(k=self.k),
            TestPrecisionScore(k=self.k),
            TestRecallScore(k=self.k),
            TestF1Score(k=self.k),
            TestColumnDrift(
                column_name=target.column_name,
                stattest=self.stattest,
                stattest_threshold=self.stattest_threshold,
            ),
            TestRocAuc(),
            TestLogLoss(),
        ]
