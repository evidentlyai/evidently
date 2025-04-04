import json
from typing import Dict

import numpy as np
import pandas as pd
import pytest

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestColumnAllConstantValues
from evidently.legacy.tests import TestColumnAllUniqueValues
from evidently.legacy.tests import TestColumnDrift
from evidently.legacy.tests import TestColumnQuantile
from evidently.legacy.tests import TestColumnRegExp
from evidently.legacy.tests import TestColumnShareOfMissingValues
from evidently.legacy.tests import TestColumnsType
from evidently.legacy.tests import TestColumnValueMax
from evidently.legacy.tests import TestColumnValueMean
from evidently.legacy.tests import TestColumnValueMedian
from evidently.legacy.tests import TestColumnValueMin
from evidently.legacy.tests import TestColumnValueStd
from evidently.legacy.tests import TestConflictPrediction
from evidently.legacy.tests import TestConflictTarget
from evidently.legacy.tests import TestMeanInNSigmas
from evidently.legacy.tests import TestMostCommonValueShare
from evidently.legacy.tests import TestNumberOfColumns
from evidently.legacy.tests import TestNumberOfColumnsWithMissingValues
from evidently.legacy.tests import TestNumberOfConstantColumns
from evidently.legacy.tests import TestNumberOfDriftedColumns
from evidently.legacy.tests import TestNumberOfDuplicatedColumns
from evidently.legacy.tests import TestNumberOfDuplicatedRows
from evidently.legacy.tests import TestNumberOfEmptyColumns
from evidently.legacy.tests import TestNumberOfEmptyRows
from evidently.legacy.tests import TestNumberOfMissingValues
from evidently.legacy.tests import TestNumberOfOutListValues
from evidently.legacy.tests import TestNumberOfOutRangeValues
from evidently.legacy.tests import TestNumberOfRows
from evidently.legacy.tests import TestNumberOfRowsWithMissingValues
from evidently.legacy.tests import TestNumberOfUniqueValues
from evidently.legacy.tests import TestShareOfDriftedColumns
from evidently.legacy.tests import TestShareOfOutListValues
from evidently.legacy.tests import TestShareOfOutRangeValues
from evidently.legacy.tests import TestUniqueValuesShare
from evidently.legacy.tests import TestValueList
from evidently.legacy.tests import TestValueRange
from evidently.legacy.tests.base_test import Test


class ErrorTest(Test):
    class Config:
        alias_required = False

    name = "Error Test"
    group = "example"

    def check(self):
        raise ValueError("Test Exception")

    def groups(self) -> Dict[str, str]:
        return {}


@pytest.fixture
def suite():
    tests = [
        TestNumberOfDriftedColumns(),
        TestShareOfDriftedColumns(),
        TestColumnDrift(column_name="num_feature_1"),
        TestNumberOfColumns(),
        TestNumberOfRows(),
        TestNumberOfMissingValues(),
        TestNumberOfColumnsWithMissingValues(),
        TestNumberOfRowsWithMissingValues(),
        TestNumberOfConstantColumns(),
        TestNumberOfEmptyRows(),
        TestNumberOfEmptyColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType({"num_feature_1": int, "cat_feature_2": str}),
        TestColumnShareOfMissingValues(column_name="num_feature_1", gt=5),
        TestColumnRegExp(column_name="cat_feature_2", reg_exp=r"[n|y|n//a]"),
        TestConflictTarget(),
        TestConflictPrediction(),
        TestColumnAllConstantValues(column_name="num_feature_1"),
        TestColumnAllUniqueValues(column_name="num_feature_1"),
        TestColumnValueMin(column_name="num_feature_1"),
        TestColumnValueMax(column_name="num_feature_1"),
        TestColumnValueMean(column_name="num_feature_1"),
        TestColumnValueMedian(column_name="num_feature_1"),
        TestColumnValueStd(column_name="num_feature_1"),
        TestNumberOfUniqueValues(column_name="num_feature_1"),
        TestUniqueValuesShare(column_name="num_feature_1"),
        TestMostCommonValueShare(column_name="num_feature_1"),
        TestMeanInNSigmas(column_name="num_feature_1"),
        TestValueRange(column_name="num_feature_1"),
        TestNumberOfOutRangeValues(column_name="num_feature_1"),
        TestShareOfOutRangeValues(column_name="num_feature_1"),
        TestValueList(column_name="num_feature_1"),
        TestNumberOfOutListValues(column_name="num_feature_1"),
        TestShareOfOutListValues(column_name="num_feature_1"),
        TestColumnQuantile(column_name="num_feature_1", quantile=0.1, lt=2),
        ErrorTest(),
    ]
    suite = TestSuite(tests=tests)
    return suite


