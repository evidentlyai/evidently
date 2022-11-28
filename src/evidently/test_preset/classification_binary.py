from typing import List
from typing import Optional

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore
from evidently.tests import TestColumnDrift
from evidently.tests import TestF1Score
from evidently.tests import TestPrecisionScore
from evidently.tests import TestRecallScore
from evidently.tests import TestRocAuc
from evidently.utils.data_operations import DatasetColumns


class BinaryClassificationTestPreset(TestPreset):
    """
    Binary Classification Tests.
    Args:
        threshold: probabilities threshold for prediction with probas
        prediction_type: type of prediction ('probas' or 'labels')

    Contains:
    - `TestColumnValueDrift` for target
    - `TestPrecisionScore` - use threshold if prediction_type is 'probas'
    - `TestRecallScore` - use threshold if prediction_type is 'probas'
    - `TestF1Score` - use threshold if prediction_type is 'probas'
    - `TestAccuracyScore` - use threshold if prediction_type is 'probas'
    """

    def __init__(
        self,
        prediction_type: str,
        columns: Optional[List[str]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
        probas_threshold: Optional[float] = None,
    ):
        super().__init__()

        if prediction_type not in ["probas", "labels"]:
            raise ValueError("`prediction_type` argument should by one of 'probas' or 'labels'")

        self.prediction_type = prediction_type
        self.columns = columns
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold
        self.probas_threshold = probas_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target

        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")

        if self.prediction_type == "labels":
            return [
                TestColumnDrift(column_name=target, stattest=self.stattest, stattest_threshold=self.stattest_threshold),
                TestPrecisionScore(probas_threshold=self.probas_threshold),
                TestRecallScore(probas_threshold=self.probas_threshold),
                TestF1Score(probas_threshold=self.probas_threshold),
                TestAccuracyScore(probas_threshold=self.probas_threshold),
            ]

        if self.prediction_type == "probas":
            return [
                TestColumnDrift(column_name=target, stattest=self.stattest, stattest_threshold=self.stattest_threshold),
                TestRocAuc(),
                TestPrecisionScore(probas_threshold=self.probas_threshold),
                TestRecallScore(probas_threshold=self.probas_threshold),
                TestAccuracyScore(probas_threshold=self.probas_threshold),
                TestF1Score(probas_threshold=self.probas_threshold),
            ]

        raise ValueError(f'Unexpected prediction_type: "{self.prediction_type}"')
