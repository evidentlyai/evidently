import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests import TestLogLoss
from evidently.test_suite import TestSuite


def test_log_loss_test_cannot_calculate_log_loss() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "c"],
            "prediction": ["a", "a", "a", "b", "a", "c", "a", "c", "c", "c"],
        }
    )
    column_mapping = ColumnMapping(target="target", prediction="prediction")

    suite = TestSuite(tests=[TestLogLoss()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite
    test_info = suite.as_dict()["tests"][0]
    assert test_info["description"] == "No log loss value for the data"
    assert test_info["status"] == "ERROR"
