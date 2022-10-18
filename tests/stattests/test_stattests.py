import numpy as np
import pandas as pd
import pytest
from pytest import approx

from evidently.calculations.stattests import z_stat_test
from evidently.calculations.stattests.anderson_darling_stattest import anderson_darling_test
from evidently.calculations.stattests.chisquare_stattest import chi_stat_test
from evidently.calculations.stattests.cramer_von_mises_stattest import cramer_von_mises
from evidently.calculations.stattests.fisher_exact_stattest import fisher_exact_test
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


@pytest.mark.parametrize(
    "reference, current, threshold, expected_pvalue, drift_detected",
    (
        (
            pd.Series(["a", "b", "b", "a", "a", "b"]),
            pd.Series(["b", "b", "a", "b", "b", "a"]),
            0.1,
            approx(0.40, abs=1e-3),
            False,
        ),
        (
            pd.Series(["a", "b", "b", "a", "a", "b"]),
            pd.Series(["a", "a", "a", "a", "a", "a"]),
            0.1,
            approx(1.0, abs=1e-3),
            False,
        ),
        (
            pd.Series(["a", "a", "a", "a", "a", "a"]),
            pd.Series(["a", "a", "a", "a", "a", "a"]),
            0.1,
            approx(1.0, abs=1e-3),
            False,
        ),
        (
            pd.Series(["a", "b", "a", "b", "a", "b"]),
            pd.Series(["b", "a", "b", "a", "b", "a"]),
            0.15,
            approx(0.10, abs=1e-3),
            True,
        ),
    ),
)
def test_pvalue_fisher_exact(
    reference: pd.Series, current: pd.Series, threshold: float, expected_pvalue: float, drift_detected: bool
) -> None:
    assert fisher_exact_test.func(reference, current, "cat", threshold) == (
        approx(expected_pvalue, abs=1e-3),
        drift_detected,
    )


@pytest.mark.parametrize(
    "reference, current",
    (
        (
            pd.Series(["a", np.nan, "b", "a", "a", "b"]),
            pd.Series(["b", "b", "a", "b", "b", "a"]),
        ),
        (
            pd.Series(["a", np.nan, "a", "a", "b"]),
            pd.Series(["a", "a", "a", "a", np.nan, "a"]),
        ),
        (pd.Series([np.inf, np.nan, np.nan, "a", "b", "a"]), pd.Series(["a", "a", np.inf, "a", "a", "b"])),
        (pd.Series([-np.inf, "b", np.nan, "b", "a", "b"]), pd.Series(["b", np.inf, "b", "a", "b", "a"])),
    ),
)
def test_for_null_fisher_exact(reference: pd.Series, current: pd.Series) -> None:
    with pytest.raises(
        ValueError,
        match="Null or inf values found in either reference_data or current_data. Please ensure that no null or inf values are present",
    ):
        fisher_exact_test.func(reference, current, "cat", 0.1)


@pytest.mark.parametrize(
    "reference, current,",
    (
        (
            pd.Series(["a", "c", "a", "a", "a", "b"]),
            pd.Series(["b", "b", "a", "b", "b", "a"]),
        ),
        (
            pd.Series(["a", 1, "a", 3, "b", "m"]),
            pd.Series(["a", "a", 2, "a", "b", "a"]),
        ),
    ),
)
def test_for_multiple_categories_fisher_exact(reference: pd.Series, current: pd.Series) -> None:
    with pytest.raises(
        ValueError,
        match="Expects binary data for both reference and current, but found unique categories > 2",
    ):
        fisher_exact_test.func(reference, current, "cat", 0.1)


def test_mann_whitney() -> None:
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert mann_whitney_u_stat_test.func(reference, current, "num", 0.05) == (approx(0.481, abs=1e-2), False)
