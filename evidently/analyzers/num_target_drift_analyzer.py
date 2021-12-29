#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import ks_stat_test
from evidently.analyzers.utils import process_columns
from typing import List, Callable


def _compute_correlation(reference_data: pd.DataFrame, current_data: pd.DataFrame, prefix: str,
                         main_column: str, num_columns: List[str], stats_fun: Callable):
    if main_column is None:
        return {}
    if not pd.api.types.is_numeric_dtype(reference_data[main_column]) or \
            not pd.api.types.is_numeric_dtype(current_data[main_column]):
        raise ValueError(f'Column {main_column} should only contain numerical values.')
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
    """Numerical target drift analyzer.

    Analyze numerical `target` and `prediction` distributions and provide calculations to the following questions:
    Does the model target behave similarly to the past period? Do my model predictions still look the same?

    For reference see https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift
    """
    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping):
        """Calculate the target and prediction drifts.

        With default options, uses a two sample Kolmogorov-Smirnov test at a 0.95 confidence level.

        Notes:
            You can also provide a custom function that computes a statistic by adding special
            `DataDriftOptions` object to the `option_provider` of the class.::

                options = DataDriftOptions(num_target_stattest_func=...)
                analyzer.options_prover.add(options)

            Such a function takes two arguments:::

                def(reference_data: pd.Series, current_data: pd.Series):
                   ...

            and returns arbitrary number (like a p_value from the other tests ;-))
        Args:
            reference_data: usually the data which you used in training.
            current_data: new, unseen data to which we compare the reference data.
            column_mapping: a `ColumnMapping` object that contains references to the name of target and prediction
                columns
        Returns:
            A dictionary that contains some meta information as well as `metrics` for either target or prediction
            columns or both. The `*_drift` column in `metrics` contains a computed p_value from tests.
        Raises:
            ValueError when target or predictions columns are not numerical.
        """
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        if current_data is None:
            raise ValueError("current_data should not be None")
        if set(columns.num_feature_names) - set(current_data.columns):
            raise ValueError(f'Some numerical features in current data {current_data.columns}'
                             f'are not present in columns.num_feature_names')

        func = options.num_target_stattest_func or ks_stat_test
        target_metrics = _compute_correlation(reference_data, current_data, 'target',
                                              columns.utility_columns.target, columns.num_feature_names, func)
        prediction_metrics = _compute_correlation(reference_data, current_data, 'prediction',
                                                  columns.utility_columns.prediction, columns.num_feature_names, func)
        result['metrics'] = dict(**target_metrics, **prediction_metrics)

        return result
