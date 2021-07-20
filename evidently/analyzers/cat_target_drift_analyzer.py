#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare, norm

def proportions_diff_z_stat_ind(ref, curr):
    n1 = len(ref)
    n2 = len(curr)
    
    p1 = float(sum(ref)) / n1
    p2 = float(sum(curr)) / n2 
    P = float(p1*n1 + p2*n2) / (n1 + n2)
    
    return (p1 - p2) / np.sqrt(P * (1 - P) * (1. / n1 + 1. / n2))

def proportions_diff_z_test(z_stat, alternative = 'two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized\n"
                         "should be 'two-sided', 'less' or 'greater'")
    
    if alternative == 'two-sided':
        return 2 * (1 - norm.cdf(np.abs(z_stat)))
    
    if alternative == 'less':
        return norm.cdf(z_stat)

    if alternative == 'greater':
        return 1 - norm.cdf(z_stat)

class CatTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        result = dict()
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])]

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])]
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        result["utility_columns"] = {'date':date_column, 'id':id_column, 'target':target_column, 'prediction':prediction_column}
        result["cat_feature_names"] = cat_feature_names
        result["num_feature_names"] = num_feature_names

        result['metrics'] = {}
        #target drift
        if target_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            ref_feature_vc = reference_data[target_column].value_counts()
            current_feature_vc = current_data[target_column].value_counts()

            keys = set(list(reference_data[target_column].unique()) + 
                list(current_data[target_column].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            current_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(current_feature_vc.index, current_feature_vc.values):
                current_feature_dict[key] = item

            if len(keys) > 2:
                f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
                f_obs = [value[1] for value in sorted(current_feature_dict.items())]
                target_p_value = chisquare(f_exp, f_obs)[1]
            else:
                ordered_keys = sorted(list(keys))
                target_p_value = proportions_diff_z_test(proportions_diff_z_stat_ind(reference_data[target_column].apply(lambda x : 0 if x == ordered_keys[0] else 1), 
                    current_data[target_column].apply(lambda x : 0 if x == ordered_keys[0] else 1)))

            result['metrics']["target_name"] = target_column
            result['metrics']["target_type"] = 'cat'
            result['metrics']["target_drift"] = target_p_value

        #prediction drift
        if prediction_column is not None:
            #calculate output drift
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            ref_feature_vc = reference_data[prediction_column].value_counts()
            current_feature_vc = current_data[prediction_column].value_counts()

            keys = set(list(reference_data[prediction_column].unique()) + 
                list(current_data[prediction_column].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            current_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(current_feature_vc.index, current_feature_vc.values):
                current_feature_dict[key] = item

            if len(keys) > 2:
                f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
                f_obs = [value[1] for value in sorted(current_feature_dict.items())]
                pred_p_value = chisquare(f_exp, f_obs)[1]
            else:
                ordered_keys = sorted(list(keys))
                pred_p_value = proportions_diff_z_test(proportions_diff_z_stat_ind(reference_data[prediction_column].apply(lambda x : 0 if x == ordered_keys[0] else 1), 
                    current_data[prediction_column].apply(lambda x : 0 if x == ordered_keys[0] else 1)))

            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'cat'
            result['metrics']["prediction_drift"] = pred_p_value

        return result
