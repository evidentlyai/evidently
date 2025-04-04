import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.stattests.tvd_stattest import _total_variation_distance
from evidently.legacy.calculations.stattests.utils import generate_fisher2x2_contingency_table
from evidently.legacy.calculations.stattests.utils import get_unique_not_nan_values_list_from_series
from evidently.legacy.calculations.stattests.utils import permutation_test


@pytest.mark.parametrize(
    "current_data, reference_data, expected_list",
    (
        (pd.Series([1, 2, 3, 3, 5]), pd.Series([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5]),
        (pd.Series([1, 2, 3, 4]), pd.Series([5, 5]), [1, 2, 3, 4, 5]),
        (pd.Series(["a", "b", "a", "c"]), pd.Series(["d", "e"]), ["b", "d", "e", "c", "a"]),
        (pd.Series(["a", None, "a", np.nan]), pd.Series([4, 5]), [4, 5, "a"]),
        (pd.Series([pd.NA, pd.NaT, np.nan]), pd.Series([pd.NA, pd.NaT, np.nan]), []),
    ),
)
def test_get_unique_not_nan_values_list_from_series(current_data: pd.Series, reference_data: pd.Series, expected_list):
    assert set(
        get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
    ) == set(expected_list)


@pytest.mark.parametrize(
    "reference, current, observed, test_statistic_func, pvalue",
    (
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8]),
            0.0628,
            _total_variation_distance,
            0.99,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8]),
            0.204,
            _total_variation_distance,
            0.14,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([0, 0, 0, 0, 0, 88]),
            0.863,
            _total_variation_distance,
            0.0,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            0.0,
            _total_variation_distance,
            1.0,
        ),
    ),
)
def test_permutation_test(reference, current, observed, test_statistic_func, pvalue):
    assert permutation_test(reference, current, observed, test_statistic_func) == pvalue


@pytest.mark.parametrize(
    "reference_data, current_data ,expected_contingency_table",
    (
        (pd.Series([1, 0, 1, 0]), pd.Series([1, 0, 1, 0]), np.array([[2, 2], [2, 2]])),
        (pd.Series([1, 1, 1, 1]), pd.Series([0, 0, 0, 0]), np.array([[0, 4], [4, 0]])),
        (pd.Series([0, 0, 0, 0]), pd.Series([0, 0, 0, 0]), np.array([[0, 4], [0, 4]])),
        (pd.Series([1, 1, 1, 0]), pd.Series([0, 1, 1, 0]), np.array([[2, 2], [3, 1]])),
    ),
)
def test_generate_fisher2x2_contingency_table(
    current_data: pd.Series, reference_data: pd.Series, expected_contingency_table: np.ndarray
):
    assert (generate_fisher2x2_contingency_table(reference_data, current_data) == expected_contingency_table).all()


@pytest.mark.parametrize(
    "reference_data, current_data",
    (
        (pd.Series([1, 0, 1]), pd.Series([1, 0, 1, 0])),
        (pd.Series([1, 1, 1, 1]), pd.Series([0])),
    ),
)
def test_input_data_length_check_generate_fisher2x2_contingency_table(
    reference_data: pd.Series, current_data: pd.Series
):
    with pytest.raises(
        ValueError,
        match="reference_data and current_data are not of equal length, please ensure that they are of equal length",
    ):
        generate_fisher2x2_contingency_table(current_data, reference_data)
