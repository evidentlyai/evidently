#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from scipy.stats import chisquare

from evidently.analyzers.base_analyzer import Analyzer
from .utils import proportions_diff_z_stat_ind, proportions_diff_z_test, process_columns


# TODO: document somewhere, that all analyzers are mutators, i.e. they will change
#   the dataframe, like here: replace infs and nans. That means if far down the pipeline
#   somebody want to compute number of nans, the results will be 0.
#   Consider return copies of dataframes, even though it will drain memory for large datasets
def _remove_nans_and_infinities(dataframe):
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.dropna(axis=0, how='any', inplace=True)
    return dataframe


def _compute_data_stats(reference_data: pd.DataFrame, current_data: pd.DataFrame, column_name: str):
    ref_feature_vc = reference_data[column_name].value_counts()
    current_feature_vc = current_data[column_name].value_counts()

    keys = set(list(reference_data[column_name].unique()) +
               list(current_data[column_name].unique()))

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
                reference_data[column_name].apply(lambda x: 0 if x == ordered_keys[0] else 1),
                current_data[column_name].apply(lambda x: 0 if x == ordered_keys[0] else 1)
            )
        )
    return target_p_value


class CatTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping) -> dict:
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        # TODO: consider replacing only values in target and prediction column, see comment above
        #   _remove_nans_and_infinities
        reference_data = _remove_nans_and_infinities(reference_data)
        current_data = _remove_nans_and_infinities(current_data)

        result['metrics'] = {}
        # target drift
        if target_column is not None:
            p_value = _compute_data_stats(reference_data, current_data, target_column)
            result['metrics']["target_name"] = target_column
            result['metrics']["target_type"] = 'cat'
            result['metrics']["target_drift"] = p_value

        # prediction drift
        if prediction_column is not None:
            p_value = _compute_data_stats(reference_data, current_data, prediction_column)
            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'cat'
            result['metrics']["prediction_drift"] = p_value

        return result
