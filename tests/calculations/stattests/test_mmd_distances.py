import numpy as np
import pytest

from evidently.legacy.calculations.stattests.mmd_stattest import rbf
from evidently.legacy.calculations.stattests.mmd_stattest import squared_paired_dist


def test_squared_distances_do_not_overflow_integer_samples():
    x = np.array([[10_000_000_000]], dtype=np.int64)
    y = np.array([[0]], dtype=np.int64)
    assert squared_paired_dist(x, y)[0, 0] == pytest.approx(1e20)


def test_squared_distances_avoid_cancellation_for_close_large_values():
    x = np.array([[1690525.703800356]])
    y = np.array([[1690525.713800356]])
    expected = float((x[0, 0] - y[0, 0]) ** 2)
    distance = squared_paired_dist(x, y)[0, 0]
    assert distance == pytest.approx(expected, rel=1e-12)
    kernel, _ = rbf(x, y, pass_sigma=1.0)
    assert 0 <= kernel[0, 0] <= 1


def test_squared_distances_reduce_all_feature_dimensions():
    x = np.array([[1.0, 2.0], [3.0, 4.0]])
    y = np.array([[5.0, 6.0], [7.0, 8.0], [9.0, 10.0]])
    expected = np.array([[32.0, 72.0, 128.0], [8.0, 32.0, 72.0]])
    np.testing.assert_allclose(squared_paired_dist(x, y), expected)
