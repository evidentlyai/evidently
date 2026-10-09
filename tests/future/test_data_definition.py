import datetime
import json
import random

import pandas as pd
import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import DEFAULT_TRACE_LINK_COLUMN
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import ServiceColumns
from evidently.core.datasets import infer_column_type
from evidently.legacy.core import ColumnType


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
        (pd.Series(pd.date_range("2025-01-01", periods=2, tz="UTC")), ColumnType.Datetime),
        (pd.Series([1, 2, 1], dtype="category"), ColumnType.Categorical),
        (pd.Series([True, False], dtype="category"), ColumnType.Categorical),
        (pd.Series(["a", "b", "a", "b"], dtype="string"), ColumnType.Categorical),
        (pd.Series(["a", "b", "c"], dtype="string"), ColumnType.Text),
        (pd.Series([[1], [2]], dtype="object"), ColumnType.List),
        (pd.Series([None, None], dtype="object"), ColumnType.Unknown),
        (pd.Series([1, 2], dtype="object"), ColumnType.Unknown),
        (pd.Series([1 + 2j, 3 + 4j]), ColumnType.Unknown),
        (pd.Series([1, 2], dtype="uint64"), ColumnType.Unknown),
        (pd.Series([1, 2], dtype="UInt64"), ColumnType.Unknown),
        (pd.Series([1.0, 0.0], dtype="Sparse[float64]"), ColumnType.Unknown),
        (pd.Series([1, 0], dtype="Sparse[int64]"), ColumnType.Unknown),
        (pd.Series([True, False], dtype="Sparse[bool]"), ColumnType.Unknown),
    ],
)
def test_infer_column_type(data: pd.Series, expected: ColumnType):
    assert infer_column_type(data) == expected


@pytest.mark.parametrize("dtype", ["Float32", "Float64"])
@pytest.mark.parametrize("values", [[0.1, 0.2], [0.1, None], [None, None], []])
def test_infer_nullable_float_column_type(dtype, values):
    assert infer_column_type(pd.Series(values, dtype=dtype)) == ColumnType.Numerical


@pytest.mark.parametrize("dtype", ["Int8", "Int16", "Int32", "Int64"])
@pytest.mark.parametrize(
    "values,expected",
    [
        (list(range(10)), ColumnType.Categorical),
        (list(range(11)), ColumnType.Numerical),
        (list(range(10)) + [None], ColumnType.Categorical),
        (list(range(11)) + [None], ColumnType.Numerical),
        ([None, None], ColumnType.Categorical),
        ([], ColumnType.Categorical),
    ],
)
def test_infer_nullable_integer_column_type(dtype, values, expected):
    assert infer_column_type(pd.Series(values, dtype=dtype)) == expected


@pytest.mark.parametrize("values", [[True, False], [True, None], [None, None], []])
def test_infer_nullable_boolean_column_type(values):
    assert infer_column_type(pd.Series(values, dtype="boolean")) == ColumnType.Categorical


def test_data_definition_convert_dtypes():
    data = pd.DataFrame(
        {
            "amount": [i + 0.5 for i in range(12)],
            "count": list(range(12)),
            "category": [0, 1] * 6,
            "flag": [True, False] * 6,
        }
    )
    expected = Dataset.from_pandas(data).data_definition
    actual = Dataset.from_pandas(data.convert_dtypes()).data_definition
    assert actual == expected


@pytest.mark.parametrize(
    "definition,numerical,categorical,datetime_cols,text,service_columns",
    [
        (
            None,
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(numerical_columns=["num_1"]),
            ("num_1",),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(categorical_columns=["cat_1"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(text_columns=["text_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_2",),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(datetime_columns=["datetime_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(timestamp="datetime"),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(numerical_columns=[]),
            tuple(),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(id_column="num_1"),
            ("num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(categorical_columns=["num_3"]),
            ("num_1", "num_2"),
            ("num_3",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link=DEFAULT_TRACE_LINK_COLUMN),
        ),
        (
            DataDefinition(service_columns=ServiceColumns(trace_link="another_trace_link")),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2", "_evidently_trace_link"),
            ServiceColumns(trace_link="another_trace_link"),
        ),
    ],
)
def test_data_definition(definition, numerical, categorical, datetime_cols, text, service_columns):
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
            _evidently_trace_link=pd.Series(["a", "b", "c", "d", "e", "a", "b", "c", "d", "e", "f"]),
        )
    )
    dataset = Dataset.from_pandas(data, data_definition=definition)
    assert set(numerical) == set(dataset.data_definition.get_numerical_columns())
    assert set(categorical) == set(dataset.data_definition.get_categorical_columns())
    assert set(datetime_cols) == set(dataset.data_definition.get_datetime_columns())
    assert set(text) == set(dataset.data_definition.get_text_columns())
    assert service_columns == dataset.data_definition.service_columns


@pytest.mark.parametrize(
    "definition,numerical,categorical,datetime_cols,text,service_columns",
    [
        (
            None,
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(numerical_columns=["num_1"]),
            ("num_1",),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(categorical_columns=["cat_1"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(text_columns=["text_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_2",),
            None,
        ),
        (
            DataDefinition(datetime_columns=["datetime_2"]),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(timestamp="datetime"),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime_2",),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(numerical_columns=[]),
            tuple(),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(id_column="num_1"),
            ("num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(categorical_columns=["num_3"]),
            ("num_1", "num_2"),
            ("num_3",),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            None,
        ),
        (
            DataDefinition(service_columns=ServiceColumns(trace_link="another_trace_link")),
            ("num_1", "num_2", "num_3"),
            ("cat_1", "cat_2", "cat_3"),
            ("datetime", "datetime_2"),
            ("text_1", "text_2"),
            ServiceColumns(trace_link="another_trace_link"),
        ),
    ],
)
def test_data_definition_without_service(definition, numerical, categorical, datetime_cols, text, service_columns):
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
    assert service_columns == dataset.data_definition.service_columns


def test_data_definition_serialization():
    data_definition = DataDefinition(text_columns=["text_2"])
    parsed = parse_obj_as(DataDefinition, json.loads(data_definition.json()))
    assert parsed == data_definition


def test_data_definition_serialization_empty():
    data_definition = DataDefinition()
    parsed = parse_obj_as(DataDefinition, {})
    assert parsed == data_definition
