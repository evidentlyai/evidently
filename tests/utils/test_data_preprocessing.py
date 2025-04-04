from datetime import datetime

import pandas as pd
import pytest

from evidently.legacy.core import ColumnType
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import NUMBER_UNIQUE_AS_CATEGORICAL
from evidently.legacy.utils.data_preprocessing import ColumnDefinition
from evidently.legacy.utils.data_preprocessing import ColumnPresenceState
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.data_preprocessing import PredictionColumns
from evidently.legacy.utils.data_preprocessing import _get_column_presence
from evidently.legacy.utils.data_preprocessing import _get_column_type
from evidently.legacy.utils.data_preprocessing import _InputData
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_get_columns():
    columns = [
        ColumnDefinition("id", ColumnType.Categorical),
        ColumnDefinition("datetime", ColumnType.Datetime),
        ColumnDefinition("target", ColumnType.Categorical),
        ColumnDefinition("predicted", ColumnType.Categorical),
        ColumnDefinition("class_1", ColumnType.Numerical),
        ColumnDefinition("class_2", ColumnType.Numerical),
        ColumnDefinition("class_3", ColumnType.Numerical),
        ColumnDefinition("column_1", ColumnType.Categorical),
        ColumnDefinition("column_2", ColumnType.Numerical),
        ColumnDefinition("column_3", ColumnType.Numerical),
        ColumnDefinition("column_4", ColumnType.Datetime),
        ColumnDefinition("column_5", ColumnType.Datetime),
        ColumnDefinition("column_6", ColumnType.Datetime),
    ]
    definition = DataDefinition(
        columns={c.column_name: c for c in columns},
        id_column=ColumnDefinition("id", ColumnType.Categorical),
        datetime_column=ColumnDefinition("datetime", ColumnType.Datetime),
        target=ColumnDefinition("target", ColumnType.Categorical),
        prediction_columns=PredictionColumns(
            predicted_values=ColumnDefinition("predicted", ColumnType.Categorical),
            prediction_probas=[
                ColumnDefinition("class_1", ColumnType.Numerical),
                ColumnDefinition("class_2", ColumnType.Numerical),
                ColumnDefinition("class_3", ColumnType.Numerical),
            ],
        ),
        task="classification",
        classification_labels=["class_1", "class_2", "class_3"],
        embeddings=None,
        reference_present=True,
        user_id=None,
        item_id=None,
        recommendations_type=None,
    )

    all_columns = [
        "id",
        "datetime",
        "target",
        "predicted",
        "class_1",
        "class_2",
        "class_3",
        "column_1",
        "column_2",
        "column_3",
        "column_4",
        "column_5",
        "column_6",
    ]
    assert all_columns == [cd.column_name for cd in definition.get_columns()]
    cat_columns = ["id", "target", "predicted", "column_1"]
    assert cat_columns == [cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Categorical)]
    num_columns = ["class_1", "class_2", "class_3", "column_2", "column_3"]
    assert num_columns == [cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Numerical)]
    dt_columns = ["datetime", "column_4", "column_5", "column_6"]
    assert dt_columns == [cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Datetime)]

    features = ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6"]
    assert features == [cd.column_name for cd in definition.get_columns(features_only=True)]
    cat_features = ["column_1"]
    assert cat_features == [
        cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Categorical, features_only=True)
    ]
    num_features = ["column_2", "column_3"]
    assert num_features == [
        cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Numerical, features_only=True)
    ]
    dt_features = ["column_4", "column_5", "column_6"]
    assert dt_features == [
        cd.column_name for cd in definition.get_columns(filter_def=ColumnType.Datetime, features_only=True)
    ]


