import json

import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.tests import TestAccuracyScore
from evidently.tests import TestPrecisionScore
from evidently.tests import TestF1Score
from evidently.tests import TestRecallScore
from evidently.tests import TestRocAuc
from evidently.tests import TestLogLoss
from evidently.tests import TestPrecisionByClass
from evidently.tests import TestRecallByClass
from evidently.tests import TestF1ByClass
from evidently.test_suite import TestSuite


def test_accuracy_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestAccuracyScore(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite


def test_accuracy_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestAccuracyScore()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "Accuracy Score is 0.5. Test Threshold is eq=0.5 ± 0.05",
        "group": "classification",
        "name": "Accuracy Score",
        "parameters": {"accuracy": 0.5, "condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.5}}},
        "status": "SUCCESS",
    }


def test_precision_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestPrecisionScore(gt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite


def test_precision_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestPrecisionScore()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "Precision Score is 0.5. Test Threshold is eq=0.5 ± 0.05",
        "group": "classification",
        "name": "Precision Score",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.5}}, "precision": 0.5},
        "status": "SUCCESS",
    }


def test_log_loss_test_cannot_calculate_log_loss() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "c"],
            "prediction": ["a", "a", "a", "b", "a", "c", "a", "c", "c", "c"],
        }
    )
    column_mapping = ColumnMapping(target="target", prediction="prediction")

    suite = TestSuite(tests=[TestLogLoss(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite
    test_info = suite.as_dict()["tests"][0]
    assert test_info["description"] == "No log loss value for the data"
    assert test_info["status"] == "ERROR"
