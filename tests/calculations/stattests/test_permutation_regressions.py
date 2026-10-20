import numpy as np
import pandas as pd
import pytest

from evidently.legacy.calculations.stattests.utils import permutation_test


def test_permutation_preserves_global_random_state():
    reference = pd.Series([1, 2, 3])
    current = pd.Series([4, 5, 6])
    state = np.random.get_state()
    try:
        first = permutation_test(reference, current, 1.0, lambda ref, cur: ref.mean() - cur.mean())
        after = np.random.get_state()
        np.testing.assert_equal(after, state)
        assert permutation_test(reference, current, 1.0, lambda ref, cur: ref.mean() - cur.mean()) == first
    finally:
        np.random.set_state(state)


def test_two_sided_permutation_is_invariant_to_observed_sign():
    reference = pd.Series([0.0, 0.0, 0.0])
    current = pd.Series([1.0, 1.0, 1.0])

    def statistic(ref, cur):
        return ref.mean() - cur.mean()

    positive = permutation_test(reference, current, 1.0, statistic)
    negative = permutation_test(reference, current, -1.0, statistic)
    assert positive < 1.0
    assert negative == positive


@pytest.mark.parametrize("iterations", [0, -1])
def test_permutation_rejects_nonpositive_iterations(iterations):
    def statistic(ref, cur):
        pytest.fail("invalid iterations should be rejected before evaluating the statistic")

    with pytest.raises(ValueError, match="iterations must be positive"):
        permutation_test(pd.Series([1]), pd.Series([2]), 1.0, statistic, iterations=iterations)
