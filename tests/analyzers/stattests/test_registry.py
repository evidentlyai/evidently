import pytest

from evidently.analyzers.stattests import ks_stat_test, chi_stat_test, z_stat_test
from evidently.analyzers.stattests.registry import get_stattest, StatTestInvalidFeatureTypeError, \
    StatTestNotFoundError


def _custom_stattest():
    pass


@pytest.mark.parametrize(
    "stattest_func, feature_type, expected_name, expected_func",
    [
        (_custom_stattest, "num", "custom function '_custom_stattest'", _custom_stattest),
        ("ks", "num", "K-S (p_value)", ks_stat_test.func),
        ("z", "cat", "Z-test (p_value)", z_stat_test.func),
        ("chisquare", "cat", "chi-square (p_value)", chi_stat_test.func),
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
