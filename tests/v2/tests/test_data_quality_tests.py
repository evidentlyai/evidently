import pandas as pd

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
from evidently.v2.test_suite import TestSuite


def test_data_quality_test_min() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMin(feature_name="numerical_feature", gte=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMin(feature_name="numerical_feature", eq=0)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_max() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMax(feature_name="numerical_feature", gt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMax(feature_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_mean() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", eq=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite

    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", gt=0, lt=10)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite

    suite = TestSuite(tests=[TestFeatureValueMean(feature_name="numerical_feature", eq=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_target() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1]
        }
    )
    suite = TestSuite(tests=[TestConflictTarget(lt=5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite


def test_data_quality_test_conflict_prediction() -> None:
    test_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestConflictPrediction(lt=5)])
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
    suite = TestSuite(tests=[TestFeatureValueMedian(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueMedian(feature_name="feature1", eq=1.5)])
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
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestFeatureValueStd(feature_name="feature1", gt=2, lt=3)])
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
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="no_existing_feature", eq=4)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="feature1", lt=2)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestNumberOfUniqueValues(feature_name="feature1", eq=4)])
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
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="no_existing_feature", eq=1.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="feature1", lt=0.5)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert not suite
    suite = TestSuite(tests=[TestUniqueValuesShare(feature_name="feature1", eq=1)])
    suite.run(current_data=test_dataset, reference_data=None, column_mapping=ColumnMapping())
    assert suite
