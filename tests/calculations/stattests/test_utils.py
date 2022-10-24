import numpy as np
import pandas as pd
import pytest

from evidently.calculations.stattests.tvd_stattest import _total_variation_distance
from evidently.calculations.stattests.utils import get_unique_not_nan_values_list_from_series
from evidently.calculations.stattests.utils import permutation_test


@pytest.mark.parametrize(
    "current_data, reference_data, expected_list",
    (
        (pd.Series([1, 2, 3, 3, 5]), pd.Series([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5]),
        (pd.Series([1, 2, 3, 4]), pd.Series([5, 5]), [1, 2, 3, 4, 5]),
        (pd.Series(["a", "b", "a", "c"]), pd.Series(["d", "e"]), ["b", "d", "e", "c", "a"]),
        (pd.Series(["a", None, "a", np.NAN]), pd.Series([4, 5]), [4, 5, "a"]),
        (pd.Series([pd.NA, pd.NaT, np.NAN]), pd.Series([pd.NA, pd.NaT, np.NAN]), []),
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
