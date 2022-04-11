import pytest

from evidently.analyzers.stattests import ks_stat_test
from evidently.analyzers.stattests import chi_stat_test
from evidently.analyzers.stattests import z_stat_test
from evidently.analyzers.stattests import jensenshannon_stat_test
from evidently.analyzers.stattests import kl_div_stat_test
from evidently.analyzers.stattests import psi_stat_test
from evidently.analyzers.stattests import wasserstein_stat_test
from evidently.analyzers.stattests.registry import get_stattest, StatTestInvalidFeatureTypeError, \
    StatTestNotFoundError


def _custom_stattest():
    pass


@pytest.mark.parametrize(
    "stattest_func, feature_type, expected_name, expected_func",
    [
        (_custom_stattest, "num", "custom function '_custom_stattest'", _custom_stattest),
        ("ks", "num", ks_stat_test.display_name, ks_stat_test.func),
        ("z", "cat", z_stat_test.display_name, z_stat_test.func),
        ("chisquare", "cat", chi_stat_test.display_name, chi_stat_test.func),
        ("jensenshannon", "num", jensenshannon_stat_test.display_name, jensenshannon_stat_test.func),
        ("kl_div", "num", kl_div_stat_test.display_name, kl_div_stat_test.func),
        ("psi", "num", psi_stat_test.display_name, psi_stat_test.func),
        ("wasserstein", "num", wasserstein_stat_test.display_name, wasserstein_stat_test.func)
     ])
def test_get_stattest_valid(stattest_func, feature_type, expected_name, expected_func):
    test = get_stattest(stattest_func, feature_type)
    assert test.display_name == expected_name
    assert test.func == expected_func


@pytest.mark.parametrize(
    "stattest_func, feature_type",
    [
        ("ks", "cat"),
        ("z", "num"),
        ("chisquare", "num"),
    ]
)
def test_get_stattest_invalid_type(stattest_func, feature_type):
    with pytest.raises(StatTestInvalidFeatureTypeError):
        get_stattest(stattest_func, feature_type)


@pytest.mark.parametrize(
    "stattest_func, feature_type",
    [
        ("missing_stattest", "cat"),
        ("missing_stattest", "num"),
    ]
)
def test_get_stattest_missing_stattest(stattest_func, feature_type):
    with pytest.raises(StatTestNotFoundError):
        get_stattest(stattest_func, feature_type)
