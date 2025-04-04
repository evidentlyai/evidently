import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.data_integration import get_number_of_all_pandas_missed_values
from evidently.legacy.calculations.data_integration import get_number_of_almost_constant_columns
from evidently.legacy.calculations.data_integration import get_number_of_almost_duplicated_columns


@pytest.mark.parametrize(
    "dataset, expected_missed",
    (
        (pd.DataFrame(), 0),
        (pd.DataFrame({"feature": []}), 0),
        (pd.DataFrame({"feature": [1, 2, 3]}), 0),
        (pd.DataFrame({"feature1": [1, None, pd.NA], "feature2": [np.nan, None, pd.NaT]}), 5),
    ),
)
def test_get_number_of_all_pandas_missed_values(dataset: pd.DataFrame, expected_missed: int) -> None:
    assert get_number_of_all_pandas_missed_values(dataset) == expected_missed


@pytest.mark.parametrize(
    "dataset, threshold, expected_almost_constant",
    (
        (pd.DataFrame(), 0.95, 0),
        (pd.DataFrame({"feature": []}), 0.95, 0),
        (pd.DataFrame({"feature": [1, 2, 3]}), 0.95, 0),
        (pd.DataFrame({"feature1": [1, 1, 3], "feature2": [1, 1, 3]}), 0.95, 1),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1] * 10 + [2, 3],
                    "feature2": [1, 1] * 10 + [4, 5],
                }
            ),
            0.95,
            0,
        ),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1] * 10 + [2, 3],
                    "feature2": [1, 1] * 10 + [4, 5],
                }
            ),
            0.9,
            1,
        ),
        (
            pd.DataFrame(
                {
                    "feature1": ["a", "a", "a"],
                    "feature2": ["b", 1, np.nan],
                    "feature3": ["a", "a", "a"],
                },
                dtype="category",
            ),
            0.9,
            1,
        ),
    ),
)
def test_get_number_of_almost_duplicated_columns(
    dataset: pd.DataFrame, threshold: float, expected_almost_constant: int
) -> None:
    assert get_number_of_almost_duplicated_columns(dataset, threshold) == expected_almost_constant


@pytest.mark.parametrize(
    "dataset, threshold, expected_almost_constant",
    (
        (pd.DataFrame(), 0.95, 0),
        (pd.DataFrame({"feature": []}), 0.95, 0),
        (pd.DataFrame({"feature": [1, 1, 3]}), 0.95, 0),
        (pd.DataFrame({"feature1": [1, 1, 1], "feature2": [1, 1, 3]}), 0.95, 1),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1] * 10 + [2, 3],
                    "feature2": [1, 1] * 10 + [4, 5],
                }
            ),
            0.95,
            0,
        ),
        (
            pd.DataFrame(
                {
                    "feature1": [1, 1] * 10 + [2, 3],
                    "feature2": [1, 1] * 10 + [4, 5],
                }
            ),
            0.9,
            2,
        ),
    ),
)
def test_get_number_of_almost_constant_columns(
    dataset: pd.DataFrame, threshold: float, expected_almost_constant: int
) -> None:
    assert get_number_of_almost_constant_columns(dataset, threshold) == expected_almost_constant
