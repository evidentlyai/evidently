import numpy as np
import pytest

from evidently.legacy.calculations.stattests.mmd_stattest import squared_paired_dist


def test_squared_distances_do_not_overflow_integer_samples():
    x = np.array([[10_000_000_000]], dtype=np.int64)
    y = np.array([[0]], dtype=np.int64)
    assert squared_paired_dist(x, y)[0, 0] == pytest.approx(1e20)
