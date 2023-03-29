import pandas
import pytest

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_operations import process_columns


@pytest.mark.parametrize(
    "test_dataset,column_mapping,expected_dict",
    (
        (
            pandas.DataFrame({"missed_all": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": ["missed_all"],
                "datetime_feature_names": [],
                "target_names": None,
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": None,
                    "target": None,
                },
                "text_feature_names": [],
            },
        ),
        (
            pandas.DataFrame({"target": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": None,
                    "target": "target",
                },
                "text_feature_names": [],
            },
        ),
        (
            pandas.DataFrame({"prediction": []}),
            ColumnMapping(),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "utility_columns": {
                    "date": None,
                    "id": None,
                    "prediction": "prediction",
                    "target": None,
                },
                "text_feature_names": [],
            },
        ),
        (
            pandas.DataFrame({"my_target": [], "predictions_1": [], "predictions_2": []}),
            ColumnMapping(
                target="my_target",
                prediction=["predictions_1", "predictions_2"],
                id="test_id",
            ),
            {
                "cat_feature_names": [],
                "num_feature_names": [],
                "datetime_feature_names": [],
                "target_names": None,
                "utility_columns": {
                    "date": None,
                    "id": "test_id",
                    "prediction": ["predictions_1", "predictions_2"],
                    "target": "my_target",
                },
                "text_feature_names": [],
            },
        ),
        (
            pandas.DataFrame({"target": [], "my_date": [], "num_1": [], "cat_1": []}),
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
                "utility_columns": {
                    "date": "my_date",
                    "id": None,
                    "prediction": None,
                    "target": "target",
                },
                "text_feature_names": [],
            },
        ),
    ),
)
def test_dataset_column_default_to_dict(
    test_dataset: pandas.DataFrame, column_mapping: ColumnMapping, expected_dict: dict
) -> None:
    columns = process_columns(test_dataset, column_mapping)
    columns_dict = columns.get_dict()
    assert columns_dict == expected_dict
