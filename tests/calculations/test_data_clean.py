import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.legacy.utils.data_operations import replace_infinity_values_to_nan


@pytest.mark.parametrize(
    "dataset, expected_dataset",
    (
        (pd.DataFrame({"test": [1, 2, 3]}), {"test": {0: 1, 1: 2, 2: 3}}),
        (pd.DataFrame({"test": [1, 2, np.inf]}), {"test": {0: 1.0, 1: 2.0, 2: approx(np.nan, nan_ok=True)}}),
        (
            pd.DataFrame({"test": [np.nan, np.inf, -np.inf]}),
            {"test": {0: approx(np.nan, nan_ok=True), 1: approx(np.nan, nan_ok=True), 2: approx(np.nan, nan_ok=True)}},
        ),
        (
            pd.DataFrame({"test": [np.nan, np.inf, 2, 0, 0], "target": [1, 0, 1, 0, -np.inf]}),
            {
                "target": {0: 1, 1: 0, 2: 1, 3: 0, 4: approx(np.nan, nan_ok=True)},
                "test": {0: approx(np.nan, nan_ok=True), 1: approx(np.nan, nan_ok=True), 2: 2, 3: 0, 4: 0},
            },
        ),
    ),
)
def test_replace_infinity_values_to_nan(dataset: pd.DataFrame, expected_dataset: dict) -> None:
    assert replace_infinity_values_to_nan(dataset).to_dict() == expected_dataset
