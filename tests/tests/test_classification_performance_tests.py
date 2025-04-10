import json

import pandas as pd
from pytest import approx

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestAccuracyScore
from evidently.legacy.tests import TestF1ByClass
from evidently.legacy.tests import TestF1Score
from evidently.legacy.tests import TestFNR
from evidently.legacy.tests import TestFPR
from evidently.legacy.tests import TestLogLoss
from evidently.legacy.tests import TestPrecisionByClass
from evidently.legacy.tests import TestPrecisionScore
from evidently.legacy.tests import TestRecallByClass
from evidently.legacy.tests import TestRecallScore
from evidently.legacy.tests import TestRocAuc
from evidently.legacy.tests import TestTNR
from evidently.legacy.tests import TestTPR


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
    assert suite.show()
    assert suite.json()


def test_accuracy_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestAccuracyScore()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The Accuracy Score is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "Accuracy Score",
        "parameters": {"value": 0.5, "condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}},
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
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_precision_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestPrecisionScore()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The Precision Score is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "Precision Score",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_f1_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestF1Score(gt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_f1_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestF1Score()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The F1 Score is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "F1 Score",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_recall_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestRecallScore(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_recall_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestRecallScore()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The Recall Score is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "Recall Score",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_log_loss_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "b": [0.2, 0.5, 0.3, 0.6],
        }
    )
    column_mapping = ColumnMapping(prediction="b", pos_label="a")
    suite = TestSuite(tests=[TestLogLoss(gte=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestLogLoss(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_log_loss_test_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "b": [0.2, 0.5, 0.3, 0.6],
        }
    )
    column_mapping = ColumnMapping(prediction="b", pos_label="a")
    suite = TestSuite(tests=[TestLogLoss()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The Logarithmic Loss is 0.446. The test threshold is eq=0.446 ± 0.0892",
        "group": "classification",
        "name": "Logarithmic Loss",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": approx(0.446, abs=0.0001)}},
            "value": approx(0.446, abs=0.0001),
        },
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
    assert (
        test_info["description"] == "Not enough data to calculate Logarithmic Loss."
        " Consider providing probabilities instead of labels."
    )
    assert test_info["status"] == "ERROR"


def test_roc_auc_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "a": [0.8, 0.5, 0.7, 0.3],
            "b": [0.2, 0.5, 0.3, 0.6],
        }
    )
    column_mapping = ColumnMapping(prediction=["a", "b"], pos_label="a")
    suite = TestSuite(tests=[TestRocAuc(gte=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestRocAuc(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite
    assert suite.show()
    assert suite.json()


def test_roc_auc_test_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["t", "f", "f", "t"],
            "f": [0.8, 0.5, 0.7, 0.3],
            "t": [0.2, 0.5, 0.3, 0.6],
        }
    )
    column_mapping = ColumnMapping(prediction=["f", "t"], pos_label="t")
    suite = TestSuite(tests=[TestRocAuc(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The ROC AUC Score is 0.5. The test threshold is lt=0.8",
        "group": "classification",
        "name": "ROC AUC Score",
        "parameters": {"condition": {"lt": 0.8}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_roc_auc_test_cannot_calculate_roc_auc() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b", "b", "b", "c", "c", "c", "c"],
            "prediction": ["a", "a", "a", "b", "a", "c", "a", "c", "c", "c"],
        }
    )
    column_mapping = ColumnMapping(target="target", prediction="prediction")

    suite = TestSuite(tests=[TestRocAuc(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite
    test_info = suite.as_dict()["tests"][0]
    assert (
        test_info["description"] == "Not enough data to calculate ROC AUC."
        " Consider providing probabilities instead of labels."
    )
    assert test_info["status"] == "ERROR"


def test_precision_by_class_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestPrecisionByClass(label="a", gt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_precision_by_class_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestPrecisionByClass(label=1)])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The precision score of the label **1** is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "Precision Score by Class",
        "parameters": {
            "label": 1,
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}},
            "value": 0.5,
        },
        "status": "SUCCESS",
    }


def test_f1_by_class_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestF1ByClass(label="a", gt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_f1_by_class_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 1, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestF1ByClass(label=0)])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The F1 score of the label **0** is 0. The test threshold is eq=0 ± 1e-12",
        "group": "classification",
        "name": "F1 Score by Class",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.0}},
            "value": 0.0,
            "label": 0,
        },
        "status": "SUCCESS",
    }


def test_recall_by_class_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "a", "b"],
            "prediction": ["a", "a", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestRecallByClass(label="b", gt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_recall_by_class_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 1, 0],
        }
    )
    suite = TestSuite(tests=[TestRecallByClass(label=1)])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The recall score of the label **1** is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "Recall Score by Class",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}},
            "label": 1,
            "value": 0.5,
        },
        "status": "SUCCESS",
    }


def test_tpr_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestTPR(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_tpr_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestTPR()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The True Positive Rate is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "True Positive Rate",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_tnr_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestTNR(gt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_tnr_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestTNR()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The True Negative Rate is 1. The test threshold is eq=1 ± 0.2",
        "group": "classification",
        "name": "True Negative Rate",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 1}}, "value": 1},
        "status": "SUCCESS",
    }


def test_fpr_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestFPR(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_fpr_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestFPR()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The False Positive Rate is 0. The test threshold is eq=0 ± 1e-12",
        "group": "classification",
        "name": "False Positive Rate",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0}}, "value": 0},
        "status": "SUCCESS",
    }


def test_fnr_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestFNR(lt=0.8)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_fnr_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": ["a", "a", "b", "b"],
            "prediction": ["a", "b", "b", "b"],
        }
    )
    column_mapping = ColumnMapping(pos_label="a")
    suite = TestSuite(tests=[TestFNR()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The False Negative Rate is 0.5. The test threshold is eq=0.5 ± 0.1",
        "group": "classification",
        "name": "False Negative Rate",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.2, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }
