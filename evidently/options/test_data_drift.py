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
