import numpy as np
import pandas as pd
import pytest
from pytest import approx
from scipy import stats

from evidently.legacy.calculations.stattests import z_stat_test
from evidently.legacy.calculations.stattests.kl_div import kl_div_stat_test
from evidently.legacy.calculations.stattests.utils import get_binned_data
from evidently.legacy.calculations.stattests.anderson_darling_stattest import anderson_darling_test
from evidently.legacy.calculations.stattests.chisquare_stattest import chi_stat_test
from evidently.legacy.calculations.stattests.cramer_von_mises_stattest import cramer_von_mises
from evidently.legacy.calculations.stattests.energy_distance import energy_dist_test
from evidently.legacy.calculations.stattests.epps_singleton_stattest import epps_singleton_test
from evidently.legacy.calculations.stattests.fisher_exact_stattest import fisher_exact_test
from evidently.legacy.calculations.stattests.g_stattest import g_test
from evidently.legacy.calculations.stattests.hellinger_distance import hellinger_stat_test
from evidently.legacy.calculations.stattests.mann_whitney_urank_stattest import mann_whitney_u_stat_test
from evidently.legacy.calculations.stattests.mmd_stattest import empirical_mmd
from evidently.legacy.calculations.stattests.mmd_stattest import sigma_median
from evidently.legacy.calculations.stattests.t_test import t_test
from evidently.legacy.calculations.stattests.tvd_stattest import tvd_test
from evidently.legacy.core import ColumnType


def test_freq_obs_eq_freq_exp() -> None:
    # observed and expected frequencies is the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, ColumnType.Categorical, 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, ColumnType.Categorical, 0.1) == (
        approx(0.06812, abs=1e-5),
        False,
    )


def test_freq_obs_not_eq_freq_exp() -> None:
    # observed and expected frequencies is not the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([x * 2 for x in [16, 18, 16, 14, 12, 12]])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, ColumnType.Categorical, 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, ColumnType.Categorical, 0.1) == (
        approx(0.06812, abs=1e-5),
        False,
    )


def test_cat_feature_with_nans() -> None:
    reference = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    assert chi_stat_test.func(reference, current, ColumnType.Categorical, 0.5) == (
        approx(1.0, abs=1e-5),
        False,
    )
    assert hellinger_stat_test.func(reference, current, ColumnType.Categorical, 0.1) == (
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
    current = pd.Series(["a", "b", "c"]).repeat([4, 6, 8])
    assert g_test.func(reference, current, "cat", 0.5) == (approx(0.8176, abs=1e-3), False)


def test_cramer_von_mises() -> None:
    reference = pd.Series(stats.norm.rvs(size=100, random_state=0))
    current = pd.Series(stats.norm.rvs(size=100, random_state=1))
    assert cramer_von_mises.func(reference, current, "num", 0.001) == (approx(0.8076839, abs=1e-3), False)


def test_sigma_median_numpy_compat() -> None:
    # np.percentile dropped the 'interpolation' kwarg in NumPy 2.4 (replaced by 'method').
    # This test ensures sigma_median does not raise TypeError on NumPy >= 2.4.
    dist = np.array([[0.0, 1.0, 4.0], [1.0, 0.0, 1.0], [4.0, 1.0, 0.0]])
    result = sigma_median(dist)
    assert result == approx((0.5 * 1.0) ** 0.5, abs=1e-9)


@pytest.mark.parametrize(
    "reference, current, threshold, expected_pvalue, drift_detected",
    (
        (pd.Series([1, 1, 1, 1, 1] * 5, dtype="float"), pd.Series([0, 0, 0, 0, 0] * 5, dtype="float"), 0.1, 0, True),
        (
            pd.Series([1, 0, 1, 0, 1] * 5, dtype="float"),
            pd.Series([1, 0, 1, 0, 1] * 5, dtype="float"),
            0.1,
            0.955,
            False,
        ),
        (pd.Series([1, 1, 1, 1, 1] * 5, dtype="float"), pd.Series([0, 0, 0, 0, 0] * 5, dtype="float"), 0.1, 0, True),
        (pd.Series([1, 1, 1, 1, 1] * 5, dtype="float"), pd.Series([1, 1, 1, 1, 1] * 5, dtype="float"), 0.1, 1, False),
        (pd.Series([1.1, 0.2, 2.1, 0, 1]), pd.Series([1, 0, 2, 0, 1]), 0.1, 0.96, False),
        (pd.Series(np.random.normal(0, 0.5, 100)), pd.Series(np.random.normal(0, 0.1, 100)), 0.1, 0, True),
        # (pd.Series(np.random.normal(0, 0.5, 100)), pd.Series(np.random.normal(0, 0.9, 100)), 0.1, 0, True),
    ),
)
def test_empirical_mmd(reference, current, threshold, expected_pvalue, drift_detected) -> None:
    np.random.seed(0)
    assert empirical_mmd.func(reference, current, "num", threshold) == (
        approx(expected_pvalue, abs=1e-1),
        drift_detected,
    )


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
            pd.Series(["a", "b", "b", "a", "a", "b"] * 15),
            pd.Series(["b", "b", "a", "b", "b", "a"] * 15),
            0.1,
            approx(0.033, abs=1e-3),
            True,
        ),
        (
            pd.Series(["a", "b", "b", "a", "a", "b"]),
            pd.Series(["a", "a", "a", "a", "a", "a"]),
            0.1,
            approx(0.181, abs=1e-3),
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
            pd.Series(["a", "b", "b", "b", "a", "b"]),
            pd.Series(["b", "b", "b", "a", "b", "a"]),
            0.1,
            approx(1.0, abs=1e-3),
            False,
        ),
        (
            pd.Series(["a", "a", "a", "a", "a", "a"]),
            pd.Series(["b", "b", "b", "b", "b", "b"]),
            0.1,
            approx(0.0021, abs=1e-3),
            True,
        ),
        (
            pd.Series(["a", "a", "a", "b", "b"] * 30),
            pd.Series(["b", "b", "b", "a", "a"] * 30),
            0.1,
            approx(0.00078, abs=1e-3),
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
        ValueError, match="Expects binary data for both reference and current, but found unique categories > 2"
    ):
        fisher_exact_test.func(reference, current, "cat", 0.1)


