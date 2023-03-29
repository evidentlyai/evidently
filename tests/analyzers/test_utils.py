import datetime

import numpy as np
import pandas as pd
import pytest

from evidently.metric_results import DatasetColumns
from evidently.metric_results import DatasetUtilityColumns
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_operations import process_columns


@pytest.mark.parametrize(
    "test_dataset, data_mapping, expected_columns",
    (
        (
            pd.DataFrame(
                {
                    "datetime_column": [
                        datetime.datetime(year=2022, month=2, day=20),
                        datetime.datetime(year=2021, month=2, day=20),
                        datetime.datetime(year=2020, month=2, day=20),
                    ],
                    "my_target": [1, 0, 1],
                    "my_prediction": [1, 1, 1],
                    "num_feature_1": [0.4, 0.3, 234.2],
                    "num_feature_2": [np.nan, np.nan, np.nan],
                    "cat_feature_1": [1, 2, 3],
                    "cat_feature_2": ["a", "b", "c"],
                    "cat_feature_3": [np.nan, np.nan, np.nan],
                    "cat_feature_4": ["apple", np.nan, "lemon"],
                }
            ),
            ColumnMapping(
                target="my_target",
                prediction="my_prediction",
                numerical_features=["num_feature_1", "num_feature_2"],
                categorical_features=["cat_feature_1", "cat_feature_2", "cat_feature_3", "cat_feature_4"],
                datetime="datetime_column",
                id="some_id",
                target_names=["apple", "lemon", "peach"],
                task="classification",
            ),
            DatasetColumns(
                target_type="cat",
                utility_columns=DatasetUtilityColumns(
                    date="datetime_column", id="some_id", target="my_target", prediction="my_prediction"
                ),
                num_feature_names=["num_feature_1", "num_feature_2"],
                cat_feature_names=["cat_feature_1", "cat_feature_2", "cat_feature_3", "cat_feature_4"],
                datetime_feature_names=[],
                target_names=["apple", "lemon", "peach"],
                task="classification",
                text_feature_names=[],
            ),
        ),
        (
            pd.DataFrame(
                {
                    "index": [1, 2, 3],
                    "datetime": [2001, 1994, 1854],
                    "el_target": [4, 9, 8],
                    "el_prediction": [6, 4, 8],
                    "cat_feature_1": [1, 2, 3],
                }
            ),
            ColumnMapping(
                target="el_target",
                prediction="el_prediction",
                categorical_features=["cat_feature_1"],
                id="index",
                task="regression",
            ),
            DatasetColumns(
                target_type="num",
                utility_columns=DatasetUtilityColumns(
                    date="datetime", id="index", target="el_target", prediction="el_prediction"
                ),
                num_feature_names=[],
                cat_feature_names=["cat_feature_1"],
                datetime_feature_names=[],
                target_names=None,
                task="regression",
                text_feature_names=[],
            ),
        ),
    ),
)
def test_process_columns(
    test_dataset: pd.DataFrame, data_mapping: ColumnMapping, expected_columns: DatasetColumns
) -> None:
    """Test applying data mapping for a different datasets cases"""
    columns = process_columns(test_dataset, data_mapping)
    assert expected_columns == columns


@pytest.mark.parametrize(
    "test_dataset,column_mapping,expected_dict",
    (
        (
            pd.DataFrame({"missed_all": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": ["missed_all"],
                "datetime_feature_names": [],
                "target_names": None,
                "text_feature_names": [],
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": None,
                    "target": None,
                },
            },
        ),
        (
            pd.DataFrame({"target": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "text_feature_names": [],
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": None,
                    "target": "target",
                },
            },
        ),
        (
            pd.DataFrame({"prediction": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "text_feature_names": [],
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": "prediction",
                    "target": None,
                },
            },
        ),
        (
            pd.DataFrame({"my_target": [], "predictions_1": [], "predictions_2": []}),
            ColumnMapping(target="my_target", prediction=["predictions_1", "predictions_2"], id="test_id"),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "text_feature_names": [],
                "utility_columns": {
                    "date": None,
                    "id": "test_id",
                    "prediction": ["predictions_1", "predictions_2"],
                    "target": "my_target",
                },
            },
        ),
        (
            pd.DataFrame({"target": [], "my_date": [], "num_1": [], "cat_1": []}),
            ColumnMapping(
                target="target",
                prediction=None,
                datetime="my_date",
                numerical_features=["num_1"],
                categorical_features=["target", "cat_1"],
            ),
            {
                "cat_feature_names": ["target", "cat_1"],
                "num_feature_names": ["num_1"],
                "datetime_feature_names": [],
                "target_names": None,
                "text_feature_names": [],
                "utility_columns": {
                    "date": "my_date",
                    "id": None,
                    "prediction": None,
                    "target": "target",
                },
            },
        ),
    ),
)
def test_dataset_column_default_to_dict(
    test_dataset: pd.DataFrame, column_mapping: ColumnMapping, expected_dict: dict
) -> None:
    columns = process_columns(test_dataset, column_mapping)
    columns_dict = columns.get_dict()
    assert columns_dict == expected_dict
