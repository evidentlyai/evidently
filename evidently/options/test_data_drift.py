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


@pytest.mark.parametrize("func,feature_func,expected", [
    (None, None, {"feature1": _default_stattest, "feature2": _default_stattest}),
    (_custom_stattest, None, {"feature1": _custom_stattest, "feature2": _custom_stattest}),
    (None, {"feature1": _custom_stattest}, {"feature1": _custom_stattest, "feature2": _default_stattest}),
    (None, {"feature2": _custom_stattest}, {"feature1": _default_stattest, "feature2": _custom_stattest}),
    (None, {"feature2": _custom_stattest}, {"feature1": _default_stattest, "feature2": _custom_stattest}),
    (_another_stattest, {"feature2": _custom_stattest}, {"feature1": _another_stattest, "feature2": _custom_stattest}),
])
def test_stattest_function_valid(func, feature_func, expected):
    options = DataDriftOptions(stattest_func=func, feature_stattest_func=feature_func)
    for feature, expected_func in expected.items():
        assert options.get_feature_stattest_func(feature, _default_stattest) == expected_func