@pytest.mark.parametrize(
    "reference,current,column_name,expected",
    [
        (None, pd.DataFrame(dict(a=[1], b=[2])), "a", ColumnPresenceState.Present),
        (None, pd.DataFrame(dict(a=[1], b=[2])), "b", ColumnPresenceState.Present),
        (None, pd.DataFrame(dict(a=[1], b=[2])), "c", ColumnPresenceState.Missing),
        (
            pd.DataFrame(dict(a=[1], c=[2])),
            pd.DataFrame(dict(a=[1], b=[2])),
            "a",
            ColumnPresenceState.Present,
        ),
        (
            pd.DataFrame(dict(a=[1], c=[2])),
            pd.DataFrame(dict(a=[1], b=[2])),
            "b",
            ColumnPresenceState.Partially,
        ),
        (
            pd.DataFrame(dict(a=[1], c=[2])),
            pd.DataFrame(dict(a=[1], b=[2])),
            "c",
            ColumnPresenceState.Partially,
        ),
        (
            pd.DataFrame(dict(a=[1], c=[2])),
            pd.DataFrame(dict(a=[1], b=[2])),
            "d",
            ColumnPresenceState.Missing,
        ),
    ],
)
def test_column_presence(reference, current, column_name, expected):
    assert _get_column_presence(column_name, _InputData(reference, current)) == expected


@pytest.mark.parametrize(
    "reference,current,column_name,expected",
    [
        (None, pd.DataFrame(dict(a=[1.0], b=[2])), "a", ColumnType.Numerical),
        (None, pd.DataFrame(dict(a=[1.0], b=[2])), "b", ColumnType.Categorical),
        (None, pd.DataFrame(dict(a=[1.0], b=["a"])), "b", ColumnType.Categorical),
        (
            None,
            pd.DataFrame(dict(a=[1.0], b=["a"], c=[datetime(2000, 1, 1)])),
            "c",
            ColumnType.Datetime,
        ),
        (pd.DataFrame(), pd.DataFrame(dict(a=[1.0], b=[2])), "a", ColumnType.Numerical),
        (
            pd.DataFrame(),
            pd.DataFrame(dict(a=[1.0], b=[2])),
            "b",
            ColumnType.Categorical,
        ),
        (
            pd.DataFrame(),
            pd.DataFrame(dict(a=[1.0], b=["a"])),
            "b",
            ColumnType.Categorical,
        ),
        (
            pd.DataFrame(),
            pd.DataFrame(dict(a=[1.0], b=["a"], c=[datetime(2000, 1, 1)])),
            "c",
            ColumnType.Datetime,
        ),
        (pd.DataFrame(dict(a=[1.0], b=[2])), pd.DataFrame(), "a", ColumnType.Numerical),
        (
            pd.DataFrame(dict(a=[1.0], b=[2])),
            pd.DataFrame(),
            "b",
            ColumnType.Categorical,
        ),
        (
            pd.DataFrame(dict(a=[1.0], b=["a"])),
            pd.DataFrame(),
            "b",
            ColumnType.Categorical,
        ),
        (
            pd.DataFrame(dict(a=[1.0], b=["a"], c=[datetime(2000, 1, 1)])),
            pd.DataFrame(),
            "c",
            ColumnType.Datetime,
        ),
        (
            pd.DataFrame(dict(a=[1.0], b=pd.Series(["a"], dtype="string"), c=[datetime(2000, 1, 1)])),
            pd.DataFrame(dict(a=[1.0], b=pd.Series(["a"], dtype="string"), c=[datetime(2000, 1, 1)])),
            "b",
            ColumnType.Categorical,
        ),
    ],
)
def test_get_column_type(reference, current, column_name, expected):
    assert _get_column_type(column_name, _InputData(reference, current)) == expected


