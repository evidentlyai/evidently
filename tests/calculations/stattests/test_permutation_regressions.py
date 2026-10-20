import numpy as np
import pandas as pd

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
