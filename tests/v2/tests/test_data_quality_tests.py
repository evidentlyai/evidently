import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestFeatureValueMin
from evidently.v2.tests import TestFeatureValueMax
from evidently.v2.tests import TestFeatureValueMean
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