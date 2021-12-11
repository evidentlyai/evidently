#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import ks_stat_test
from evidently.analyzers.utils import process_columns


def _compute_correlation(reference_data: pd.DataFrame, current_data: pd.DataFrame, prefix,
                         main_column, num_columns, stats_fun):
    if main_column is None:
        return {}
    target_p_value = stats_fun(reference_data[main_column], current_data[main_column])
    metrics = {
        prefix + '_name': main_column,
        prefix + '_type': 'num',
        prefix + '_drift': target_p_value
    }
    ref_target_corr = reference_data[num_columns + [main_column]].corr()[main_column]
    curr_target_corr = current_data[num_columns + [main_column]].corr()[main_column]
    target_corr = {'reference': ref_target_corr.to_dict(), 'current': curr_target_corr.to_dict()}
    metrics[prefix + '_correlations'] = target_corr
    return metrics


class NumTargetDriftAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping) -> dict:
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        num_feature_names = columns.num_feature_names

        result['metrics'] = {}

        func = options.num_target_stattest_func or ks_stat_test
        # target
        metrics = _compute_correlation(reference_data, current_data, 'target', target_column, num_feature_names, func)
        result['metrics'] = dict(**result['metrics'], **metrics)

        # prediction
        metrics = _compute_correlation(reference_data, current_data, 'prediction', prediction_column, num_feature_names, func)
        result['metrics'] = dict(**result['metrics'], **metrics)

        return result
