#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import z_stat_test, chi_stat_test
from evidently.analyzers.utils import process_columns


class CatTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        result['metrics'] = {}

        func = options.cat_target_stattest_func
        # target drift
        if target_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            keys = set(list(reference_data[target_column].unique()) +
                       list(current_data[target_column].unique()))

            if len(keys) > 2:
                func = chi_stat_test if func is None else func
                target_p_value = func(reference_data[target_column], current_data[target_column])
            else:
                func = z_stat_test if func is None else func
                target_p_value = func(reference_data[target_column], current_data[target_column])

            result['metrics']["target_name"] = target_column
            result['metrics']["target_type"] = 'cat'
            result['metrics']["target_drift"] = target_p_value

        # prediction drift
        if prediction_column is not None:
            # calculate output drift
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            keys = set(list(reference_data[prediction_column].unique()) +
                       list(current_data[prediction_column].unique()))

            if len(keys) > 2:
                func = chi_stat_test if func is None else func
                pred_p_value = func(reference_data[prediction_column], current_data[prediction_column])
            else:
                func = z_stat_test if func is None else func
                pred_p_value = func(reference_data[prediction_column], current_data[prediction_column])

            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'cat'
            result['metrics']["prediction_drift"] = pred_p_value

        return result
