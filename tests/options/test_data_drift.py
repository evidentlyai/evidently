import pytest

from evidently.options import DataDriftOptions


@pytest.mark.parametrize("confidence,expected", [
    (0.5, {"feature1": 0.5, "feature2": 0.5}),
    ({"feature1": 0.5}, {"feature1": 0.5, "feature2": DataDriftOptions.confidence}),
    ({"feature2": 0.5}, {"feature1": DataDriftOptions.confidence, "feature2": 0.5}),
    ({}, {"feature1": DataDriftOptions.confidence, "feature2": DataDriftOptions.confidence}),
])
def test_confidence_valid(confidence, expected):
    options = DataDriftOptions(confidence=confidence)
    for feature, expected_confidence in expected.items():
        assert options.get_confidence(feature) == expected_confidence


def test_confidence_default():
    options = DataDriftOptions()
    assert options.get_confidence("feature") == DataDriftOptions.confidence


def test_confidence_invalid():
    # special check if passed totally incorrect value
    # noinspection PyTypeChecker
    options = DataDriftOptions(confidence="")
    with pytest.raises(ValueError):
        options.get_confidence("feature1")


def _default_stattest():
    pass


def _custom_stattest():
    pass


def _another_stattest():
    pass


@pytest.mark.parametrize("feature_func,expected", [
    (None, {"feature1": _default_stattest, "feature2": _default_stattest}),
    ({"feature1": _custom_stattest}, {"feature1": _custom_stattest, "feature2": _default_stattest}),
    ({"feature2": _custom_stattest}, {"feature1": _default_stattest, "feature2": _custom_stattest}),
    ({"feature2": _custom_stattest}, {"feature1": _default_stattest, "feature2": _custom_stattest}),
])
def test_stattest_function_valid(feature_func, expected):
    options = DataDriftOptions(feature_stattest_func=feature_func)
    for feature, expected_func in expected.items():
        assert options.get_feature_stattest_func(feature, _default_stattest) == expected_func


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
