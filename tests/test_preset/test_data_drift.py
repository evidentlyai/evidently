import pandas as pd

from evidently import ColumnMapping
from evidently.test_preset import DataDrift
from evidently.test_suite import TestSuite


def test_data_drift_preset():
    test_current_dataset = pd.DataFrame(
        {
            "category_feature_1": ["y", "y", "n", "y"],
            "category_feature_2": [0, 1, 0, 4],
            "numerical_feature_1": [0.4, -12, 7, 234],
            "numerical_feature_2": [4, -2, 53, 23.4],
            "target": [1, 1, 0, 1],
            "prediction": [0, 0, 1, 0],
        }
    )
    test_reference_dataset = pd.DataFrame(
        {
            "category_feature_1": ["y", "n", "n", "y"],
            "category_feature_2": [0, 1, 4, 0],
            "numerical_feature_1": [0, 1, 2, 5],
            "numerical_feature_2": [0.1, 4.1, 1.2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    data_quality_suite = TestSuite(
        tests=[
            DataDrift(),
        ]
    )
    column_mapping = ColumnMapping(
        numerical_features=["numerical_feature_1", "numerical_feature_2"],
        categorical_features=["category_feature_1", "category_feature_2"],
    )
    data_quality_suite.run(
        current_data=test_current_dataset, reference_data=test_reference_dataset, column_mapping=column_mapping
    )
    assert data_quality_suite
    assert len(data_quality_suite.as_dict()["tests"]) == 7
