#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from scipy.stats import ks_2samp

from evidently.analyzers.base_analyzer import Analyzer
from .utils import process_columns


class NumTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        num_feature_names = columns.num_feature_names

        result['metrics'] = {}
        #target
        if target_column is not None:
            #drift
            target_p_value = ks_2samp(reference_data[target_column], current_data[target_column])[1]
            result['metrics']["target_name"] = target_column
            result['metrics']["target_type"] = 'num'
            result['metrics']["target_drift"] = target_p_value

            #corr
            ref_target_corr = reference_data[num_feature_names + [target_column]].corr()[target_column]
            curr_target_corr = current_data[num_feature_names + [target_column]].corr()[target_column]
            target_corr = {'reference':ref_target_corr.to_dict(), 'current':curr_target_corr.to_dict()}
            result['metrics']['target_correlations'] = target_corr

        #prediction
        if prediction_column is not None:
            #drift
            pred_p_value = ks_2samp(reference_data[prediction_column], current_data[prediction_column])[1]
            result['metrics']["prediction_name"] = prediction_column
            result['metrics']["prediction_type"] = 'num'
            result['metrics']["prediction_drift"] = pred_p_value

            #corr
            ref_pred_corr = reference_data[num_feature_names + [prediction_column]].corr()[prediction_column]
            curr_pred_corr = current_data[num_feature_names + [prediction_column]].corr()[prediction_column]
            prediction_corr = {'reference':ref_pred_corr.to_dict(), 'current':curr_pred_corr.to_dict()}
            result['metrics']['prediction_correlations'] = prediction_corr

        return result
