#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import ks_stat_test
from evidently.analyzers.utils import process_columns


class NumTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        num_feature_names = columns.num_feature_names

        result['metrics'] = {}

        func = options.num_target_stattest_func
        func = ks_stat_test if func is None else func
        # target
        if target_column is not None:
            # drift
            target_p_value = func(reference_data[target_column], current_data[target_column])
            result['metrics']["target_name"] = target_column
            result['metrics']["target_type"] = 'num'
            result['metrics']["target_drift"] = target_p_value

            # corr
            ref_target_corr = reference_data[num_feature_names + [target_column]].corr()[target_column]
            curr_target_corr = current_data[num_feature_names + [target_column]].corr()[target_column]
            target_corr = {'reference': ref_target_corr.to_dict(), 'current': curr_target_corr.to_dict()}
            result['metrics']['target_correlations'] = target_corr

        # prediction
        if prediction_column is not None:
            # drift
            pred_p_value = func(reference_data[prediction_column], current_data[prediction_column])
            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'num'
            result['metrics']["prediction_drift"] = pred_p_value

            # corr
            ref_pred_corr = reference_data[num_feature_names + [prediction_column]].corr()[prediction_column]
            curr_pred_corr = current_data[num_feature_names + [prediction_column]].corr()[prediction_column]
            prediction_corr = {'reference': ref_pred_corr.to_dict(), 'current': curr_pred_corr.to_dict()}
            result['metrics']['prediction_correlations'] = prediction_corr

        return result