@pytest.mark.parametrize(
    "reference,current,mapping,target,id,datetime,prediction,columns,embeddings",
    [
        (
            None,
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            ColumnMapping(),
            None,
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="c", column_type=ColumnType.Datetime),
            ],
            None,
        ),
        (
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            ColumnMapping(),
            None,
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="c", column_type=ColumnType.Datetime),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame(
                dict(
                    a=list(range(NUMBER_UNIQUE_AS_CATEGORICAL + 1)),
                    target=[1] * (NUMBER_UNIQUE_AS_CATEGORICAL + 1),
                ),
            ),
            ColumnMapping(),
            ColumnDefinition(column_name="target", column_type=ColumnType.Categorical),
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="target", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame(dict(a=[1], id=["a"], datetime=[datetime(2000, 1, 1)], prediction=[1])),
            ColumnMapping(id="id"),
            None,
            ColumnDefinition(column_name="id", column_type=ColumnType.Categorical),
            ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
            PredictionColumns(
                predicted_values=ColumnDefinition(column_name="prediction", column_type=ColumnType.Categorical)
            ),
            [
                ColumnDefinition(column_name="id", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
                ColumnDefinition(column_name="prediction", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame(dict(target=[1, 0], prediction=[0.9, 0.1])),
            ColumnMapping(),
            ColumnDefinition(column_name="target", column_type=ColumnType.Categorical),
            None,
            None,
            PredictionColumns(
                predicted_values=None,
                prediction_probas=[
                    ColumnDefinition(column_name="prediction", column_type=ColumnType.Numerical),
                ],
            ),
            [
                ColumnDefinition(column_name="target", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="prediction", column_type=ColumnType.Numerical),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame({"a": [0] * 100 + [1] * 100, "b": [0] * 100 + [1] * 100}),
            ColumnMapping(target="a", prediction="b"),
            ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
            None,
            None,
            PredictionColumns(
                predicted_values=ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
                prediction_probas=None,
            ),
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame({"a": [0] * 100 + [1] * 100, "b": [0] * 100 + [1] * 100}),
            ColumnMapping(target="a", prediction="b", task="regression"),
            ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
            None,
            None,
            PredictionColumns(
                predicted_values=ColumnDefinition(column_name="b", column_type=ColumnType.Numerical),
                prediction_probas=None,
            ),
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
                ColumnDefinition(column_name="b", column_type=ColumnType.Numerical),
            ],
            None,
        ),
        (
            None,
            pd.DataFrame(
                {
                    "a": [0] * 100 + [1] * 100,
                    "b": [0] * 100 + [1] * 100,
                    "c": [0.1] * 100 + [0.6] * 100,
                    "d": [0.1] * 50 + [0.2] * 50 + [0.6] * 100,
                }
            ),
            ColumnMapping(target="a", prediction=["c", "d"]),
            ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
            None,
            None,
            PredictionColumns(
                predicted_values=None,
                prediction_probas=[
                    ColumnDefinition(column_name="c", column_type=ColumnType.Numerical),
                    ColumnDefinition(column_name="d", column_type=ColumnType.Numerical),
                ],
            ),
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="c", column_type=ColumnType.Numerical),
                ColumnDefinition(column_name="d", column_type=ColumnType.Numerical),
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
            ],
            None,
        ),
        (
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            ColumnMapping(embeddings={"a": ["a"]}),
            None,
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="c", column_type=ColumnType.Datetime),
            ],
            {"a": ["a"]},
        ),
        (
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            pd.DataFrame(dict(a=[0.1], b=["a"], c=[datetime(2000, 1, 1)])),
            ColumnMapping(numerical_features=["a"], embeddings={"a": ["a"]}),
            None,
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="b", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="c", column_type=ColumnType.Datetime),
            ],
            {"a": ["a"]},
        ),
        (
            None,
            pd.DataFrame(
                dict(
                    a=list(range(NUMBER_UNIQUE_AS_CATEGORICAL + 1)),
                    target=[1] * (NUMBER_UNIQUE_AS_CATEGORICAL + 1),
                ),
            ),
            ColumnMapping(embeddings={"a": ["target"]}),
            None,
            None,
            None,
            None,
            [
                ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
            ],
            {"a": ["target"]},
        ),
        (
            None,
            pd.DataFrame(dict(a=[1], id=["a"], datetime=[datetime(2000, 1, 1)], prediction=[1])),
            ColumnMapping(id="id", embeddings={"a": ["id"]}),
            None,
            None,
            ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
            PredictionColumns(
                predicted_values=ColumnDefinition(column_name="prediction", column_type=ColumnType.Categorical)
            ),
            [
                ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
                ColumnDefinition(column_name="prediction", column_type=ColumnType.Categorical),
                ColumnDefinition(column_name="a", column_type=ColumnType.Categorical),
            ],
            {"a": ["id"]},
        ),
    ],
)
def test_create_data_definition(reference, current, mapping, target, id, datetime, prediction, columns, embeddings):
    definition = create_data_definition(reference, current, mapping)
    assert definition.get_target_column() == target
    assert definition.get_id_column() == id
    assert definition.get_datetime_column() == datetime
    assert definition.get_prediction_columns() == prediction
    assert definition.get_columns() == columns
    assert definition.embeddings == embeddings
