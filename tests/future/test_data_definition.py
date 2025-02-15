import datetime
import random

import pandas as pd
import pytest

from evidently import ColumnType
from evidently.future.datasets import Dataset
from evidently.future.datasets import infer_column_type


@pytest.mark.parametrize(
    "data,expected",
    [
        (pd.Series(["a", "b", "a", "b", "a"]), ColumnType.Categorical),
        (pd.Series([0.1, 0.2, 0.3, 0.4, 0.5]), ColumnType.Numerical),
        (pd.Series([0.1, 0.1, 0.2, 0.2, 0.2]), ColumnType.Numerical),
        (pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), ColumnType.Numerical),
        (pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]), ColumnType.Categorical),
        (pd.Series([True, False, True, False, True, False]), ColumnType.Categorical),
        (pd.Series([datetime.datetime.now(), datetime.datetime.now()]), ColumnType.Datetime),
        (pd.Series(["a", "b", "c", "d", "e", "f", "g"]), ColumnType.Text),
        (pd.Categorical(["a", "b", "c", "d", "e", "f", "g"]), ColumnType.Categorical),
    ],
)
def test_infer_column_type(data: pd.Series, expected: ColumnType):
    assert infer_column_type(data) == expected


def test_data_definition():
    data = pd.DataFrame(
        data=dict(
            num_1=pd.Series([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]),
            num_2=pd.Series([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
            num_3=pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            cat_1=pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1]),
            cat_2=pd.Series(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "a"]),
            cat_3=pd.Series(random.choices([True, False], k=11)),
            datetime=pd.Series([datetime.datetime.now()] * 11),
            text_1=pd.Series(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]),
            text_2=pd.Series(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "f"]),
        )
    )
    dataset = Dataset.from_pandas(data)
    assert dataset.data_definition.get_column_type("num_1") == ColumnType.Numerical
    assert dataset.data_definition.get_column_type("num_2") == ColumnType.Numerical
    assert dataset.data_definition.get_column_type("num_3") == ColumnType.Numerical
    assert dataset.data_definition.get_column_type("cat_1") == ColumnType.Categorical
    assert dataset.data_definition.get_column_type("cat_2") == ColumnType.Categorical
    assert dataset.data_definition.get_column_type("cat_3") == ColumnType.Categorical
    assert dataset.data_definition.get_column_type("datetime") == ColumnType.Date
    assert dataset.data_definition.get_column_type("text_1") == ColumnType.Text
    assert dataset.data_definition.get_column_type("text_2") == ColumnType.Text
