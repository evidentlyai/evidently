import numpy as np
import pandas as pd

import pytest

from evidently.metrics.calculations.data_quality import get_rows_count


@pytest.mark.parametrize(
    "dataset, expected_rows",
    (
        (pd.DataFrame({}), 0),
        (pd.DataFrame({"test": [1, 2, 3]}), 3),
        (pd.DataFrame({"test": [1, 2, None]}), 3),
        (pd.DataFrame({"test": [None, None, None]}), 3),
        (pd.DataFrame({"test": [np.NAN, pd.NA, 2, 0, pd.NaT], "target": [1, 0, 1, 0, 1]}), 5),
    ),
)
def test_get_rows_count(dataset: pd.DataFrame, expected_rows: int) -> None:
    assert get_rows_count(dataset) == expected_rows
