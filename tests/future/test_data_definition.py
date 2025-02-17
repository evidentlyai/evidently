import datetime
import random

import pandas as pd
import pytest

from evidently import ColumnType
from evidently.future.datasets import DataDefinition
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
        (pd.Series(pd.date_range("2025-01-01", periods=11, freq="D").values), ColumnType.Datetime),
    ],
)
def test_infer_column_type(data: pd.Series, expected: ColumnType):
    assert infer_column_type(data) == expected


@pytest.mark.parametrize(
    "definition,numerical,categorical,datetime_cols,text",
    [
        (
            None,
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(numerical_columns=["num_1"]),
            ("num_1",),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(categorical_columns=["cat_1"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(text_columns=["text_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_2",),
        ),
        (
            DataDefinition(datetime_columns=["datetime_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(timestamp="datetime"),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(numerical_columns=[]),
            tuple(),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(id_column="num_1"),
            ("num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
        (
            DataDefinition(categorical_columns=["num_3"]),
            ("num_1", "num_2"),
            ("num_3",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
        ),
    ],
)
def test_data_definition(definition, numerical, categorical, datetime_cols, text):
    data = pd.DataFrame(
        data=dict(
            num_1=pd.Series([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]),
            num_2=pd.Series([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
            num_3=pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            cat_1=pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1]),
            cat_2=pd.Series(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "a"]),
            cat_3=pd.Series(random.choices([True, False], k=11)),
            datetime=pd.Series([datetime.datetime.now()] * 11),
            datetime_2=pd.date_range("2025-01-01", periods=11, freq="D"),
            text_1=pd.Series(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]),
            text_2=pd.Series(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "f"]),
        )
    )
    dataset = Dataset.from_pandas(data, data_definition=definition)
    assert set(numerical) == set(dataset.data_definition.get_numerical_columns())
    assert set(categorical) == set(dataset.data_definition.get_categorical_columns())
    assert set(datetime_cols) == set(dataset.data_definition.get_datetime_columns())
    assert set(text) == set(dataset.data_definition.get_text_columns())
