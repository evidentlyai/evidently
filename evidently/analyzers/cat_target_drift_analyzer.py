#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from scipy.stats import chisquare

from evidently.analyzers.base_analyzer import Analyzer
from .stattests.z_stattest import proportions_diff_z_stat_ind, proportions_diff_z_test
from .utils import process_columns
from .. import ColumnMapping


# TODO: document somewhere, that all analyzers are mutators, i.e. they will change
#   the dataframe, like here: replace infs and nans. That means if far down the pipeline
#   somebody want to compute number of nans, the results will be 0.
#   Consider return copies of dataframes, even though it will drain memory for large datasets
from ..options import DataDriftOptions


def _remove_nans_and_infinities(dataframe):
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.dropna(axis=0, how='any', inplace=True)
    return dataframe


def _compute_data_stats(reference_data: pd.DataFrame, current_data: pd.DataFrame, column_name: str):
    # keys will be sorted from the beginning
    keys = sorted(set(reference_data[column_name]) | set(current_data[column_name]))

    ref_feature_dict = {**dict.fromkeys(keys, 0), **dict(reference_data[column_name].value_counts())}
    current_feature_dict = {**dict.fromkeys(keys, 0), **dict(current_data[column_name].value_counts())}

    if len(keys) > 2:
        # sort by key and in that order extract values
        f_exp = [value for key, value in sorted(ref_feature_dict.items())]
        f_obs = [value for key, value in sorted(current_feature_dict.items())]
        target_p_value = chisquare(f_exp, f_obs)[1]
    else:
        target_p_value = proportions_diff_z_test(
            proportions_diff_z_stat_ind(
                reference_data[column_name].apply(lambda x: 0 if x == keys[0] else 1),
                current_data[column_name].apply(lambda x: 0 if x == keys[0] else 1)
            )
        )
    return target_p_value


class CatTargetDriftAnalyzer(Analyzer):
    """Categorical target drift analyzer.

    Analyze categorical `target` and `prediction` distributions and provide calculations to the following questions:
    Does the model target behave similarly to the past period? Do my model predictions still look the same?

    For reference see https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift
    """

    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame,
                  column_mapping: ColumnMapping, options: DataDriftOptions = None) -> dict:
        """Calculate the target and prediction drifts.

        Notes:
            Be aware that nay nan or infinity values will be dropped from the dataframes in place.

        Args:
            reference_data: usually the data which you used in training.
            current_data: new, unseen data to which we compare the reference data.
            column_mapping: a `ColumnMapping` object that contains references to the name of target and prediction
                columns
        Returns:
            A dictionary that contains some meta information as well as `metrics` for either target or prediction
            columns or both.
        """
        # options = options or DataDriftOptions()
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        # TODO: consider replacing only values in target and prediction column, see comment above
        #   _remove_nans_and_infinities
        reference_data = _remove_nans_and_infinities(reference_data)
        current_data = _remove_nans_and_infinities(current_data)

        result['metrics'] = {}

        # func = options.cat_target_stattest_func
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
