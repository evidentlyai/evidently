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

def dataset_drift_evaluation(p_values, confidence=0.95, drift_share=0.5):
    n_drifted_features = sum([1 if x<(1. - confidence) else 0 for x in p_values])
    share_drifted_features = n_drifted_features/len(p_values)
    dataset_drift = True if share_drifted_features >= drift_share else False
    return (n_drifted_features, share_drifted_features, dataset_drift)

class DataDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        result = dict()
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
            confidence = 0.95 
            drift_share = 0.5
            nbinsx = None
            xbins = None

        result["utility_columns"] = {'date':date_column, 'id':id_column, 'target':target_column, 'prediction':prediction_column,
            'drift_conf_level':confidence, 'drift_features_share':drift_share, 'nbinsx':nbinsx, 'xbins':xbins}
        result["cat_feature_names"] = cat_feature_names
        result["num_feature_names"] = num_feature_names

        #calculate result
        result['metrics'] = {}

        p_values = []

        for feature_name in num_feature_names:
            p_value=ks_2samp(reference_data[feature_name], current_data[feature_name])[1]
            p_values.append(p_value)
            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name] = dict(
                current_small_hist=[t.tolist() for t in np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                            bins=current_nbinsx, density=True)],
                feature_type='num',
                p_value=p_value    
            )

        for feature_name in cat_feature_names:
            ref_feature_vc = reference_data[feature_name][np.isfinite(reference_data[feature_name])].value_counts()
            current_feature_vc = current_data[feature_name][np.isfinite(current_data[feature_name])].value_counts()

            keys = set(list(reference_data[feature_name][np.isfinite(reference_data[feature_name])].unique()) +
                       list(current_data[feature_name][np.isfinite(current_data[feature_name])].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            current_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(current_feature_vc.index, current_feature_vc.values):
                current_feature_dict[key] = item

            if len(keys) > 2:
                f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
                f_obs = [value[1] for value in sorted(current_feature_dict.items())]
                # CHI2 to be implemented for cases with different categories
                p_value = chisquare(f_exp, f_obs)[1]
            else:
                ordered_keys = sorted(list(keys))
                p_value = proportions_diff_z_test(proportions_diff_z_stat_ind(reference_data[feature_name].apply(lambda x : 0 if x == ordered_keys[0] else 1), 
                    current_data[feature_name].apply(lambda x : 0 if x == ordered_keys[0] else 1)))
            
            p_values.append(p_value)

            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name] = dict(
                current_small_hist=[t.tolist() for t in np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                            bins=current_nbinsx, density=True)],
                feature_type='cat',
                p_value=p_value
            )

        n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(p_values, confidence, drift_share)
        result['metrics']['n_features'] = len(num_feature_names) + len(cat_feature_names)
        result['metrics']['n_drifted_features'] = n_drifted_features
        result['metrics']['share_drifted_features'] = share_drifted_features
        result['metrics']['dataset_drift'] = dataset_drift
        return result
