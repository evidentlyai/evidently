import numpy as np
from scipy.stats import norm

def proportions_diff_z_stat_ind(ref, curr):
    # pylint: disable=invalid-name
    n1 = len(ref)
    n2 = len(curr)

    p1 = float(sum(ref)) / n1
    p2 = float(sum(curr)) / n2
    P = float(p1*n1 + p2*n2) / (n1 + n2)

    return (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))


def proportions_diff_z_test(z_stat, alternative = 'two-sided'):
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
                 date: str,
                 id_column: str,
                 target: str,
                 prediction: str,
                 drift_conf_level: float,
                 drift_features_share: float,
                 nbinsx: float,
                 xbins: float):
        self.date = date
        self.id_column = id_column
        self.target = target
        self.prediction = prediction
        self.drift_conf_level = drift_conf_level
        self.drift_features_share = drift_features_share
        self.nbinsx = nbinsx
        self.xbins = xbins

    def as_dict(self):
        return {
            'date': self.date,
            'id': self.id_column,
            'target': self.target,
            'prediction': self.prediction,
            'drift_conf_level': self.drift_conf_level,
            'drift_features_share': self.drift_features_share,
            'nbinsx': self.nbinsx,
            'xbins': self.xbins
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


def process_columns(dataset, column_mapping):
    if column_mapping:
        date_column = column_mapping.get('datetime')
        id_column = column_mapping.get('id')
        target_column = column_mapping.get('target')
        prediction_column = column_mapping.get('prediction')
        num_feature_names = column_mapping.get('numerical_features')
        confidence = column_mapping.get('drift_conf_level')
        if confidence is None:
            confidence = 0.95
        drift_share = column_mapping.get('drift_features_share')
        if drift_share is None:
            drift_share = 0.5
        nbinsx = column_mapping.get('nbinsx')
        xbins = column_mapping.get('xbins')
        target_names = column_mapping.get('target_names')
        if num_feature_names is None:
            num_feature_names = []
        else:
            num_feature_names = dataset[num_feature_names].select_dtypes([np.number]).columns.tolist()

        cat_feature_names = column_mapping.get('categorical_features')
        if cat_feature_names is None:
            cat_feature_names = []
        else:
            cat_feature_names = dataset[cat_feature_names].select_dtypes([np.number]).columns.tolist()
    else:
        date_column = 'datetime' if 'datetime' in dataset.columns else None
        id_column = None
        target_column = 'target' if 'target' in dataset.columns else None
        prediction_column = 'prediction' if 'prediction' in dataset.columns else None

        utility_columns = [date_column, id_column, target_column, prediction_column]

        num_feature_names = list(set(dataset.select_dtypes([np.number]).columns) - set(utility_columns))
        cat_feature_names = list(set(dataset.select_dtypes([np.object]).columns) - set(utility_columns))

        target_names = None
        confidence = 0.95
        drift_share = 0.5
        nbinsx = None
        xbins = None

    return DatasetColumns(
                DatasetUtilityColumns(date_column, id_column, target_column, prediction_column, confidence, drift_share, nbinsx, xbins),
                num_feature_names,
                cat_feature_names,
                target_names)
