import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.calculations.stattests import z_stat_test
from evidently.calculations.stattests.anderson_darling_stattest import anderson_darling_test
from evidently.calculations.stattests.chisquare_stattest import chi_stat_test
from evidently.calculations.stattests.cramer_von_mises_stattest import cramer_von_mises
from evidently.calculations.stattests.energy_distance import energy_dist_test
from evidently.calculations.stattests.g_stattest import g_test
from evidently.calculations.stattests.hellinger_distance import hellinger_stat_test
from evidently.calculations.stattests.mann_whitney_urank_stattest import mann_whitney_u_stat_test


def test_freq_obs_eq_freq_exp() -> None:
    # observed and expected frequencies is the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, "cat", 0.1) == (
        approx(0.06812, abs=1e-5),
        False,
    )


def test_freq_obs_not_eq_freq_exp() -> None:
    # observed and expected frequencies is not the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([x * 2 for x in [16, 18, 16, 14, 12, 12]])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, "cat", 0.1) == (
        approx(0.06812, abs=1e-5),
        False,
    )


def test_cat_feature_with_nans() -> None:
    reference = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (
        approx(1.0, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, "cat", 0.1) == (
        approx(0, abs=1e-5),
        False,
    )


def test_num_features() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0, np.nan])
    current = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0, np.nan])
    assert hellinger_stat_test.func(reference, current, "num", 0.1) == (
        approx(0, abs=1e-5),
        False,
    )


def test_chi_stat_test_cat_feature() -> None:
    reference = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (
        approx(1.0, abs=1e-5),
        False,
    )


@pytest.mark.parametrize(
    "reference, current, expected_score, expected_condition_result",
    (
        (
            pd.Series(["a", "b"] * 10),
            pd.Series(["a", "b"] * 10),
            approx(1.0, abs=1e-5),
            False,
        ),
        (
            pd.Series(["a", np.nan] * 10),
            pd.Series(["a", "b"] * 10),
            approx(1.0, abs=1e-5),
            False,
        ),
    ),
)
def test_z_stat_test_cat_feature(reference, current, expected_score, expected_condition_result: bool) -> None:
    assert z_stat_test.func(reference, current, "cat", 0.5) == (
        expected_score,
        expected_condition_result,
    )


def test_anderson_darling() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    current = pd.Series([39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8])
    assert anderson_darling_test.func(reference, current, "num", 0.001) == (approx(0.0635, abs=1e-3), False)


def test_g_test() -> None:
    reference = pd.Series(["a", "b", "c"]).repeat([5, 5, 8])
    current = pd.Series(["a", "b", "c"]).repeat([4, 7, 8])
    assert g_test.func(reference, current, "cat", 0.5) == (approx(0.231, abs=1e-3), True)


def test_cramer_von_mises() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    current = pd.Series([39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8])
    assert cramer_von_mises.func(reference, current, "num", 0.001) == (approx(0.0643, abs=1e-3), False)


def test_hellinger_distance() -> None:
    reference = pd.Series([1, 1, 1, 1, 1] * 10)
    current = reference
    assert hellinger_stat_test.func(reference, current, "num", 0.1) == (
        approx(0.0, abs=1e-3),
        False,
    )
    assert hellinger_stat_test.func(reference, current, "cat", 0.1) == (
        approx(0.0, abs=1e-3),
        False,
    )


def test_mann_whitney() -> None:
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert mann_whitney_u_stat_test.func(reference, current, "num", 0.05) == (approx(0.481, abs=1e-2), False)


def test_energy_distance() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    current = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    assert energy_dist_test.func(reference, current, "num", 0.1) == (approx(0, abs=1e-5), False)
    assert energy_dist_test.func(reference, current + 5, "num", 0.1) == (approx(1.9, abs=1e-1), True)
