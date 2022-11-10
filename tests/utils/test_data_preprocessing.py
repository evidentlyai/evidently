import pytest

from evidently.utils.data_preprocessing import DataDefinition, ColumnDefinition


def test_get_columns():
    definition = DataDefinition(
        columns=[
            ColumnDefinition("column_1", "cat"),
            ColumnDefinition("column_2", "num"),
            ColumnDefinition("column_3", "num"),
            ColumnDefinition("column_4", "datetime"),
            ColumnDefinition("column_5", "datetime"),
            ColumnDefinition("column_6", "datetime"),
        ],
        target=None,
        prediction_columns=None,
        task="classification",
        classification_labels=[],
    )

    assert ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6"] == definition.get_columns()
    assert ["column_1"] == definition.get_columns(filter_def="categorical_columns")
    assert ["column_2", "column_3"] == definition.get_columns(filter_def="numerical_columns")
    assert ["column_4", "column_5", "column_6"] == definition.get_columns(filter_def="datetime_columns")
