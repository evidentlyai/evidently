#!/usr/bin/env python
# coding: utf-8
from typing import Optional
from typing import Sequence


from dataclasses import dataclass

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.analyzers.stattests.registry import get_stattest, StatTest
from evidently.analyzers.utils import process_columns
from evidently.options import DataDriftOptions, QualityMetricsOptions


def _remove_nans_and_infinities(dataframe):
    #   document somewhere, that all analyzers are mutators, i.e. they will change
    #   the dataframe, like here: replace inf and nan values. That means if far down the pipeline
    #   somebody wants to compute number of nans, the results will be 0.
    #   Consider return copies of dataframes, even though it will drain memory for large datasets
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.dropna(axis=0, how="any", inplace=True)
    return dataframe


def _compute_statistic(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    feature_type: str,
    column_name: str,
    stattest: StatTest,
    threshold: Optional[float]
):
    return stattest(reference_data[column_name], current_data[column_name], feature_type, threshold)


@dataclass
class DataDriftMetrics:
    """Class for drift values"""

    column_name: str
    stattest_name: str
    drift_score: float
    drift_detected: bool


@dataclass
class CatTargetDriftAnalyzerResults(BaseAnalyzerResult):
    """Class for all results of category target drift calculations"""

    target_metrics: Optional[DataDriftMetrics] = None
    prediction_metrics: Optional[DataDriftMetrics] = None
    reference_data_count: int = 0
    current_data_count: int = 0


class CatTargetDriftAnalyzer(Analyzer):
    """Categorical target drift analyzer.

    Analyze categorical `target` and `prediction` distributions and provide calculations to the following questions:
    Does the model target behave similarly to the past period? Do my model predictions still look the same?

    For reference see https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift
    """

    @staticmethod
    def get_results(analyzer_results) -> CatTargetDriftAnalyzerResults:
        return analyzer_results[CatTargetDriftAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
    ) -> CatTargetDriftAnalyzerResults:
        """Calculate the target and prediction drifts.

        With default options, uses a chi² test when number of labels is greater than 2.
        Otherwise, uses a z-test.

        Notes:
            Be aware that any nan or infinity values will be dropped from the dataframes in place.

            You can also provide a custom function that computes a statistic by adding special
            `DataDriftOptions` object to the `option_provider` of the class.::

                options = DataDriftOptions(cat_target_stattest_func=...)
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
        """
        if reference_data is None:
            raise ValueError("reference_data should be present")

        if current_data is None:
            raise ValueError("current_data should be present")

        data_drift_options = self.options_provider.get(DataDriftOptions)
        threshold = data_drift_options.cat_target_threshold
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        classification_threshold = quality_metrics_options.classification_threshold
        columns = process_columns(reference_data, column_mapping)
        target_column = columns.utility_columns.target
        prediction_column_raw = columns.utility_columns.prediction

        if not isinstance(target_column, str) and isinstance(target_column, Sequence):
            raise ValueError("target should not be a sequence")

        prediction_column = None
        if prediction_column_raw is not None:
            if isinstance(prediction_column_raw, list) and len(prediction_column_raw) > 2:
                reference_data['predicted_labels'] = self._get_pred_labels_from_prob(reference_data, prediction_column_raw)
                current_data['predicted_labels'] = self._get_pred_labels_from_prob(current_data, prediction_column_raw)
                prediction_column = 'predicted_labels'
            elif isinstance(prediction_column_raw, list) and len(prediction_column_raw) == 2:
                reference_data['predicted_labels'] = (reference_data[prediction_column_raw[0]] > classification_threshold).astype(int)
                current_data['predicted_labels'] = (current_data[prediction_column_raw[0]] > classification_threshold).astype(int)
                prediction_column = 'predicted_labels'
            elif isinstance(prediction_column_raw, str):
                prediction_column = prediction_column_raw

        result = CatTargetDriftAnalyzerResults(
            columns=columns, reference_data_count=reference_data.shape[0], current_data_count=current_data.shape[0]
        )

        # consider replacing only values in target and prediction column, see comment above
        #   _remove_nans_and_infinities
        reference_data = _remove_nans_and_infinities(reference_data)
        current_data = _remove_nans_and_infinities(current_data)
        feature_type = "cat"
        if target_column is not None:
            target_test = get_stattest(reference_data[target_column],
                                       current_data[target_column],
                                       feature_type,
                                       data_drift_options.cat_target_stattest_func)
            drift_result = _compute_statistic(
                reference_data, current_data, feature_type, target_column, target_test, threshold
            )
            result.target_metrics = DataDriftMetrics(
                column_name=target_column,
                stattest_name=target_test.display_name,
                drift_score=drift_result.drift_score,
                drift_detected=drift_result.drifted,
            )

        if prediction_column is not None:
            pred_test = get_stattest(reference_data[prediction_column],
                                     current_data[prediction_column],
                                     feature_type,
                                     data_drift_options.cat_target_stattest_func)

            drift_result = _compute_statistic(
                reference_data, current_data, feature_type, prediction_column, pred_test, threshold
            )
            result.prediction_metrics = DataDriftMetrics(
                column_name=prediction_column,
                stattest_name=pred_test.display_name,
                drift_score=drift_result.drift_score,
                drift_detected=drift_result.drifted,
            )

        return result

    def _get_pred_labels_from_prob(self, df: pd.DataFrame, prediction_column: list):
        array_prediction = df[prediction_column].to_numpy()
        prediction_ids = np.argmax(array_prediction, axis=-1)
        prediction_labels = [prediction_column[x] for x in prediction_ids]
        return prediction_labels
