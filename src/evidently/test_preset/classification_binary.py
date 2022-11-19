from typing import List
from typing import Optional

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestF1Score
from evidently.tests import TestPrecisionScore
from evidently.tests import TestRecallScore
from evidently.tests import TestRocAuc
from evidently.utils.data_operations import DatasetColumns


class BinaryClassificationTestPreset(TestPreset):
    prediction_type: str
    columns: Optional[List[str]]
    stattest: Optional[PossibleStatTestType]
    threshold_probas: float
    threshold_stattest: Optional[float]

    def __init__(
        self,
        prediction_type: str,
        columns: Optional[List[str]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        threshold_probas: float = 0.5,
        threshold_stattest: Optional[float] = None,
    ):
        super().__init__()
        if prediction_type not in ["probas", "labels"]:
            raise ValueError("`prediction_type` argument should by one of 'probas' or 'labels'")
        self.prediction_type = prediction_type
        self.columns = columns
        self.stattest = stattest
        self.threshold_probas = threshold_probas
        self.threshold_stattest = threshold_stattest

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        if self.prediction_type == "labels":
            return [
                TestColumnValueDrift(column_name=target, stattest=self.stattest, threshold=self.threshold_stattest),
                TestPrecisionScore(),
                TestRecallScore(),
                TestF1Score(),
                TestAccuracyScore(),
            ]
        if self.prediction_type == "probas":
            return [
                TestColumnValueDrift(column_name=target, stattest=self.stattest, threshold=self.threshold_stattest),
                TestRocAuc(),
                TestPrecisionScore(threshold=self.threshold_probas),
                TestRecallScore(threshold=self.threshold_probas),
                TestAccuracyScore(threshold=self.threshold_probas),
                TestF1Score(threshold=self.threshold_probas),
            ]
        raise ValueError(f'Unexpected prediction_type: "{self.prediction_type}"')
