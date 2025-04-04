import json

import pandas as pd
import pytest
from pytest import approx as pytest_approx

from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests import TestCategoryCount
from evidently.legacy.tests import TestColumnQuantile
from evidently.legacy.tests import TestColumnValueMax
from evidently.legacy.tests import TestColumnValueMean
from evidently.legacy.tests import TestColumnValueMedian
from evidently.legacy.tests import TestColumnValueMin
from evidently.legacy.tests import TestColumnValueStd
from evidently.legacy.tests import TestConflictPrediction
from evidently.legacy.tests import TestConflictTarget
from evidently.legacy.tests import TestHighlyCorrelatedColumns
from evidently.legacy.tests import TestMeanInNSigmas
from evidently.legacy.tests import TestMostCommonValueShare
from evidently.legacy.tests import TestNumberOfOutListValues
from evidently.legacy.tests import TestNumberOfOutRangeValues
from evidently.legacy.tests import TestNumberOfUniqueValues
from evidently.legacy.tests import TestShareOfOutListValues
from evidently.legacy.tests import TestShareOfOutRangeValues
from evidently.legacy.tests import TestTargetFeaturesCorrelations
from evidently.legacy.tests import TestTargetPredictionCorrelation
from evidently.legacy.tests import TestUniqueValuesShare
from evidently.legacy.tests import TestValueList
from evidently.legacy.tests import TestValueRange
from evidently.legacy.tests.base_test import TestStatus
from evidently.legacy.tests.utils import approx


@pytest.mark.parametrize(
    "test_dataset, reference_dataset, test_object, expected_success",
    (
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature", gte=10),
            False,
        ),
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature", eq=0),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "category_feature": ["n", "d", "p", "n"],
                    "numerical_feature": [0.4, 0.1, -1.45, 5],
                    "target": [0, 0, 0, 1],
                }
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature", eq=approx(-1, absolute=0.5)),
            True,
        ),
        (
            pd.DataFrame(
                {
                    "category_feature": ["n", "d", "p", "n"],
                    "numerical_feature": [10, 7, 5.1, 4.9],
                    "target": [0, 0, 0, 1],
                }
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature", lt=approx(10, relative=0.5)),
            True,
        ),
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [10, 7, 5.1, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature", lt=approx(10, relative=0.5)),
            False,
        ),
    ),
)
def test_data_quality_test_min(
    test_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, test_object: TestColumnValueMin, expected_success: bool
) -> None:
    suite = TestSuite(tests=[test_object])
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=mapping)
    if expected_success:
        suite._inner_suite.raise_for_error()
    assert bool(suite) is expected_success


@pytest.mark.parametrize(
    "test_dataset, reference_dataset, test_object, expected_success",
    (
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestColumnValueMin(column_name="numerical_feature"),
            False,
        ),
    ),
)
def test_data_quality_test_min_exception(
    test_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, test_object: TestColumnValueMin, expected_success: bool
) -> None:
    suite = TestSuite(tests=[test_object])
    suite.run(current_data=test_dataset, reference_data=reference_dataset)
    assert suite.as_dict()["tests"][0]["status"] == TestStatus.ERROR.value


