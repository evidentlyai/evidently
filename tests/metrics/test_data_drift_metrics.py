from typing import Optional

import numpy as np
import pandas as pd

import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.metrics.base_metric import InputData
from evidently.metrics.data_drift_metrics import DataDriftMetrics


@pytest.mark.parametrize(
    "current_dataset, reference_dataset, n_drifted_features",
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
                    "category_feature": ["a", "b", "c"],
                    "numerical_feature": [6, 6, 6],
                    "target": [1, 0, 1],
                    "prediction": [1, 0, 1],
                }
            ),
            2,
        ),
    ),
)
def test_data_drift_metrics(
    current_dataset: pd.DataFrame, reference_dataset: Optional[pd.DataFrame], n_drifted_features: int
) -> None:
    data_mapping = ColumnMapping()
    metric = DataDriftMetrics()
    result = metric.calculate(
        data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
        metrics={},
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
            data=InputData(current_data=current_dataset, reference_data=reference_dataset, column_mapping=data_mapping),
            metrics={},
        )
