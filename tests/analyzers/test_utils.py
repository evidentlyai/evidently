import datetime

import pandas
import pytest

from evidently.analyzers.utils import process_columns
from evidently.pipeline.column_mapping import ColumnMapping


def test_process_columns() -> None:
    dataset = pandas.DataFrame({
        'datetime': [datetime.datetime.now()],
        'target': [1],
        'prediction': [1],
        'feature1': [0],
        'feature2': [1],
        'cat_feature1': ['o'],
        'cat_feature2': ['b'],
    })

    columns = process_columns(dataset, ColumnMapping())
    assert columns.utility_columns.id_column is None
    # process_columns has a problem with columns order - it returns not sorted list
    # we have to before a fix use sorted for comparing with sorted expected data
    assert sorted(columns.num_feature_names) == ['feature1', 'feature2']
    assert sorted(columns.cat_feature_names) == ['cat_feature1', 'cat_feature2']


@pytest.mark.parametrize(
    'test_dataset,column_mapping,expected_dict',
    (
        (
            pandas.DataFrame({'missed_all': []}),
            ColumnMapping(),
            {
                'cat_feature_names': [],
                'num_feature_names': ['missed_all'],
                'datetime_feature_names': [],
                'target_names': None,
                'utility_columns': {
                    'date': None,
                    'id': None,
                    'prediction': None,
                    'target': None,
                },
            }
        ),
        (
            pandas.DataFrame({'target': []}),
            ColumnMapping(),
            {
                'cat_feature_names': [],
                'num_feature_names': [],
                'datetime_feature_names': [],
                'target_names': None,
                'utility_columns': {
                    'date': None,
                    'id': None,
                    'prediction': None,
                    'target': 'target',
                },
            }
        ),
        (
            pandas.DataFrame({'prediction': []}),
            ColumnMapping(),
            {
                'cat_feature_names': [],
                'num_feature_names': [],
                'datetime_feature_names': [],
                'target_names': None,
                'utility_columns': {
                    'date': None,
                    'id': None,
                    'prediction': 'prediction',
                    'target': None,
                },
            }
        ),
        (
            pandas.DataFrame({'my_target': [], 'predictions_1': [], 'predictions_2': []}),
            ColumnMapping(
                target='my_target', prediction=['predictions_1', 'predictions_2'], id='test_id'
            ),
            {
                'cat_feature_names': [],
                'num_feature_names': [],
                'datetime_feature_names': [],
                'target_names': None,
                'utility_columns': {
                    'date': None,
                    'id': 'test_id',
                    'prediction': ['predictions_1', 'predictions_2'],
                    'target': 'my_target',
                },
            }
        ),
        (
            pandas.DataFrame({'target': [], 'my_date': [], 'num_1': [], 'cat_1': []}),
            ColumnMapping(
                target='target', prediction=None, datetime='my_date',
                numerical_features=['num_1'], categorical_features=['target', 'cat_1']
            ),
            {
                'cat_feature_names': ['target', 'cat_1'],
                'num_feature_names': ['num_1'],
                'datetime_feature_names': [],
                'target_names': None,
                'utility_columns': {
                    'date': 'my_date',
                    'id': None,
                    'prediction': None,
                    'target': 'target',
                },
            }
        ),
    )
)
def test_dataset_column_default_to_dict(
        test_dataset: pandas.DataFrame, column_mapping: ColumnMapping, expected_dict: dict
) -> None:
    columns = process_columns(test_dataset, column_mapping)
    columns_dict = columns.as_dict()
    assert columns_dict == expected_dict
