import json

import pandas as pd

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestValueAbsMaxError
from evidently.legacy.tests import TestValueMAE
from evidently.legacy.tests import TestValueMAPE
from evidently.legacy.tests import TestValueMeanError
from evidently.legacy.tests import TestValueR2Score
from evidently.legacy.tests import TestValueRMSE


def test_value_mae_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAE(gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMAE(eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_value_mae_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAE()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The MAE is 0.5. The test threshold is eq=0.5 ± 0.05",
        "group": "regression",
        "name": "Mean Absolute Error (MAE)",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_value_mape_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAPE(lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMAPE(eq=100)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    assert suite.show()
    assert suite.json()


def test_value_mape_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMAPE()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The MAPE is 25.0. The test threshold is eq=25 ± 2.5.",
        "group": "regression",
        "name": "Mean Absolute Percentage Error (MAPE)",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 25.0}}, "value": 25.0},
        "status": "SUCCESS",
    }


def test_value_mean_error_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMeanError(gt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueMeanError(eq=0.0)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_value_mean_error_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 1, 0, 0],
        }
    )
    suite = TestSuite(tests=[TestValueMeanError()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The ME is 0.0. The test threshold is eq=0 ± 0.0816.",
        "group": "regression",
        "name": "Mean Error (ME)",
        "parameters": {
            "condition": {"eq": {"absolute": 0.08164965809277261, "relative": 1e-06, "value": 0}},
            "value": 0.0,
        },
        "status": "SUCCESS",
    }


def test_abs_max_error_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1.0, 2.0, 3.0, 4.0],
        }
    )
    suite = TestSuite(tests=[TestValueAbsMaxError(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite
    assert suite.show()
    assert suite.json()


def test_abs_max_error_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "prediction": [1.0, 2.0, 3.0, 4.0],
        }
    )
    suite = TestSuite(tests=[TestValueAbsMaxError()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())

    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The Max Absolute Error is 0.0. The test threshold is lte=0 ± 1e-12.",
        "group": "regression",
        "name": "Max Absolute Error",
        "parameters": {
            "value": 0.0,
            "condition": {"lte": {"absolute": 1e-12, "relative": 0.1, "value": 0.0}},
        },
        "status": "SUCCESS",
    }


def test_r2_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueR2Score(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite
    assert suite.show()
    assert suite.json()


def test_r2_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "prediction": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueR2Score()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The R2 score is 0.8. The test threshold is eq=0.8 ± 0.08.",
        "group": "regression",
        "name": "R2 Score",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.8}}, "value": 0.8},
        "status": "SUCCESS",
    }


def test_rmse_score_test() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "preds": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueRMSE(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping(prediction="preds"))
    assert suite
    assert suite.show()
    assert suite.json()


def test_rmse_score_test_render_json() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 2, 3, 4],
            "prediction": [1, 2, 3, 3],
        }
    )
    suite = TestSuite(tests=[TestValueRMSE()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_json = suite.json()
    assert isinstance(result_json, str)

    result = json.loads(result_json)["tests"][0]
    assert result == {
        "description": "The RMSE is 0.5. The test threshold is eq=0.5 ± 0.05.",
        "group": "regression",
        "name": "Root Mean Square Error (RMSE)",
        "parameters": {"condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.5}}, "value": 0.5},
        "status": "SUCCESS",
    }
