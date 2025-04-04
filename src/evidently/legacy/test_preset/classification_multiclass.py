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
from evidently.legacy.tests import TestNumberOfRows
from evidently.legacy.tests import TestPrecisionByClass
from evidently.legacy.tests import TestRecallByClass
from evidently.legacy.tests import TestRocAuc
from evidently.legacy.utils.data_preprocessing import DataDefinition


class MulticlassClassificationTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:MulticlassClassificationTestPreset"

    """
    Multiclass Classification tests.

    Args:
        stattest: statistical test for target drift test.
        stattest_threshold: threshold for statistical test for target drift test.

    Contains tests:
    - `TestAccuracyScore`
    - `TestF1Score`
    - `TestPrecisionByClass` for each class in data
    - `TestRecallByClass` for each class in data
    - `TestNumberOfRows`
    - `TestColumnValueDrift`
    - `TestRocAuc`
    - `TestLogLoss`
    """

    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        target = data_definition.get_target_column()

        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")

        classification_labels = data_definition.classification_labels
        if classification_labels is None:
            labels = set()
        else:
            labels = set(
                classification_labels if isinstance(classification_labels, list) else classification_labels.values()
            )

        tests: List[AnyTest] = [
            TestAccuracyScore(),
            TestF1Score(),
            *[TestPrecisionByClass(label=label) for label in labels],
            *[TestRecallByClass(label=label) for label in labels],
            TestNumberOfRows(),
            TestColumnDrift(
                column_name=target.column_name,
                stattest=self.stattest,
                stattest_threshold=self.stattest_threshold,
            ),
        ]

        prediction_columns = data_definition.get_prediction_columns()
        if prediction_columns is None or prediction_columns.prediction_probas is None:
            return tests
        else:
            return tests + [TestRocAuc(), TestLogLoss()]
