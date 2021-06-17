#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare


class NumTargetDriftAnalyzer(Analyzer):
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
