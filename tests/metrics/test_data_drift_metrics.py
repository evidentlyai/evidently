import numpy as np
import pandas as pd
import pytest

from evidently.metrics.data_drift_metrics import DataDriftMetrics
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, data_mapping",
    (
        (
            pd.DataFrame(
                {
                    "category_feature": ["1", "2", "3"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.NAN, 1],
                    "prediction": [1, np.NAN, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["1", "2", "3"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.NAN, 1],
                    "prediction": [1, np.NAN, 1],
                }
            ),
            ColumnMapping(),
        ),
        (
            pd.DataFrame(
                {
                    "category_feature": ["1", "2", "3"],
                    "numerical_feature": [3, 2, 1],
                    "target": [None, np.NAN, 1],
                    "prediction": [1, np.NAN, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c", "a", "b", "c"],
                    "numerical_feature": [6, 6, 6, 9, 9, 9],
                    "target": [5, 4, 3, 2, 1, 0],
                    "prediction": [1, 2, 3, 4, 5, 6],
                }
            ),
            ColumnMapping(),
        ),
        # binary classification
        (
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.3, 0.2, 0.1],
                    "label_b": [0.5, 0.5, 1],
                    "target": [1, 1, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.9, 0.5, 0.3],
                    "label_b": [0.2, 0.5, 0.7],
                    "target": [0, 0, 0],
                }
            ),
            ColumnMapping(prediction=["label_a", "label_b"]),
        ),
        # multy classification
        (
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.3, 0.2, 0.1],
                    "label_b": [0.5, 0.5, 1],
                    "label_c": [0.2, 0.5, 0.7],
                    "my_target": [1, 1, 1],
                }
            ),
            pd.DataFrame(
                {
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "label_a": [0.9, 0.5, 0.3],
                    "label_b": [0.2, 0.5, 0.7],
                    "label_c": [0.3, 0.2, 0.1],
                    "my_target": [0, 0, 0],
                }
            ),
            ColumnMapping(target="my_target", prediction=["label_a", "label_b", "label_c"]),
        ),
    ),
)
def test_data_drift_metrics_no_errors(
    current_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, data_mapping: ColumnMapping
) -> None:
    report = Report(metrics=[DataDriftMetrics()])
    report.run(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    assert report.show()
    assert report.json()


def test_data_drift_metrics_value_error() -> None:
    test_data = pd.DataFrame(
        {
            "category_feature": ["1", "2", "3"],
            "numerical_feature": [3, 2, 1],
            "target": [None, np.NAN, 1],
            "prediction": [1, np.NAN, 1],
        }
    )
    data_mapping = ColumnMapping()
    report = Report(metrics=[DataDriftMetrics()])

    with pytest.raises(ValueError):
        report.run(current_data=test_data, reference_data=None, column_mapping=data_mapping)

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        report.run(current_data=None, reference_data=test_data, column_mapping=data_mapping)
