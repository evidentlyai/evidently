import numpy as np
import pytest

from evidently.legacy.utils.visualizations import histogram_bin_edges_doane


@pytest.mark.parametrize(
    "data",
    [
        np.full(105, -1.11188012),
        np.full(62, 1.20406802),
        np.array([5] * 10),
    ],
)
def test_doane_constant_data_matches_numpy(data):
    edges = histogram_bin_edges_doane(data)
    expected = np.histogram_bin_edges(data, bins="doane")
    assert len(edges) - 1 == 1
    assert np.allclose(edges, expected)


def test_doane_non_constant_data_matches_numpy():
    rng = np.random.RandomState(0)
    data = rng.exponential(size=500)
    assert np.allclose(
        histogram_bin_edges_doane(data),
        np.histogram_bin_edges(data, bins="doane"),
    )
