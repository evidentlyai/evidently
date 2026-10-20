import pandas as pd
import pytest

from evidently.legacy.calculations.stattests.z_stattest import _z_stat_test
from evidently.legacy.core import ColumnType


def test_z_test_accepts_mixed_binary_category_types():
    reference = pd.Series([1, "a", 1, "a"], dtype=object)
    current = pd.Series([1, 1, 1, "a"], dtype=object)
    actual, drifted = _z_stat_test(reference, current, ColumnType.Categorical, 0.05)
    expected, expected_drift = _z_stat_test(reference.astype(str), current.astype(str), ColumnType.Categorical, 0.05)
    assert actual == pytest.approx(expected)
    assert drifted == expected_drift


def test_z_test_preserves_existing_missing_category_behavior():
    reference = pd.Series(["a", None] * 10)
    current = pd.Series(["a", "b"] * 10)
    score, drifted = _z_stat_test(reference, current, ColumnType.Categorical, 0.5)
    assert score == pytest.approx(1.0)
    assert not drifted
