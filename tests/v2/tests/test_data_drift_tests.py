import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.v2.tests import TestNumberOfDriftedFeatures
from evidently.v2.tests import TestShareOfDriftedFeatures
from evidently.v2.tests import TestFeatureValueDrift
from evidently.v2.test_suite import TestSuite


def test_data_drift_test_of_drifted_features() -> None:
    test_current_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    test_reference_dataset = pd.DataFrame(
        {
            "category_feature": ["n", "d", "p", "n"],
            "numerical_feature": [3, 1, 2, 0],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    suite = TestSuite(tests=[TestNumberOfDriftedFeatures(lt=3), TestShareOfDriftedFeatures(lte=0.5)])
    suite.run(current_data=test_current_dataset, reference_data=test_reference_dataset, column_mapping=ColumnMapping())
    assert suite


def test_data_drift_test_feature_value_drift() -> None:
    test_current_dataset = pd.DataFrame({"feature_1": [0, 1, 2, 3], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]})
    test_reference_dataset = pd.DataFrame(
        {"feature_1": [0, 1, 2, 0], "target": [0, 0, 0, 1], "prediction": [0, 0, 0, 1]}
    )
    suite = TestSuite(tests=[TestFeatureValueDrift(column_name="feature_1", lt=1)])
    suite.run(current_data=test_current_dataset, reference_data=test_reference_dataset, column_mapping=ColumnMapping())
    assert suite
