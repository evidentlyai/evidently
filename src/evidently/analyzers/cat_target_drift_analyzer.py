#!/usr/bin/env python
# coding: utf-8
from typing import Optional, Dict
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

        feature_type = "cat"
        data_mapping = {
            "reference_data": reference_data,
            "current_data": current_data,
        }
        if target_column:
            metrics = self._get_cat_column_drift(
                column_name=target_column,
                data_mapping=data_mapping,
                feature_type=feature_type,
            )
            result.target_metrics = metrics
        if prediction_column:
            metrics = self._get_cat_column_drift(
                column_name=prediction_column,
                data_mapping=data_mapping,
                feature_type=feature_type
            )
            result.prediction_metrics = metrics

        return result

    @staticmethod
    def _get_pred_labels_from_prob(df: pd.DataFrame,
                                   prediction_column: list):
        array_prediction = df[prediction_column].to_numpy()
        prediction_ids = np.argmax(array_prediction, axis=-1)
        prediction_labels = [prediction_column[x] for x in prediction_ids]
        return prediction_labels

    def _get_cat_column_drift(
            self,
            column_name: str,
            data_mapping: Dict[str, pd.DataFrame],
            feature_type: str
    ) -> DataDriftMetrics:
        columns = {
            data_name: self._get_clean_column(column_name, data)
            for data_name, data in data_mapping.items()
        }
        self._check_columns_not_empty(
            columns=columns, column_name=column_name
        )
        display_name, statistics = self._compute_statistic(
            columns,
            feature_type,
        )
        drift_score, drift_detected = statistics
        metrics = DataDriftMetrics(
            column_name=column_name,
            stattest_name=display_name,
            drift_score=drift_score,
            drift_detected=drift_detected,
        )
        return metrics

    def _get_clean_column(
            self,
            column_name: str,
            data: pd.DataFrame,
    ) -> pd.Series:
        column = data[column_name]
        column = self._remove_nans_and_infinities(column)
        return column

    @staticmethod
    def _check_columns_not_empty(
            columns: Dict[str, pd.Series], column_name: str):
        empty_columns = [
            data_name for data_name, column in columns.items() if column.empty
        ]
        if empty_columns:
            msg = (
                f"After removing invalid values, the {column_name} "
                f"column is empty in the following data sets: \n    - "
            )
            msg += "\n    - ".join(empty_columns)
            raise ValueError(msg)

    def _compute_statistic(
            self,
            column_mapping: Dict[str, pd.Series],
            feature_type: str,
    ):
        reference_column = column_mapping["reference_data"]
        current_column = column_mapping["current_data"]
        data_drift_options = self.options_provider.get(DataDriftOptions)

        stat_test = get_stattest(
            reference_data=reference_column,
            current_data=current_column,
            feature_type=feature_type,
            stattest_func=data_drift_options.cat_target_stattest_func,
        )

        threshold = data_drift_options.cat_target_threshold
        statistic = stat_test(
            reference_data=reference_column,
            current_data=current_column,
            feature_type=feature_type,
            threshold=threshold,
        )
        return stat_test.display_name, statistic

    def _remove_nans_and_infinities(self, column: pd.Series) -> pd.Series:
        keep_mask = self._get_keep_mask(column)
        column = column.loc[keep_mask]
        return column

    @staticmethod
    def _get_keep_mask(column: pd.Series) -> pd.Series:
        finite_mask = ~column.isin([np.inf, -np.inf])
        non_nan_masks = column.notna()
        keep_mask = finite_mask & non_nan_masks
        return keep_mask
