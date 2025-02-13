import datetime

import pandas as pd
import pytest

from evidently import ColumnType
from evidently.future.datasets import Dataset


@pytest.mark.parametrize(
    "column,column_type",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ColumnType.Numerical),
        (
            [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
            ],
            ColumnType.Categorical,
        ),
        ([1.1, 2.1, 3.1, 4.1, 5.1, 6.1], ColumnType.Numerical),
        # ([1.1+1j,2.1+1j,3.1+1j,4.1+1j,5.1+1j,6.1+1j], ColumnType.Numerical),  # not supported
        ([True, True, False, False], ColumnType.Categorical),
        (pd.Categorical(["A", "B", "C", "A"]), ColumnType.Categorical),
        (["a"] * 20 + ["b"] * 20, ColumnType.Text),
        (["text", "other text", "third text"], ColumnType.Text),
        ([datetime.datetime.now(), datetime.datetime.now()], ColumnType.Datetime),
    ],
)
def test_pandas_data_definition(column, column_type):
    data = pd.DataFrame({"col": column})

    dataset = Dataset.from_pandas(data)
    assert dataset.column("col").type == column_type
