import numpy as np
import pandas as pd
from pytest import approx

from evidently.analyzers.stattests import z_stat_test
from evidently.analyzers.stattests.chisquare_stattest import chi_stat_test


def test_freq_obs_eq_freq_exp() -> None:
    # observed and expected frequencies is the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (approx(0.67309, abs=1e-5), False)


def test_chi_stat_test_cat_feature() -> None:
    reference = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (approx(1.0, abs=1e-5), False)


def test_z_stat_test_cat_feature() -> None:
    reference = pd.Series(["a", "b"]).repeat([10, 10])
    current = pd.Series(["a", "b"]).repeat([10, 10])
    assert z_stat_test.func(reference, current, "cat", 0.5) == (approx(1.0, abs=1e-5), False)


def test_cat_feature_with_nans() -> None:
    reference = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (approx(1.0, abs=1e-5), False)


def test_freq_obs_not_eq_freq_exp() -> None:
    # observed and expected frequencies is not the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([x * 2 for x in [16, 18, 16, 14, 12, 12]])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test.func(reference, current, "cat", 0.5) == (approx(0.67309, abs=1e-5), False)
