import numpy as np
import pandas as pd
import pytest
from scipy.stats import fisher_exact

from evidently.legacy.calculations.stattests.fisher_exact_stattest import _fisher_exact_stattest
from evidently.legacy.core import ColumnType


@pytest.mark.parametrize("reference,current", [(["a", "b"], ["b", "c"]), (["a", "b"], ["c", "d"])])
def test_fisher_rejects_more_than_two_categories_across_both_samples(reference, current):
    with pytest.raises(ValueError, match="unique categories > 2"):
        _fisher_exact_stattest(pd.Series(reference), pd.Series(current), ColumnType.Categorical, 0.05)


def test_fisher_supports_independent_samples_of_unequal_size():
    reference = pd.Series(["a"] * 8 + ["b"] * 2)
    current = pd.Series(["a"] + ["b"] * 4)
    pvalue, drifted = _fisher_exact_stattest(reference, current, ColumnType.Categorical, 0.05)
    expected = fisher_exact(np.array([[1, 4], [8, 2]])).pvalue
    assert pvalue == pytest.approx(expected)
    assert drifted == (expected < 0.05)
