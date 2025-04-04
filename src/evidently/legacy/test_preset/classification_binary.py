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
from evidently.legacy.tests import TestPrecisionScore
from evidently.legacy.tests import TestRecallScore
from evidently.legacy.tests import TestRocAuc
from evidently.legacy.utils.data_preprocessing import DataDefinition


class BinaryClassificationTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:BinaryClassificationTestPreset"

    """
    Binary Classification Tests.
    Args:
        stattest: statistical test for target drift test.
        stattest_threshold: threshold for statistical test for target drift test.
        probas_threshold: threshold for label calculation for prediction.

    Contains:
    - `TestColumnValueDrift` for target
    - `TestPrecisionScore`
    - `TestRecallScore`
    - `TestF1Score`
    - `TestAccuracyScore`
    """

    stattest: Optional[PossibleStatTestType] = None
    stattest_threshold: Optional[float] = None
    probas_threshold: Optional[float] = None

    def __init__(
        self,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
        probas_threshold: Optional[float] = None,
    ):
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold
        self.probas_threshold = probas_threshold
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        target = data_definition.get_target_column()

        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        prediction_columns = data_definition.get_prediction_columns()
        is_probas_present = prediction_columns is not None and prediction_columns.prediction_probas is not None
        if not is_probas_present:
            return [
                TestColumnDrift(
                    column_name=target.column_name,
                    stattest=self.stattest,
                    stattest_threshold=self.stattest_threshold,
                ),
                TestPrecisionScore(probas_threshold=self.probas_threshold),
                TestRecallScore(probas_threshold=self.probas_threshold),
                TestF1Score(probas_threshold=self.probas_threshold),
                TestAccuracyScore(probas_threshold=self.probas_threshold),
            ]

        return [
            TestColumnDrift(
                column_name=target.column_name,
                stattest=self.stattest,
                stattest_threshold=self.stattest_threshold,
            ),
            TestRocAuc(),
            TestPrecisionScore(probas_threshold=self.probas_threshold),
            TestRecallScore(probas_threshold=self.probas_threshold),
            TestAccuracyScore(probas_threshold=self.probas_threshold),
            TestF1Score(probas_threshold=self.probas_threshold),
        ]
