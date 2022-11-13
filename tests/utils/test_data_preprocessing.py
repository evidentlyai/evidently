from datetime import datetime
import pandas as pd
import pytest
from evidently.pipeline.column_mapping import ColumnMapping

from evidently.utils.data_preprocessing import ColumnPresenceState, ColumnType, DataDefinition, ColumnDefinition, _InputData, PredictionColumns, _get_column_presence, _get_column_type, create_data_definition


def test_get_columns():
    definition = DataDefinition(
        columns=[
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
        ],
        id_column=ColumnDefinition("id", ColumnType.Categorical),
        datetime_column=ColumnDefinition("datetime", ColumnType.Datetime),
        target=ColumnDefinition("target", ColumnType.Categorical),
        prediction_columns=PredictionColumns(
            predicted_values=ColumnDefinition("predicted", ColumnType.Categorical),
            prediction_probas=[
                ColumnDefinition("class_1", ColumnType.Numerical),
                ColumnDefinition("class_2", ColumnType.Numerical),
                ColumnDefinition("class_3", ColumnType.Numerical),
            ]
        ),
        task="classification",
        classification_labels=["class_1", "class_2", "class_3"],
    )

    assert ["id", "datetime", "target", "predicted", "class_1", "class_2", "class_3",
            "column_1", "column_2", "column_3", "column_4", "column_5", "column_6"] == [cd.column_name for cd in definition.get_columns()]
    assert ["id", "target", "predicted", "column_1"] == [cd.column_name for cd in definition.get_columns(filter_def="categorical_columns")]
    assert ["class_1", "class_2", "class_3", "column_2", "column_3"] == [cd.column_name for cd in definition.get_columns(filter_def="numerical_columns")]
    assert ["datetime", "column_4", "column_5", "column_6"] == [cd.column_name for cd in definition.get_columns(filter_def="datetime_columns")]

    assert ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6"] == [cd.column_name for cd in definition.get_columns(filter_def="all_features")]
    assert ["column_1"] == [cd.column_name for cd in definition.get_columns(filter_def="categorical_features")]
    assert ["column_2", "column_3"] == [cd.column_name for cd in definition.get_columns(filter_def="numerical_features")]
    assert ["column_4", "column_5", "column_6"] == [cd.column_name for cd in definition.get_columns(filter_def="datetime_features")]


@pytest.mark.parametrize("reference,current,column_name,expected",
[
    (None, pd.DataFrame(dict(a=[1], b=[2])), "a", ColumnPresenceState.Present),
    (None, pd.DataFrame(dict(a=[1], b=[2])), "b", ColumnPresenceState.Present),
    (None, pd.DataFrame(dict(a=[1], b=[2])), "c", ColumnPresenceState.Missing),
    (pd.DataFrame(dict(a=[1], c=[2])), pd.DataFrame(dict(a=[1], b=[2])), "a", ColumnPresenceState.Present),
    (pd.DataFrame(dict(a=[1], c=[2])), pd.DataFrame(dict(a=[1], b=[2])), "b", ColumnPresenceState.Partially),
    (pd.DataFrame(dict(a=[1], c=[2])), pd.DataFrame(dict(a=[1], b=[2])), "c", ColumnPresenceState.Partially),
    (pd.DataFrame(dict(a=[1], c=[2])), pd.DataFrame(dict(a=[1], b=[2])), "d", ColumnPresenceState.Missing),
])
def test_column_presence(reference, current, column_name, expected):
    assert _get_column_presence(column_name, _InputData(reference, current)) == expected


@pytest.mark.parametrize("reference,current,column_name,expected",
[
    (None, pd.DataFrame(dict(a=[1], b=[2])), "a", ColumnType.Numerical),
    (None, pd.DataFrame(dict(a=[1], b=["a"])), "b", ColumnType.Categorical),
    (None, pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])), "c", ColumnType.Datetime),
    (pd.DataFrame(), pd.DataFrame(dict(a=[1], b=[2])), "a", ColumnType.Numerical),
    (pd.DataFrame(), pd.DataFrame(dict(a=[1], b=["a"])), "b", ColumnType.Categorical),
    (pd.DataFrame(), pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])), "c", ColumnType.Datetime),
    (pd.DataFrame(dict(a=[1], b=[2])), pd.DataFrame(), "a", ColumnType.Numerical),
    (pd.DataFrame(dict(a=[1], b=["a"])), pd.DataFrame(), "b", ColumnType.Categorical),
    (pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])), pd.DataFrame(), "c", ColumnType.Datetime),
])
def test_get_column_type(reference,current,column_name,expected):
    assert _get_column_type(column_name, _InputData(reference, current)) == expected


@pytest.mark.parametrize("reference,current,mapping,target,id,datetime,prediction,columns",
[
    (
        None,
        pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])),
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
    ),
    (
        pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])),
        pd.DataFrame(dict(a=[1], b=["a"], c=[datetime(2000, 1, 1)])),
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
    ),
    (
        None,
        pd.DataFrame(dict(a=[1], target=[1])),
        ColumnMapping(),
        ColumnDefinition(column_name="target", column_type=ColumnType.Numerical),
        None,
        None,
        None,
        [
            ColumnDefinition(column_name="target", column_type=ColumnType.Numerical),
            ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
        ],
    ),
    (
        None,
        pd.DataFrame(dict(a=[1], id=["a"], datetime=[datetime(2000, 1, 1)], prediction=[1])),
        ColumnMapping(id="id"),
        None,
        ColumnDefinition(column_name="id", column_type=ColumnType.Categorical),
        ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
        PredictionColumns(predicted_values=ColumnDefinition(column_name="prediction", column_type=ColumnType.Numerical)),
        [
            ColumnDefinition(column_name="id", column_type=ColumnType.Categorical),
            ColumnDefinition(column_name="datetime", column_type=ColumnType.Datetime),
            ColumnDefinition(column_name="prediction", column_type=ColumnType.Numerical),
            ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
        ],
    ),
    (
        None,
        pd.DataFrame(dict(a=[1], c1=[.1], c2=[.2])),
        ColumnMapping(prediction=["c1", "c2"]),
        None,
        None,
        None,
        PredictionColumns(prediction_probas=[
            ColumnDefinition(column_name="c1", column_type=ColumnType.Numerical),
            ColumnDefinition(column_name="c2", column_type=ColumnType.Numerical),
        ]),
        [
            ColumnDefinition(column_name="c1", column_type=ColumnType.Numerical),
            ColumnDefinition(column_name="c2", column_type=ColumnType.Numerical),
            ColumnDefinition(column_name="a", column_type=ColumnType.Numerical),
        ],
    ),
])
def test_create_data_definition(reference, current, mapping, target, id, datetime, prediction, columns):
    definition = create_data_definition(_InputData(reference, current), mapping)
    assert definition.get_target_column() == target
    assert definition.get_id_column() == id
    assert definition.get_datetime_column() == datetime
    assert definition.get_prediction_columns() == prediction
    assert definition.get_columns() == columns
