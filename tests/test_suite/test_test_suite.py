import json

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedFeatures
from evidently.tests import TestShareOfDriftedFeatures
from evidently.tests import TestFeatureValueDrift
from evidently.tests import TestNumberOfColumns
from evidently.tests import TestNumberOfRows
from evidently.tests import TestNumberOfNulls
from evidently.tests import TestNumberOfColumnsWithNulls
from evidently.tests import TestNumberOfRowsWithNulls
from evidently.tests import TestNumberOfConstantColumns
from evidently.tests import TestNumberOfEmptyRows
from evidently.tests import TestNumberOfEmptyColumns
from evidently.tests import TestNumberOfDuplicatedRows
from evidently.tests import TestNumberOfDuplicatedColumns
from evidently.tests import TestColumnsType
from evidently.tests import TestColumnShareOfNulls
from evidently.tests import TestColumnAllConstantValues
from evidently.tests import TestColumnAllUniqueValues
from evidently.tests import TestColumnValueRegExp
from evidently.tests import TestConflictTarget
from evidently.tests import TestConflictPrediction
from evidently.tests import TestFeatureValueMin
from evidently.tests import TestFeatureValueMax
from evidently.tests import TestFeatureValueMean
from evidently.tests import TestFeatureValueMedian
from evidently.tests import TestFeatureValueStd
from evidently.tests import TestNumberOfUniqueValues
from evidently.tests import TestUniqueValuesShare
from evidently.tests import TestMostCommonValueShare
from evidently.tests import TestMeanInNSigmas
from evidently.tests import TestValueRange
from evidently.tests import TestNumberOfOutRangeValues
from evidently.tests import TestShareOfOutRangeValues
from evidently.tests import TestValueList
from evidently.tests import TestNumberOfOutListValues
from evidently.tests import TestShareOfOutListValues
from evidently.tests import TestValueQuantile
from evidently.tests.base_test import Test


class ErrorTest(Test):
    name = "Error Test"
    group = "example"

    def check(self):
        raise ValueError("Test Exception")


def test_export_to_json():
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

    tests = [
        TestNumberOfDriftedFeatures(),
        TestShareOfDriftedFeatures(),
        TestFeatureValueDrift(column_name="num_feature_1"),
        TestNumberOfColumns(),
        TestNumberOfRows(),
        TestNumberOfNulls(),
        TestNumberOfColumnsWithNulls(),
        TestNumberOfRowsWithNulls(),
        TestNumberOfConstantColumns(),
        TestNumberOfEmptyRows(),
        TestNumberOfEmptyColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType({"num_feature_1": int, "cat_feature_2": str}),
        TestColumnShareOfNulls(column_name="num_feature_1", gt=5),
        TestColumnValueRegExp(column_name="cat_feature_2", reg_exp=r"[n|y|n//a]"),
        TestConflictTarget(),
        TestConflictPrediction(),
        TestColumnAllConstantValues(column_name="num_feature_1"),
        TestColumnAllUniqueValues(column_name="num_feature_1"),
        TestFeatureValueMin(column_name="num_feature_1"),
        TestFeatureValueMax(column_name="num_feature_1"),
        TestFeatureValueMean(column_name="num_feature_1"),
        TestFeatureValueMedian(column_name="num_feature_1"),
        TestFeatureValueStd(column_name="num_feature_1"),
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
        TestValueQuantile(column_name="num_feature_1", quantile=0.1, lt=2),
        ErrorTest(),
    ]
    suite = TestSuite(tests=tests)
    suite.run(current_data=current_data, reference_data=reference_data, column_mapping=column_mapping)

    # assert suite

    json_str = suite.json()

    assert isinstance(json_str, str)

    json_result = json.loads(json_str)

    assert "tests" in json_result
    assert len(json_result["tests"]) == len(tests)

    for test_info in json_result["tests"]:
        assert "description" in test_info, test_info
        assert "name" in test_info, test_info
        assert "status" in test_info, test_info
        assert "group" in test_info, test_info
        assert "parameters" in test_info, test_info

    assert "datetime" in json_result
    assert isinstance(json_result["datetime"], str)
    assert "version" in json_result

    assert "columns_info" in json_result
    assert json_result["columns_info"] == {
        "cat_feature_names": ["cat_feature_1", "cat_feature_2"],
        "datetime_feature_names": [],
        "num_feature_names": ["num_feature_1", "num_feature_2"],
        "target_names": None,
        "utility_columns": {"date": None, "id_column": None, "prediction": "pred_result", "target": "result"},
    }
    assert "summary" in json_result

    summary_result = json_result["summary"]
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