def test_data_quality_test_min_render():
    test_dataset = pd.DataFrame({"numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestColumnValueMin(column_name="numerical_feature", eq=0)])
    column_mapping = ColumnMapping(numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestColumnValueMin(column_name="numerical_feature")])
    mapping = ColumnMapping(numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite.show()
    assert suite.json()


def test_data_quality_test_max() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestColumnValueMax(column_name="numerical_feature", gt=10)])
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite

    suite = TestSuite(tests=[TestColumnValueMax(column_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite


def test_data_quality_test_max_render():
    test_dataset = pd.DataFrame({"numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]})
    suite = TestSuite(tests=[TestColumnValueMax(column_name="numerical_feature", eq=0)])
    mapping = ColumnMapping(numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestColumnValueMax(column_name="numerical_feature")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite.show()
    assert suite.json()


def test_data_quality_test_mean() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestColumnValueMean(column_name="numerical_feature", eq=5)])
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite

    suite = TestSuite(tests=[TestColumnValueMean(column_name="numerical_feature", gt=0, lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite

    suite = TestSuite(tests=[TestColumnValueMean(column_name="numerical_feature", eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite


def test_data_quality_test_mean_render():
    test_dataset = pd.DataFrame({"numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]})
    mapping = ColumnMapping(numerical_features=["numerical_feature"])
    suite = TestSuite(tests=[TestColumnValueMean(column_name="numerical_feature", eq=0)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite.show()
    assert suite.json()

    suite = TestSuite(tests=[TestColumnValueMean(column_name="numerical_feature")])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite.show()
    assert suite.json()


def test_data_quality_test_conflict_target() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "n", "p", "n"], "numerical_feature": [0, 0, 2, 5], "target": [0, 1, 0, 1]}
    )
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite

    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_conflict_prediction() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "n", "p", "n"], "numerical_feature": [0, 0, 2, 5], "prediction": [0, 1, 0, 1]}
    )
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    suite._inner_suite.raise_for_error()
    assert not suite

    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "prediction": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_target_prediction_correlation() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    mapping = ColumnMapping(categorical_features=["category_feature"], numerical_features=["numerical_feature"])
    suite = TestSuite(tests=[TestTargetPredictionCorrelation(gt=0.5, method="cramer_v")])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_median() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite = TestSuite(tests=[TestColumnValueMedian(column_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite
    suite = TestSuite(tests=[TestColumnValueMedian(column_name="feature1", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_std() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestColumnValueStd(column_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestColumnValueStd(column_name="feature1", lt=2)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite
    suite = TestSuite(tests=[TestColumnValueStd(column_name="feature1", gt=2, lt=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_unique_number() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfUniqueValues(column_name="no_existing_feature", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(column_name="feature1", lt=2)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(column_name="feature1", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_unique_share() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestUniqueValuesShare(column_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(column_name="feature1", lt=0.5)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(column_name="feature1", eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_most_common_value_share() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1")])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="no_existing_feature", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_most_common_value_share_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 5],
        }
    )
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1", eq=0.5)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": (
            "The most common value in the column **feature1** is 1. Its share is 0.5. The test threshold is eq=0.5."
        ),
        "group": "data_quality",
        "name": "Share of the Most Common Value",
        "parameters": {"column_name": "feature1", "condition": {"eq": 0.5}, "value": 0.5},
        "status": "SUCCESS",
    }


def test_data_quality_test_value_in_n_sigmas() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="feature1")])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=mapping)
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="not_exist_feature", n_sigmas=3)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="feature1", n_sigmas=4)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=mapping)
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_value_in_n_sigmas_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="feature1", n_sigmas=5)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=mapping)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The mean value of the column **feature1** is 0.5. The expected range is from -2.4 to 3.4",
        "group": "data_quality",
        "name": "Mean Value Stability",
        "parameters": {
            "column_name": "feature1",
            "current_mean": 0.5,
            "n_sigmas": 5,
            "reference_mean": 0.5,
            "reference_std": 0.58,
        },
        "status": "SUCCESS",
    }


def test_data_quality_test_value_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3, 4, 20],
            "target": [0, 0, 0, 1, 0, 1],
            "prediction": [0, 0, 1, 1, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column_name="feature1", left=0, right=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column_name="feature1", left=0, right=100)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3, 2, 4, 5],
            "target": [0, 0, 0, 1, 0, 1, 1],
            "prediction": [0, 0, 1, 1, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column_name="feature1", right=100)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_number_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 2, 3, 4, 15],
            "target": [0, 0, 2, 3, 4, 5, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", left=0, right=10, lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", left=0, right=10, lte=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3, 4, 5, 6, 7],
            "target": [0, 0, 0, 1, 0, 0, 1, 1],
            "prediction": [0, 0, 1, 1, 0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", lt=1)])
    suite.run(
        current_data=test_dataset,
        reference_data=reference_dataset,
        column_mapping=ColumnMapping(
            prediction=None,
            numerical_features=["feature1"],
        ),
    )
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", lte=1)])
    suite.run(
        current_data=test_dataset,
        reference_data=reference_dataset,
        column_mapping=ColumnMapping(
            prediction=None,
            numerical_features=["feature1"],
        ),
    )
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_share_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 2, 3, 4, 15],
            "target": [0, 0, 2, 3, 4, 5, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, lt=0.1)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3, 4, 5, 6, 7],
            "target": [0, 0, 0, 1, 0, 0, 1, 1],
            "prediction": [0, 0, 1, 1, 0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", lt=0.1)])
    suite.run(
        current_data=test_dataset,
        reference_data=reference_dataset,
        column_mapping=ColumnMapping(
            prediction=None,
            numerical_features=["feature1"],
        ),
    )
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", lte=0.5)])
    suite.run(
        current_data=test_dataset,
        reference_data=reference_dataset,
        column_mapping=ColumnMapping(
            prediction=None,
            numerical_features=["feature1"],
        ),
    )
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_share_of_values_not_in_range_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0, 24, 2, 3, 4],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, gt=0.2)])
    mapping = ColumnMapping(numerical_features=["feature1"])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=mapping)
    assert not suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is False
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": (
            "The share of values out of range in the column **feature1** is 0.125 (1 out of 8)."
            "  The test threshold is gt=0.2."
        ),
        "group": "data_quality",
        "name": "Share of Out-of-Range Values",
        "parameters": {"condition": {"gt": 0.2}, "left": 0, "right": 10, "value": 0.125},
        "status": "FAIL",
    }


def test_data_quality_test_value_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3, 4, 20],
            "target": [0, 0, 0, 1, 0, 1],
            "prediction": [0, 0, 1, 1, 0, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3, 2, 4, 5],
            "target": [0, 0, 0, 1, 0, 1, 1],
            "prediction": [0, 0, 1, 2, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueList(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueList(column_name="prediction", values=[0, 1])])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestValueList(column_name="target")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_value_in_list_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "target": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "target": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestValueList(column_name="target")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "All values in the column **target** are in the list.",
        "group": "data_quality",
        "name": "Out-of-List Values",
        "parameters": {"column_name": "target", "value": 0, "values": None},
        "status": "SUCCESS",
    }


