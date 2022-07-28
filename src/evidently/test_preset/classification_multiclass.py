from evidently.analyzers.utils import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore, TestF1Score, TestPrecisionByClass, TestRecallByClass,\
    TestNumberOfRows, TestFeatureValueDrift, TestRocAuc, TestLogLoss


class MulticlassClassification(TestPreset):
    def __init__(self, prediction_type: str):
        super().__init__()
        if prediction_type not in ['probas', 'labels']:
            raise ValueError("`prediction_type` argument should by one of 'probas' or 'labels'")
        self.prediction_type = prediction_type

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        labels = set()
        if data.reference_data is not None:
            labels = labels | set(data.reference_data[columns.utility_columns.target].unique())
        labels = labels | set(data.current_data[columns.utility_columns.target].unique())
        tests = [
            TestAccuracyScore(),
            TestF1Score(),
            *[TestPrecisionByClass(label) for label in labels],
            *[TestRecallByClass(label) for label in labels],
            TestNumberOfRows(),
            TestFeatureValueDrift(column_name=columns.utility_columns.target),
        ]

        if self.prediction_type == 'labels':
            return tests
        if self.prediction_type == 'probas':
            return tests + [TestRocAuc(), TestLogLoss()]
        raise ValueError(f'Unexpected prediction_type: "{self.prediction_type}"')
