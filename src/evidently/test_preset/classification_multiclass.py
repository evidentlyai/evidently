from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAccuracyScore
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestF1Score
from evidently.tests import TestLogLoss
from evidently.tests import TestNumberOfRows
from evidently.tests import TestPrecisionByClass
from evidently.tests import TestRecallByClass
from evidently.tests import TestRocAuc
from evidently.utils.data_operations import DatasetColumns


class MulticlassClassificationTestPreset(TestPreset):
    def __init__(self, prediction_type: str):
        super().__init__()
        if prediction_type not in ["probas", "labels"]:
            raise ValueError("`prediction_type` argument should by one of 'probas' or 'labels'")
        self.prediction_type = prediction_type

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        target = columns.utility_columns.target
        if target is None:
            raise ValueError("Target column should be set in mapping and be present in data")
        labels = set(data.current_data[target].unique())
        if data.reference_data is not None:
            labels = labels | set(data.reference_data[target].unique())
        tests = [
            TestAccuracyScore(),
            TestF1Score(),
            *[TestPrecisionByClass(str(label)) for label in labels],
            *[TestRecallByClass(str(label)) for label in labels],
            TestNumberOfRows(),
            TestColumnValueDrift(column_name=target),
        ]

        if self.prediction_type == "labels":
            return tests
        if self.prediction_type == "probas":
            return tests + [TestRocAuc(), TestLogLoss()]
        raise ValueError(f'Unexpected prediction_type: "{self.prediction_type}"')
