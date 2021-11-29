from typing import Optional, Union, Sequence

import numpy as np
import pandas as pd
from scipy.stats import norm

from evidently.pipeline.column_mapping import ColumnMapping


def proportions_diff_z_stat_ind(ref, curr):
    # pylint: disable=invalid-name
    n1 = len(ref)
    n2 = len(curr)

    p1 = float(sum(ref)) / n1
    p2 = float(sum(curr)) / n2
    P = float(p1 * n1 + p2 * n2) / (n1 + n2)

    return (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))


def proportions_diff_z_test(z_stat, alternative='two-sided'):
    if alternative == 'two-sided':
        return 2 * (1 - norm.cdf(np.abs(z_stat)))

    if alternative == 'less':
        return norm.cdf(z_stat)

    if alternative == 'greater':
        return 1 - norm.cdf(z_stat)

    raise ValueError("alternative not recognized\n"
                     "should be 'two-sided', 'less' or 'greater'")


class DatasetUtilityColumns:
    def __init__(self,
                 date: Optional[str],
                 id_column: Optional[str],
                 target: Optional[str],
                 prediction: Optional[Union[str, Sequence[str]]]):
        self.date = date
        self.id_column = id_column
        self.target = target
        self.prediction = prediction

    def as_dict(self):
        return {
            'date': self.date,
            'id': self.id_column,
            'target': self.target,
            'prediction': self.prediction,
        }


class DatasetColumns:
    def __init__(self,
                 utility_columns: DatasetUtilityColumns,
                 num_feature_names,
                 cat_feature_names,
                 target_names):
        self.utility_columns = utility_columns
        self.num_feature_names = num_feature_names
        self.cat_feature_names = cat_feature_names
        self.target_names = target_names

    def as_dict(self):
        return {
            'utility_columns': self.utility_columns.as_dict(),
            'cat_feature_names': self.cat_feature_names,
            'num_feature_names': self.num_feature_names,
            'target_names': self.target_names,
        }


def process_columns(dataset: pd.DataFrame, column_mapping: ColumnMapping):
    date_column = column_mapping.datetime if column_mapping.datetime in dataset else None
    id_column = column_mapping.id
    target_column = column_mapping.target if column_mapping.target in dataset else None
    prediction_column = column_mapping.prediction
    num_feature_names = column_mapping.numerical_features
    target_names = column_mapping.target_names

    utility_columns = [date_column, id_column, target_column]
    if isinstance(prediction_column, str):
        prediction_column = prediction_column if prediction_column in dataset else None
        utility_columns.append(prediction_column)
    elif prediction_column is None:
        pass
    else:
        prediction_column = dataset[prediction_column].columns.tolist()
        utility_columns += prediction_column if prediction_column else []
    if num_feature_names is None:
        num_feature_names = list(set(dataset.select_dtypes([np.number]).columns) - set(utility_columns))
    else:
        num_feature_names = dataset[num_feature_names].select_dtypes([np.number]).columns.tolist()

    cat_feature_names = column_mapping.categorical_features
    if cat_feature_names is None:
        cat_feature_names = list(set(dataset.select_dtypes([np.object]).columns) - set(utility_columns))
    else:
        cat_feature_names = dataset[cat_feature_names].select_dtypes([np.number]).columns.tolist()

    return DatasetColumns(
        DatasetUtilityColumns(date_column, id_column, target_column, prediction_column),
        num_feature_names,
        cat_feature_names,
        target_names)
