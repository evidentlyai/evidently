from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore, TestF1Score, TestPrecisionScore, TestRecallScore, \
    TestFeatureValueDrift, TestRocAuc, TestTPR, TestTNR, TestFPR, TestFNR


class BinaryClassification(TestPreset):
    def __init__(self, prediction_type: str, threshold: float = 0.5):
        super().__init__()
        if prediction_type not in ['probas', 'labels']:
            raise ValueError("`prediction_type` argument should by one of 'probas' or 'labels'")
        self.prediction_type = prediction_type
        self.threshold = threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        tests = []
        tests += [TestFeatureValueDrift(columns.utility_columns.target)]
        if self.prediction_type == 'labels':
            return tests + [
                TestPrecisionScore(),
                TestRecallScore(),
                TestF1Score(),
                TestAccuracyScore(),
            ]
        if self.prediction_type == 'probas':
            return tests + [
                TestRocAuc(),
                TestPrecisionScore(classification_threshold=self.threshold),
                TestRecallScore(classification_threshold=self.threshold),
                TestAccuracyScore(classification_threshold=self.threshold),
                TestF1Score(classification_threshold=self.threshold),
                TestTPR(),
                TestTNR(),
                TestFPR(),
                TestFNR(),
            ]
        raise ValueError(f'Unexpected prediction_type: "{self.prediction_type}"')
