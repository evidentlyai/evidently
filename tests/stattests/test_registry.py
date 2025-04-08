from typing import Tuple

import pandas as pd
import pytest

from evidently.legacy.calculation_engine.python_engine import PythonEngine
from evidently.legacy.calculations.stattests import StatTest
from evidently.legacy.calculations.stattests import chi_stat_test
from evidently.legacy.calculations.stattests import get_stattest
from evidently.legacy.calculations.stattests import jensenshannon_stat_test
from evidently.legacy.calculations.stattests import kl_div_stat_test
from evidently.legacy.calculations.stattests import ks_stat_test
from evidently.legacy.calculations.stattests import psi_stat_test
from evidently.legacy.calculations.stattests import wasserstein_stat_test
from evidently.legacy.calculations.stattests import z_stat_test
from evidently.legacy.calculations.stattests.registry import StatTestInvalidFeatureTypeError
from evidently.legacy.calculations.stattests.registry import StatTestNotFoundError
from evidently.legacy.calculations.stattests.registry import add_stattest_impl
from evidently.legacy.calculations.stattests.registry import create_impl_wrapper
from evidently.legacy.core import ColumnType


def _custom_stattest(
    reference_data: pd.Series, current_data: pd.Series, feature_type: ColumnType, _: float
) -> Tuple[float, bool]:
    pass


custom_stattest = StatTest("", "custom function '_custom_stattest'", [])

add_stattest_impl(custom_stattest, PythonEngine, create_impl_wrapper(_custom_stattest))


@pytest.mark.parametrize(
    "stattest_func, feature_type, expected",
    [
        (_custom_stattest, "num", custom_stattest),
        ("ks", "num", ks_stat_test),
        ("z", "cat", z_stat_test),
        ("chisquare", "cat", chi_stat_test),
        ("jensenshannon", "num", jensenshannon_stat_test),
        ("kl_div", "num", kl_div_stat_test),
        ("psi", "num", psi_stat_test),
        ("wasserstein", "num", wasserstein_stat_test),
    ],
)
def test_get_stattest_valid_resolve(stattest_func, feature_type, expected):
    test = get_stattest(pd.Series(dtype="float64"), pd.Series(dtype="float64"), feature_type, stattest_func)
    assert test.display_name == expected.display_name
    assert test.func == expected.func


@pytest.mark.parametrize(
    "reference_data, current_data, feature_type, expected",
    [
        (pd.Series([1.0] * 10), pd.Series([1.0] * 10), "num", z_stat_test),
        (
            pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            "num",
            ks_stat_test,
        ),
        (
            pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] * 1000),
            pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] * 1000),
            "num",
            wasserstein_stat_test,
        ),
        (pd.Series([1, 2, 3, 4, 5] * 1000), pd.Series([1, 2, 3, 4, 5] * 1000), "num", jensenshannon_stat_test),
        (pd.Series(["a", "b", "c"] * 10), pd.Series(["a", "b", "c"] * 10), "cat", chi_stat_test),
        (pd.Series(["a", "b"] * 10), pd.Series(["a", "b"] * 10), "cat", z_stat_test),
        (pd.Series(["a", "b"] * 10000), pd.Series(["a", "b"] * 10000), "cat", jensenshannon_stat_test),
    ],
)
def test_get_default_stattest(reference_data, current_data, feature_type, expected):
    test = get_stattest(reference_data, current_data, feature_type, None)
    assert test == expected


@pytest.mark.parametrize(
    "stattest_func, feature_type",
    [
        ("ks", "cat"),
        ("z", "num"),
        ("chisquare", "num"),
    ],
)
def test_get_stattest_invalid_type(stattest_func, feature_type):
    with pytest.raises(StatTestInvalidFeatureTypeError):
        get_stattest(pd.Series(dtype="float64"), pd.Series(dtype="float64"), feature_type, stattest_func)


@pytest.mark.parametrize(
    "stattest_func, feature_type",
    [
        ("missing_stattest", "cat"),
        ("missing_stattest", "num"),
    ],
)
def test_get_stattest_missing_stattest(stattest_func, feature_type):
    with pytest.raises(StatTestNotFoundError):
        get_stattest(pd.Series(dtype="float64"), pd.Series(dtype="float64"), feature_type, stattest_func)


@pytest.mark.parametrize(
    "stat_test, override_threshold, expected_threshold",
    [
        (StatTest("", "", []), None, 0.05),
        (StatTest("", "", [], 0.1), None, 0.1),
        (StatTest("", "", []), 0.5, 0.5),
    ],
)
def test_stattest_default_threshold(stat_test, override_threshold, expected_threshold):
    add_stattest_impl(stat_test, PythonEngine, create_impl_wrapper(lambda rd, cd, ft, thr: (thr, False)))
    result = stat_test(pd.Series(dtype="float64"), pd.Series(dtype="float64"), ColumnType.Numerical, override_threshold)
    assert result.drift_score == expected_threshold
