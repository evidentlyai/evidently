import pytest
from numpy.ma.testutils import approx

from evidently.options import DataDriftOptions
from evidently.options.data_drift import DEFAULT_THRESHOLD


@pytest.mark.parametrize("confidence,expected", [
    (0.1, {"feature1": 0.9, "feature2": 0.9}),
    ({"feature1": 0.1}, {"feature1": 0.9, "feature2": DEFAULT_THRESHOLD}),
    ({"feature2": 0.1}, {"feature1": DEFAULT_THRESHOLD, "feature2": 0.9}),
    ({}, {"feature1": DEFAULT_THRESHOLD, "feature2": DEFAULT_THRESHOLD}),
])
def test_confidence_threshold_valid(confidence, expected):
    options = DataDriftOptions(confidence=confidence)
    for feature, expected_threshold in expected.items():
        assert approx(options.get_threshold(feature), expected_threshold)


@pytest.mark.parametrize("threshold,expected", [
    (0.1, {"feature1": 0.1, "feature2": 0.1}),
    ({"feature1": 0.1}, {"feature1": 0.1, "feature2": DEFAULT_THRESHOLD}),
    ({"feature2": 0.1}, {"feature1": DEFAULT_THRESHOLD, "feature2": 0.1}),
    ({}, {"feature1": DEFAULT_THRESHOLD, "feature2": DEFAULT_THRESHOLD}),
])
def test_threshold_valid(threshold, expected):
    options = DataDriftOptions(threshold=threshold)
    for feature, expected_threshold in expected.items():
        assert approx(options.get_threshold(feature), expected_threshold)


def test_threshold_default():
    options = DataDriftOptions()
    assert options.get_threshold("feature") == DEFAULT_THRESHOLD


def test_threshold_invalid():
    # special check if passed totally incorrect value
    # noinspection PyTypeChecker
    options = DataDriftOptions(confidence="")
    with pytest.raises(ValueError):
        options.get_threshold("feature1")


def _default_stattest():
    pass


def _custom_stattest():
    pass


def _another_stattest():
    pass


@pytest.mark.parametrize("feature_func,expected", [
    (None, {"feature1": "def_st", "feature2": "def_st"}),
    ("st1", {"feature1": "st1", "feature2": "st1"}),
    ({"feature1": _custom_stattest}, {"feature1": _custom_stattest, "feature2": "def_st"}),
    ({"feature2": _custom_stattest}, {"feature1": "def_st", "feature2": _custom_stattest}),
    ({"feature1": _another_stattest, "feature2": _custom_stattest},
     {"feature1": _another_stattest, "feature2": _custom_stattest}),
    ({"feature1": "st1"}, {"feature1": "st1", "feature2": "def_st"}),
    ({"feature2": "st2"}, {"feature1": "def_st", "feature2": "st2"}),
    ({"feature1": "st1", "feature2": "st2"}, {"feature1": "st1", "feature2": "st2"}),
    ({"feature1": _another_stattest, "feature2": "st2"}, {"feature1": _another_stattest, "feature2": "st2"}),
])
def test_stattest_function_valid(feature_func, expected):
    options = DataDriftOptions(feature_stattest_func=feature_func)
    for feature, expected_func in expected.items():
        assert options.get_feature_stattest_func(feature, "def_st") == expected_func


@pytest.mark.parametrize("nbinsx,expected", [
    (20, {"feature1": 20, "feature2": 20}),
    ({"feature1": 15}, {"feature1": 15, "feature2": DataDriftOptions.nbinsx}),
    ({"feature2": 11}, {"feature1": DataDriftOptions.nbinsx, "feature2": 11}),
    ({"feature1": 25, "feature2": 35}, {"feature1": 25, "feature2": 35})
])
def test_nbinsx_valid(nbinsx, expected):
    options = DataDriftOptions(nbinsx=nbinsx)
    for feature, expected_nbinsx in expected.items():
        assert options.get_nbinsx(feature) == expected_nbinsx


def test_nbinsx_invalid():
    # special check if passed totally incorrect value
    # noinspection PyTypeChecker
    options = DataDriftOptions(nbinsx="")
    with pytest.raises(ValueError):
        options.get_nbinsx("feature1")
