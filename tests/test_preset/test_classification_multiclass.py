import pandas as pd

from evidently.legacy.test_preset import MulticlassClassificationTestPreset
from evidently.legacy.test_suite import TestSuite


def test_no_target_performance_preset():
    test_current_dataset = pd.DataFrame(
        {
            "category_feature": ["y", "y", "n", "p"],
            "numerical_feature": [0.4, -12, 0, 234],
            "target": [1, 1, 0, 1],
            "prediction": [0, 0, 1, 0],
        }
    )
    test_reference_dataset = pd.DataFrame(
        {
            "category_feature": ["y", "n", "n", "y"],
            "numerical_feature": [0, 1, 2, 5],
            "target": [0, 0, 0, 1],
            "prediction": [0, 0, 0, 1],
        }
    )
    data_quality_suite = TestSuite(
        tests=[
            MulticlassClassificationTestPreset(stattest="psi"),
        ]
    )

    data_quality_suite.run(current_data=test_current_dataset, reference_data=test_reference_dataset)
    assert not data_quality_suite
    assert len(data_quality_suite.as_dict()["tests"]) == 8
