import pytest

from evidently.analyzers.stattests import ks_stat_test, chi_stat_test, z_stat_test
from evidently.analyzers.stattests.registry import get_stattest, stattest, StatTestInvalidFeatureTypeError, \
    StatTestNotFoundError


@stattest("test_stattest", allowed_feature_types=["cat"])
def _test_stattest():
    pass


@stattest("test_num_stattest", allowed_feature_types=["num"])
def _test_num_stattest():
    pass


def _custom_stattest():
    pass


@pytest.mark.parametrize(
    "stattest_func, feature_type, expected_name, expected_func",
    [
        (_custom_stattest, "num", "custom function _custom_stattest", _custom_stattest),
        ("ks", "num", "ks", ks_stat_test),
        ("z", "cat", "z", z_stat_test),
        ("chisquare", "cat", "chisquare", chi_stat_test),
        ("test_stattest", "cat", "test_stattest", _test_stattest),
     ])
def test_get_stattest_valid(stattest_func, feature_type, expected_name, expected_func):
    stattest_name, func = get_stattest(stattest_func, feature_type)
    assert stattest_name == expected_name
    assert func == expected_func


@pytest.mark.parametrize(
    "stattest_func, feature_type",
    [
        ("ks", "cat"),
        ("z", "num"),
        ("chisquare", "num"),
        ("test_stattest", "num"),
        ("test_num_stattest", "cat"),
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
