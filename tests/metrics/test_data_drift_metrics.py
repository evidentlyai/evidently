from typing import Optional

import numpy as np
import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_drift_metrics import DataDriftMetrics


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, data_mapping, n_drifted_features",
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
            0,
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
            2,
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
            2,
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
            1,
        ),
    ),
)
def test_data_drift_metrics(
    current_dataset: pd.DataFrame, reference_dataset: pd.DataFrame, data_mapping: ColumnMapping, n_drifted_features: int
) -> None:
    metric = DataDriftMetrics()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
    )
    assert result is not None
    assert result.metrics.n_drifted_features == n_drifted_features


@pytest.mark.parametrize(
    "current_dataset, reference_dataset",
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
            None,
        ),
    ),
)
def test_data_drift_metrics_value_error(
    current_dataset: pd.DataFrame, reference_dataset: Optional[pd.DataFrame]
) -> None:
    data_mapping = ColumnMapping()
    metric = DataDriftMetrics()

    with pytest.raises(ValueError):
        metric.calculate(
            data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping)
        )
