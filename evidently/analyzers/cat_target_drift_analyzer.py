#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from scipy.stats import chisquare

from evidently.analyzers.base_analyzer import Analyzer
from .utils import proportions_diff_z_stat_ind, proportions_diff_z_test, process_columns


class CatTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

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
                target_p_value = proportions_diff_z_test(
                    proportions_diff_z_stat_ind(
                        reference_data[target_column].apply(lambda x : 0 if x == ordered_keys[0] else 1),
                        current_data[target_column].apply(lambda x : 0 if x == ordered_keys[0] else 1)
                    )
                )

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
                pred_p_value = proportions_diff_z_test(
                    proportions_diff_z_stat_ind(
                        reference_data[prediction_column].apply(lambda x : 0 if x == ordered_keys[0] else 1),
                        current_data[prediction_column].apply(lambda x : 0 if x == ordered_keys[0] else 1)
                    )
                )

            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'cat'
            result['metrics']["prediction_drift"] = pred_p_value

        return result
