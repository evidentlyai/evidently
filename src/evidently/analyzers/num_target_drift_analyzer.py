#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd
from dataclasses import dataclass

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import ks_stat_test
from evidently.analyzers.utils import process_columns
from evidently.analyzers.utils import DatasetColumns
from typing import List, Callable


@dataclass
class NumDataDriftMetrics:
    """Class for drift values"""
    column_name: str
    reference_correlations: dict
    current_correlations: dict
    drift: float


def _compute_correlation(
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        prefix: str,
        main_column: str,
        num_columns: List[str],
        stats_fun: Callable
) -> Optional[NumDataDriftMetrics]:
    if main_column is None:
        return None

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
    return NumDataDriftMetrics(
        column_name=main_column,
        reference_correlations=ref_target_corr.to_dict(),
        current_correlations=curr_target_corr.to_dict(),
        drift=target_p_value,
    )


@dataclass
class NumTargetDriftAnalyzerResults:
    columns: DatasetColumns
    target_metrics: Optional[NumDataDriftMetrics] = None
    prediction_metrics: Optional[NumDataDriftMetrics] = None


class NumTargetDriftAnalyzer(Analyzer):
    """Numerical target drift analyzer.

    Analyze numerical `target` and `prediction` distributions and provide calculations to the following questions:
    Does the model target behave similarly to the past period? Do my model predictions still look the same?

    For reference see https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift
    """

    @staticmethod
    def get_results(analyzer_results) -> NumTargetDriftAnalyzerResults:
        return analyzer_results[NumTargetDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping) -> NumTargetDriftAnalyzerResults:
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
        data_drift_options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = NumTargetDriftAnalyzerResults(columns=columns)

        if current_data is None:
            raise ValueError("current_data should not be None")

        if set(columns.num_feature_names) - set(current_data.columns):
            raise ValueError(f'Some numerical features in current data {current_data.columns}'
                             f'are not present in columns.num_feature_names')

        func = data_drift_options.num_target_stattest_func or ks_stat_test
        result.target_metrics = _compute_correlation(
            reference_data, current_data, 'target',
            columns.utility_columns.target, columns.num_feature_names, func
        )
        result.prediction_metrics = _compute_correlation(
            reference_data, current_data, 'prediction',
            columns.utility_columns.prediction, columns.num_feature_names, func
        )

        return result
