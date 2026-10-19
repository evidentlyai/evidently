import numpy as np
import pandas as pd
import pytest

from evidently.legacy.core import ColumnType
from evidently.legacy.calculations.stattests import (
    psi_stat_test,
    kl_div_stat_test,
    jensenshannon_stat_test,
    hellinger_stat_test,
)


@pytest.mark.parametrize(
    "stattest",
    [psi_stat_test, kl_div_stat_test, jensenshannon_stat_test, hellinger_stat_test],
)
def test_stattests_empty_series_handling(stattest):
    empty_s = pd.Series([], dtype=float)
    valid_s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])

    # Test empty reference
    res1 = stattest.func(empty_s, valid_s, ColumnType.Numerical, 0.1)
    assert np.isnan(res1[0])
    assert res1[1] is False

    # Test empty current
    res2 = stattest.func(valid_s, empty_s, ColumnType.Numerical, 0.1)
    assert np.isnan(res2[0])
    assert res2[1] is False

    # Test both empty
    res3 = stattest.func(empty_s, empty_s, ColumnType.Numerical, 0.1)
    assert np.isnan(res3[0])
    assert res3[1] is False
