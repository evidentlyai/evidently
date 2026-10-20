import pandas as pd
import pytest

from evidently.legacy.calculations.stattests.fisher_exact_stattest import _fisher_exact_stattest
from evidently.legacy.core import ColumnType


@pytest.mark.parametrize("reference,current", [(["a", "b"], ["b", "c"]), (["a", "b"], ["c", "d"])])
def test_fisher_rejects_more_than_two_categories_across_both_samples(reference, current):
    with pytest.raises(ValueError, match="unique categories > 2"):
        _fisher_exact_stattest(pd.Series(reference), pd.Series(current), ColumnType.Categorical, 0.05)
