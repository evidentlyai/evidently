import json

import pandas as pd
import pytest
from sklearn.metrics import r2_score

from evidently.legacy.base_metric import InputData
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests.custom_test import CustomValueTest


def r2_func(data: InputData):
    return r2_score(data.current_data["target"], data.current_data["prediction"])


def test_custom_test() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "target": [0, 1],
            "prediction": [0, 1],
        }
    )

    # happy path
    suite = TestSuite(tests=[CustomValueTest(r2_func, eq=1)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()

    with pytest.raises(ValueError):  # no conditions specified
        CustomValueTest(func=r2_func, title="R2 score test")

    # failed condition
    suite = TestSuite(tests=[CustomValueTest(r2_func, lt=0)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)
    suite._inner_suite.raise_for_error()
    assert not suite


def test_custom_test_json_render() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "target": [0, 1],
            "prediction": [0, 1],
        }
    )
    suite = TestSuite(tests=[CustomValueTest(r2_func, title="r2_score", eq=1)])
    suite.run(current_data=test_current_dataset, reference_data=test_current_dataset)

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "name": "Custom Value test",
        "description": "Custom function 'r2_score' value is 1.0. The test threshold is eq=1",
        "status": "SUCCESS",
        "group": "custom",
        "parameters": {"condition": {"eq": 1}, "value": 1.0},
    }