def test_data_quality_test_number_of_values_not_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [2, 4, 4, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [2, 4, 4, 2],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutListValues(column_name="feature1", gt=10)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutListValues(column_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite
    assert suite.show()
    assert suite.json()


def test_data_quality_test_share_of_values_not_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )

    suite = TestSuite(tests=[TestShareOfOutListValues(column_name="feature1", values=[0], lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutListValues(column_name="feature1", values=[0, 1], lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_share_of_values_not_in_list_json_render() -> None:
    current_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 10, 20],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
        }
    )

    suite = TestSuite(tests=[TestShareOfOutListValues(column_name="feature1")])
    suite.run(current_data=current_dataset, reference_data=reference_dataset)
    assert not suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is False
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": (
            "The share of values out of list in the column **feature1** is 0.25 (1 out of 4)."
            " The test threshold is eq=0 ± 1e-12."
        ),
        "group": "data_quality",
        "name": "Share of Out-of-List Values",
        "parameters": {
            "condition": {"eq": {"absolute": 1e-12, "relative": 1e-06, "value": 0}},
            "value": 0.25,
            "values": None,
        },
        "status": "FAIL",
    }


def test_data_quality_test_value_quantile() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )

    suite = TestSuite(tests=[TestColumnQuantile(column_name="feature1", quantile=0.7, lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestColumnQuantile(column_name="feature1", quantile=0.2, lt=0.7)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    suite._inner_suite.raise_for_error()
    assert suite
    assert suite.show()
    assert suite.json()


@pytest.mark.skip("require proper tests case")
def test_data_quality_test_highly_correlated_features() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "feature2": [0, 0, 0, 1],
            "feature3": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestHighlyCorrelatedColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    suite = TestSuite(tests=[TestHighlyCorrelatedColumns(gt=1)])
    suite.run(current_data=test_dataset, reference_data=None)
    assert not suite

    suite = TestSuite(tests=[TestHighlyCorrelatedColumns(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None)
    assert suite
    assert suite.show()
    assert suite.json()


@pytest.mark.skip("require proper tests case")
def test_data_quality_test_highly_correlated_features_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "feature2": [0, 2, 3, 4],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestHighlyCorrelatedColumns()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The maximum correlation is 0.983. The test threshold is eq=0.983 ± 0.0983.",
        "group": "data_quality",
        "name": "Highly Correlated Columns",
        "parameters": {
            "value": 0.983,
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": 0.9827076298239908}},
        },
        "status": "SUCCESS",
    }


@pytest.mark.skip("require proper tests case")
def test_data_quality_test_target_features_correlation() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "target": [0, 0, 0, 1],
        }
    )
    column_mapping = ColumnMapping(task="regression")

    suite = TestSuite(tests=[TestTargetFeaturesCorrelations()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    assert suite

    suite = TestSuite(tests=[TestTargetFeaturesCorrelations(gt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert not suite

    suite = TestSuite(tests=[TestTargetFeaturesCorrelations(lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=column_mapping)
    assert suite
    assert suite.show()
    assert suite.json()


@pytest.mark.skip("require proper tests case")
def test_data_quality_test_target_features_correlation_errors() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "prediction": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestTargetFeaturesCorrelations()])
    suite.run(current_data=test_dataset, reference_data=test_dataset)
    assert not suite

    assert suite.as_dict()["tests"][0] == {
        "description": "No target in the current dataset",
        "group": "data_quality",
        "name": "Correlation between Target and Features",
        "parameters": {"value": None, "condition": {"lt": 0.9}},
        "status": "ERROR",
    }


@pytest.mark.skip("require proper tests case")
def test_data_quality_test_target_features_correlation_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "target": [0.0, 0.0, 0.0, 1.0],
            "prediction": [0.0, 0.0, 0.0, 1.0],
        }
    )
    column_mapping = ColumnMapping(task="regression")
    suite = TestSuite(tests=[TestTargetFeaturesCorrelations()])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=column_mapping)
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "The maximum correlation is 0.775. The test threshold is eq=0.775 ± 0.0775.",
        "group": "data_quality",
        "name": "Correlation between Target and Features",
        "parameters": {
            "abs_max_target_features_correlation": 0.775,
            "condition": {"eq": {"absolute": 1e-12, "relative": 0.1, "value": pytest_approx(0.775, rel=0.1)}},
        },
        "status": "SUCCESS",
    }


def test_category_count_binary_column():
    df = pd.DataFrame({"a": [True, False]})
    test = TestCategoryCount(column_name="a", category=False, lte=0)
    data_quality = TestSuite(
        tests=[
            test,
        ]
    )

    data_quality.run(reference_data=None, current_data=df)

    assert "False" in test.get_description(0)
