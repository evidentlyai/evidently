import json

import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestConflictTarget
from evidently.v2.tests import TestConflictPrediction
from evidently.v2.tests import TestTargetPredictionCorrelation
from evidently.v2.tests import TestFeatureValueMin
from evidently.v2.tests import TestFeatureValueMax
from evidently.v2.tests import TestFeatureValueMean
from evidently.v2.tests import TestFeatureValueMedian
from evidently.v2.tests import TestFeatureValueStd
from evidently.v2.tests import TestNumberOfUniqueValues
from evidently.v2.tests import TestUniqueValuesShare
from evidently.v2.tests import TestMostCommonValueShare
from evidently.v2.tests import TestMeanInNSigmas
from evidently.v2.tests import TestValueRange
from evidently.v2.tests import TestNumberOfOutRangeValues
from evidently.v2.tests import TestShareOfOutRangeValues
from evidently.v2.tests import TestValueList
from evidently.v2.tests import TestNumberOfOutListValues
from evidently.v2.tests import TestShareOfOutListValues
from evidently.v2.tests import TestValueQuantile
from evidently.v2.test_suite import TestSuite
from evidently.v2.tests.utils import approx


@pytest.mark.parametrize(
    "test_dataset, reference_dataset, test_object, expected_success",
    (
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestFeatureValueMin(column_name="numerical_feature", gte=10),
            False,
        ),
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestFeatureValueMin(column_name="numerical_feature", eq=0),
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
            TestFeatureValueMin(column_name="numerical_feature", eq=approx(-1, absolute=0.5)),
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
            TestFeatureValueMin(column_name="numerical_feature", lt=approx(10, relative=0.5)),
            True,
        ),
        (
            pd.DataFrame(
                {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [10, 7, 5.1, 5], "target": [0, 0, 0, 1]}
            ),
            None,
            TestFeatureValueMin(column_name="numerical_feature", lt=approx(10, relative=0.5)),
            False,
        ),
    ),
)
def test_data_quality_test_min(
    test_dataset: pd.DataFrame,
    reference_dataset: pd.DataFrame,
    test_object: TestFeatureValueMin,
    expected_success: bool,
) -> None:
    suite = TestSuite(tests=[test_object])
    suite.run(current_data=test_dataset, reference_data=reference_dataset)
    assert bool(suite) is expected_success


def test_data_quality_test_max() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestFeatureValueMax(column_name="numerical_feature", gt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMax(column_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_mean() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestFeatureValueMean(column_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMean(column_name="numerical_feature", gt=0, lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestFeatureValueMean(column_name="numerical_feature", eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_target() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "n", "p", "n"], "numerical_feature": [0, 0, 2, 5], "target": [0, 1, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "target": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictTarget()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_prediction() -> None:
    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "n", "p", "n"], "numerical_feature": [0, 0, 2, 5], "prediction": [0, 1, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    test_dataset = pd.DataFrame(
        {"category_feature": ["n", "d", "p", "n"], "numerical_feature": [0, 1, 2, 5], "prediction": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestConflictPrediction()])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_target_prediction_correlation() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestTargetPredictionCorrelation(gt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_median() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMedian(column_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueMedian(column_name="feature1", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_std() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestFeatureValueStd(column_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(column_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(column_name="feature1", gt=2, lt=3)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(column_name="feature1", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(column_name="feature1", eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_most_common_value_share() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="no_existing_feature", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestMostCommonValueShare(column_name="feature1", eq=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


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
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="not_exist_feature", n_sigmas=3)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="feature1", n_sigmas=4)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_value_in_n_sigmas_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestMeanInNSigmas(column_name="feature1", n_sigmas=5)])
    suite.run(current_data=test_dataset, reference_data=test_dataset, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "Mean value of column feature1 0.5 is in range from -2.4 to 3.4",
        "group": "data_quality",
        "name": "Test Mean Value Stability",
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
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column_name="feature1", left=0, right=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column_name="feature1", left=0, right=100)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueRange(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueRange(column_name="feature1", right=100)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_number_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 15],
            "target": [0, 0, 5, 1],
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
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", lt=1)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestNumberOfOutRangeValues(column_name="feature1", lte=1)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_share_of_values_not_in_range() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 15],
            "target": [0, 0, 5, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, lt=0.2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", lt=0.2)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", lte=0.5)])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_share_of_values_not_in_range_json_render() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0, 24],
        }
    )
    suite = TestSuite(tests=[TestShareOfOutRangeValues(column_name="feature1", left=0, right=10, gt=0.2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is False
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "Share of Out-Of-Range Values for feature feature1 is 0.2. Test Threshold is [gt=0.2].",
        "group": "data_quality",
        "name": "Test Share of Out-Of-Range Values",
        "parameters": {"condition": {"gt": 0.2}, "left": 0, "right": 10, "share_not_in_range": 0.2},
        "status": "FAIL",
    }


def test_data_quality_test_value_in_list() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    reference_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 0],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )
    suite = TestSuite(tests=[TestValueList(column_name="feature1")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueList(column_name="target")])
    suite.run(current_data=test_dataset, reference_data=reference_dataset, column_mapping=ColumnMapping())
    assert suite


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
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 1, 20],
        }
    )

    suite = TestSuite(tests=[TestShareOfOutListValues(column_name="feature1", values=[0, 1], lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    result_from_json = json.loads(suite.json())
    assert result_from_json["summary"]["all_passed"] is True
    test_info = result_from_json["tests"][0]
    assert test_info == {
        "description": "Share of Out-Of-List Values for feature feature1 is 0.25. "
        "Values list is [0, 1]. Test Threshold is [lt=0.5].",
        "group": "data_quality",
        "name": "Test Share of Out-Of-List Values",
        "parameters": {"condition": {"lt": 0.5}, "share_not_in_list": 0.25, "values": [0, 1]},
        "status": "SUCCESS",
    }


def test_data_quality_test_value_quantile() -> None:
    test_dataset = pd.DataFrame(
        {
            "feature1": [0, 1, 2, 3],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 1, 1],
        }
    )

    suite = TestSuite(tests=[TestValueQuantile(column_name="feature1", quantile=0.7, lt=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestValueQuantile(column_name="feature1", quantile=0.2, lt=0.7)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
