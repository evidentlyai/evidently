import json

import pandas as pd

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestColumnDrift
from evidently.legacy.tests import TestNumberOfDriftedColumns
from evidently.legacy.tests import TestShareOfDriftedColumns


def test_data_drift_test_number_of_drifted_features() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfDriftedColumns()])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestNumberOfDriftedColumns(is_in=[234, 14])])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    assert not suite

    suite = TestSuite(tests=[TestNumberOfDriftedColumns(lt=1)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_drift_test_number_of_drifted_features_json_render() -> None:
    current_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 1, 0, 1],
            "prediction": [1, 1, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfDriftedColumns()])
    suite.run(current_data=current_dataset, reference_data=reference_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The drift is detected for 0 out of 4 features. The test " "threshold is lt=1.",
        "group": "data_drift",
        "name": "Number of Drifted Features",
        "parameters": {
            "condition": {"lt": 1},
            "features": {
                "category_feature": {
                    "detected": False,
                    "score": 1.0,
                    "stattest": "chi-square " "p_value",
                    "threshold": 0.05,
                },
                "numerical_feature": {
                    "detected": False,
                    "score": 1.0,
                    "stattest": "chi-square " "p_value",
                    "threshold": 0.05,
                },
                "prediction": {
                    "detected": False,
                    "score": 0.157,
                    "stattest": "Z-test p_value",
                    "threshold": 0.05,
                },
                "target": {
                    "detected": False,
                    "score": 0.157,
                    "stattest": "Z-test p_value",
                    "threshold": 0.05,
                },
            },
        },
        "status": "SUCCESS",
    }


def test_data_drift_test_share_of_drifted_features() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [1, 0, 0, 1],
            "prediction": [1, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfDriftedColumns()])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    suite = TestSuite(tests=[TestShareOfDriftedColumns(gt=0.6)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    assert not suite

    suite = TestSuite(tests=[TestShareOfDriftedColumns(lte=0.5)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_drift_test_share_of_drifted_features_json_render() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfDriftedColumns()])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The drift is detected for 0% features (0 out of 4). The test " "threshold is lt=0.3",
        "group": "data_drift",
        "name": "Share of Drifted Columns",
        "parameters": {
            "condition": {"lt": 0.3},
            "features": {
                "category_feature": {
                    "detected": False,
                    "score": 1.0,
                    "stattest": "chi-square " "p_value",
                    "threshold": 0.05,
                },
                "numerical_feature": {
                    "detected": False,
                    "score": 1.0,
                    "stattest": "chi-square " "p_value",
                    "threshold": 0.05,
                },
                "prediction": {
                    "detected": False,
                    "score": 1.0,
                    "stattest": "Z-test p_value",
                    "threshold": 0.05,
                },
                "target": {"detected": False, "score": 1.0, "stattest": "Z-test p_value", "threshold": 0.05},
            },
        },
        "status": "SUCCESS",
    }


def test_data_drift_test_feature_value_drift() -> None:
    test_current_dataset = pd.DataFrame({"feature_1": [0, 0, 0, 1], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]})
    test_reference_dataset = pd.DataFrame(
        {"feature_1": [0, 1, 2, 0], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestColumnDrift(column_name="feature_1")])
    suite.run(current_data=test_current_dataset, reference_data=test_reference_dataset, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_drift_test_feature_value_drift_json_render() -> None:
    test_current_dataset = pd.DataFrame({"feature_1": [0, 0, 0, 1], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]})
    test_reference_dataset = pd.DataFrame(
        {"feature_1": [1, 1, 2, 0], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestColumnDrift(column_name="feature_1")])
    suite.run(current_data=test_current_dataset, reference_data=test_reference_dataset)
    suite._inner_suite.raise_for_error()
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The drift score for the feature **feature_1** is 0.064."
        " The drift detection method is chi-square p_value. The drift detection threshold is 0.05.",
        "group": "data_drift",
        "name": "Drift per Column",
        "parameters": {
            "detected": False,
            "score": 0.064,
            "stattest": "chi-square p_value",
            "threshold": 0.05,
            "column_name": "feature_1",
        },
        "status": "SUCCESS",
    }