def test_mann_whitney() -> None:
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert mann_whitney_u_stat_test.func(reference, current, "num", 0.05) == (approx(0.481, abs=1e-2), False)


@pytest.mark.parametrize(
    "reference, current, threshold, pvalue, drift_detected",
    (
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8]),
            0.1,
            approx(0.928, abs=1e-3),
            False,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([10, 10, 24, 24, 10, 10]),
            0.1,
            approx(0.085, abs=1e-3),
            True,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([0, 0, 0, 0, 0, 88]),
            0.1,
            approx(0.0, abs=1e-3),
            True,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            0.1,
            approx(1.0, abs=1e-3),
            False,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12]),
            pd.Series([1, 2, 3, 4, 5, 6]).repeat([10, 24, 12, 16, 8, 16]),
            0.5,
            approx(0.309, abs=1e-3),
            True,
        ),
    ),
)
def test_tvd_stattest(reference, current, threshold, pvalue, drift_detected) -> None:
    assert tvd_test.func(reference, current, "cat", threshold) == (pvalue, drift_detected)


def test_energy_distance() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    current = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    assert energy_dist_test.func(reference, current, "num", 0.1) == (approx(0, abs=1e-5), False)
    assert energy_dist_test.func(reference, current + 5, "num", 0.1) == (approx(1.9, abs=1e-1), True)


def test_epps_singleton() -> None:
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert epps_singleton_test.func(reference, current, "num", 0.05) == (approx(0.81, abs=1e-2), False)


def test_t_test() -> None:
    reference = pd.Series([38.7, 41.5, 43.8, 44.5, 45.5, 46.0, 47.7, 58.0])
    current = pd.Series([39.2, 39.3, 39.7, 41.4, 41.8, 42.9, 43.3, 45.8])
    assert t_test.func(reference, current, "num", 0.05) == (approx(0.084, abs=1e-3), False)


def test_get_binned_data_fill_zero_is_dynamic() -> None:
    # Regression test for https://github.com/evidentlyai/evidently/issues/334.
    # When the minimum non-zero probability is smaller than 0.0001 the old code
    # used min/1e6 as fill, which is astronomically small and inflates KL divergence.
    # The fix uses min/10 so the fill stays proportional to the real data.
    from evidently.legacy.core import ColumnType

    # Build a categorical distribution where one bucket has a very small percent.
    # 99_999 "a" and 1 "b" → p("b") ≈ 1e-5, well below the old 0.0001 threshold.
    reference = pd.Series(["a"] * 99_999 + ["b"])
    current = pd.Series(["a"] * 99_999 + ["c"])  # "c" absent in reference, "b" absent in current

    ref_pct, cur_pct = get_binned_data(reference, current, ColumnType.Categorical, n=10)

    # All zero slots must be filled with a positive value
    assert np.all(ref_pct > 0), "reference percents must be strictly positive after fill"
    assert np.all(cur_pct > 0), "current percents must be strictly positive after fill"

    # The fill value must be strictly smaller than the smallest genuine probability
    min_genuine = min(reference.value_counts(normalize=True).min(), current.value_counts(normalize=True).min())
    fill_used = min(ref_pct.min(), cur_pct.min())
    assert fill_used < min_genuine, "fill value must be smaller than any real non-zero probability"

    # KL divergence must not be inflated: identical distributions should score near 0
    ref_same = pd.Series(["a"] * 50 + ["b"] * 50)
    cur_same = pd.Series(["a"] * 50 + ["b"] * 50)
    score_same, _ = kl_div_stat_test.func(ref_same, cur_same, ColumnType.Categorical, 0.1)
    assert score_same == approx(0.0, abs=1e-6), "KL of identical distributions must be ~0"


def test_get_binned_data_fill_zero_symmetric() -> None:
    # Both reference and current must receive the same fill value so that
    # KL divergence is not artificially asymmetric.
    from evidently.legacy.core import ColumnType

    reference = pd.Series(["a"] * 90 + ["b"] * 10)
    current = pd.Series(["a"] * 95 + ["c"] * 5)  # "b" zero in current, "c" zero in reference

    ref_pct, cur_pct = get_binned_data(reference, current, ColumnType.Categorical, n=10)

    # The fill value is derived from both distributions combined, so the minimum
    # of ref and current percents must be identical.
    assert ref_pct.min() == approx(cur_pct.min(), rel=1e-9), "fill value must be identical for ref and current"
