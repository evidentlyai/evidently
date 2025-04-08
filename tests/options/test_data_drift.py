import pytest
from numpy.ma.testutils import approx

from evidently.legacy.options.data_drift import DataDriftOptions


@pytest.mark.parametrize(
    "confidence,expected",
    [
        (0.1, {"feature1": 0.9, "feature2": 0.9}),
        ({"feature1": 0.1}, {"feature1": 0.9, "feature2": None}),
        ({"feature2": 0.1}, {"feature1": None, "feature2": 0.9}),
        ({}, {"feature1": None, "feature2": None}),
    ],
)
def test_confidence_threshold_valid(confidence, expected):
    options = DataDriftOptions(confidence=confidence)
    for feature, expected_threshold in expected.items():
        assert approx(options.get_threshold(feature, "num"), expected_threshold)


@pytest.mark.parametrize(
    "threshold,expected",
    [
        (0.1, {"feature1": 0.1, "feature2": 0.1}),
        ({"feature1": 0.1}, {"feature1": 0.1, "feature2": None}),
        ({"feature2": 0.1}, {"feature1": None, "feature2": 0.1}),
        ({}, {"feature1": None, "feature2": None}),
    ],
)
def test_threshold_valid(threshold, expected):
    options = DataDriftOptions(threshold=threshold)
    for feature, expected_threshold in expected.items():
        assert approx(options.get_threshold(feature, "num"), expected_threshold)


def test_threshold_default():
    options = DataDriftOptions()
    assert options.get_threshold("feature", "num") is None


def _default_stattest():
    pass


def _custom_stattest():
    pass


def _another_stattest():
    pass


@pytest.mark.parametrize(
    "feature_func,expected",
    [
        (None, {"feature1": None, "feature2": None}),
        ("st1", {"feature1": "st1", "feature2": "st1"}),
        ({"feature1": _custom_stattest}, {"feature1": _custom_stattest, "feature2": None}),
        ({"feature2": _custom_stattest}, {"feature1": None, "feature2": _custom_stattest}),
        (
            {"feature1": _another_stattest, "feature2": _custom_stattest},
            {"feature1": _another_stattest, "feature2": _custom_stattest},
        ),
        ({"feature1": "st1"}, {"feature1": "st1", "feature2": None}),
        ({"feature2": "st2"}, {"feature1": None, "feature2": "st2"}),
        ({"feature1": "st1", "feature2": "st2"}, {"feature1": "st1", "feature2": "st2"}),
        ({"feature1": _another_stattest, "feature2": "st2"}, {"feature1": _another_stattest, "feature2": "st2"}),
    ],
)
def test_stattest_function_valid(feature_func, expected):
    options = DataDriftOptions(feature_stattest_func=feature_func)
    for feature, expected_func in expected.items():
        assert options.get_feature_stattest_func(feature, "cat") == expected_func


@pytest.mark.parametrize(
    "global_st,cat_st,num_st,per_feature_st,expected",
    [
        (None, None, None, None, {"cat1": None, "cat2": None, "num1": None, "num2": None}),
        ("st1", None, None, None, {"cat1": "st1", "cat2": "st1", "num1": "st1", "num2": "st1"}),
        (None, None, None, {"cat1": "st1"}, {"cat1": "st1", "cat2": None, "num1": None, "num2": None}),
        (
            None,
            None,
            None,
            {"cat2": _custom_stattest},
            {"cat1": None, "cat2": _custom_stattest, "num1": None, "num2": None},
        ),
        (
            None,
            None,
            None,
            {"cat1": _custom_stattest, "num1": _another_stattest},
            {"cat1": _custom_stattest, "cat2": None, "num1": _another_stattest, "num2": None},
        ),
        (None, "st1", None, None, {"cat1": "st1", "cat2": "st1", "num1": None, "num2": None}),
        (
            None,
            _custom_stattest,
            None,
            None,
            {"cat1": _custom_stattest, "cat2": _custom_stattest, "num1": None, "num2": None},
        ),
        (
            None,
            None,
            _custom_stattest,
            None,
            {"cat1": None, "cat2": None, "num1": _custom_stattest, "num2": _custom_stattest},
        ),
        ("st1", "st2", None, None, {"cat1": "st2", "cat2": "st2", "num1": "st1", "num2": "st1"}),
        ("st1", None, "st2", None, {"cat1": "st1", "cat2": "st1", "num1": "st2", "num2": "st2"}),
        (
            "st1",
            None,
            None,
            {"cat2": "st2", "num2": "st2"},
            {"cat1": "st1", "cat2": "st2", "num1": "st1", "num2": "st2"},
        ),
        (
            "st1",
            "st2",
            "st3",
            {"cat2": "st4", "num2": "st5"},
            {"cat1": "st2", "cat2": "st4", "num1": "st3", "num2": "st5"},
        ),
    ],
)
def test_stattest_function_valid_v2(global_st, cat_st, num_st, per_feature_st, expected):
    features_with_types = {"cat1": "cat", "cat2": "cat", "num1": "num", "num2": "num"}
    options = DataDriftOptions(
        all_features_stattest=global_st,
        cat_features_stattest=cat_st,
        num_features_stattest=num_st,
        per_feature_stattest=per_feature_st,
    )
    for feature, expected_func in expected.items():
        assert options.get_feature_stattest_func(feature, features_with_types[feature]) == expected_func


@pytest.mark.parametrize(
    "feature_st,global_st,cat_st,num_st,per_feature_st",
    (
        [
            ("st1", "st2", None, None, None),
            ("st1", None, "st2", None, None),
            ("st1", None, None, "st2", None),
            ("st1", None, None, None, {"f1": "st2"}),
        ]
    ),
)
def test_stattest_function_deprecated(feature_st, global_st, cat_st, num_st, per_feature_st):
    options = DataDriftOptions(
        feature_stattest_func=feature_st,
        all_features_stattest=global_st,
        cat_features_stattest=cat_st,
        num_features_stattest=num_st,
        per_feature_stattest=per_feature_st,
    )
    with pytest.raises(ValueError):
        options.get_feature_stattest_func("f1", "cat")


@pytest.mark.parametrize(
    "nbinsx,expected",
    [
        (20, {"feature1": 20, "feature2": 20}),
        ({"feature1": 15}, {"feature1": 15, "feature2": DataDriftOptions.DEFAULT_NBINSX}),
        ({"feature2": 11}, {"feature1": DataDriftOptions.DEFAULT_NBINSX, "feature2": 11}),
        ({"feature1": 25, "feature2": 35}, {"feature1": 25, "feature2": 35}),
    ],
)
def test_nbinsx_valid(nbinsx, expected):
    options = DataDriftOptions(nbinsx=nbinsx)
    for feature, expected_nbinsx in expected.items():
        assert options.get_nbinsx(feature) == expected_nbinsx