@pytest.fixture()
def data():
    current_data = pd.DataFrame(
        {
            "num_feature_1": [1, 2, 3, 4, 5, 6, 7, np.nan, 9, 10],
            "num_feature_2": [-1, 2, 3.4, 4, -5, 6, 7, 99.1, np.nan, np.nan],
            "cat_feature_1": [1, 0, 1, 0, 2, 1, 0, 3, 1, 0],
            "cat_feature_2": ["y", "n", "n/a", "n", "y", "y", "n", "y", "n", "n/a"],
            "result": [1, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            "pred_result": [1, 0, 1, 0, 2, 1, 0, 3, 1, 0],
        }
    )

    reference_data = pd.DataFrame(
        {
            "num_feature_1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "num_feature_2": [0.1, 2, 0.3, 4, 5, -0.6, 7, 8, 9, -10],
            "cat_feature_1": [1, 0, 1, 0, 2, 1, 0, 3, 1, 0],
            "cat_feature_2": ["y", "n", "n/a", "n", "y", "y", "n", "y", "n", "n/a"],
            "result": [1, 0, 1, 0, 1, 1, 0, 0, 1, 0],
            "pred_result": [1, 0, 1, 0, 2, 1, 0, 3, 1, 0],
        }
    )
    column_mapping = ColumnMapping(
        target="result",
        prediction="pred_result",
        numerical_features=["num_feature_1", "num_feature_2"],
        categorical_features=["cat_feature_1", "cat_feature_2"],
    )
    return current_data, reference_data, column_mapping


def test_export_to_json(suite, data):
    current_data, reference_data, column_mapping = data
    suite.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)

    # assert suite

    suite_json = suite.json()

    assert isinstance(suite_json, str)

    result = json.loads(suite_json)

    assert "timestamp" in result
    assert isinstance(result["timestamp"], str)
    assert "version" in result
    assert isinstance(result["version"], str)
    assert "tests" in result
    assert isinstance(result["tests"], list)
    assert "summary" in result
    assert isinstance(result["summary"], dict)

    assert len(result["tests"]) == len(suite._inner_suite.context.tests)

    for test_info in result["tests"]:
        assert "description" in test_info, test_info
        assert "name" in test_info, test_info
        assert "status" in test_info, test_info
        assert "group" in test_info, test_info
        assert "parameters" in test_info, test_info

    summary_result = result["summary"]
    assert "all_passed" in summary_result, summary_result
    assert summary_result["all_passed"] is False

    assert "total_tests" in summary_result
    assert summary_result["total_tests"] == 37

    assert "success_tests" in summary_result
    assert summary_result["success_tests"] == 28

    assert "failed_tests" in summary_result
    assert summary_result["failed_tests"] == 8

    assert "by_status" in summary_result
    assert summary_result["by_status"] == {"FAIL": 8, "SUCCESS": 28, "ERROR": 1}


def test_include_metric_results(suite: TestSuite, data):
    current_data, reference_data, column_mapping = data
    suite.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)

    data = suite.as_dict(include_metrics=True)

    assert "metric_results" in data
    metric_results = data["metric_results"]
    assert len(metric_results) > 0
