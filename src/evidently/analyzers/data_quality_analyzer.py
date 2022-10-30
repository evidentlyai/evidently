#!/usr/bin/env python
# coding: utf-8
from typing import Dict
from typing import Optional

import pandas as pd
from dataclasses import dataclass

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.calculations.data_quality import DataQualityStats
from evidently.calculations.data_quality import calculate_correlations
from evidently.calculations.data_quality import calculate_data_quality_stats
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_task


@dataclass
class DataQualityAnalyzerResults(BaseAnalyzerResult):
    """Class for all results of data quality calculations"""

    reference_features_stats: DataQualityStats
    reference_correlations: Dict[str, pd.DataFrame]
    current_features_stats: Optional[DataQualityStats] = None
    current_correlations: Optional[Dict[str, pd.DataFrame]] = None


class DataQualityAnalyzer(Analyzer):
    """Data quality analyzer
    provides detailed feature statistics and feature behavior overview
    """

    @staticmethod
    def get_results(analyzer_results) -> DataQualityAnalyzerResults:
        return analyzer_results[DataQualityAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
    ) -> DataQualityAnalyzerResults:
        """Calculates base statistics for numerical, categorical and datetime features.
        For categorical features, calculates the Cramer's v correlation matrix.
        For numerical features, Evidently calculates the Pearson, Spearman and Kendall matrices.

        Args:
            reference_data: usually the data which you used in training.
            current_data: new, unseen data to which we compare the reference data.
            column_mapping: a `ColumnMapping` object that contains references to the name of target and prediction
                columns
        Returns:
            A dictionary that contains:
                - some meta information
                - data quality metrics for all features
                - correlation matrices
        """

        columns = process_columns(reference_data, column_mapping)
        target_name = columns.utility_columns.target
        task: Optional[str]

        if column_mapping.task is not None:
            task = column_mapping.task

        elif column_mapping.task is None and target_name:
            task = recognize_task(target_name, reference_data)

        else:
            task = None

        reference_features_stats = calculate_data_quality_stats(reference_data, columns, task)

        current_features_stats: Optional[DataQualityStats]

        if current_data is not None:
            current_features_stats = calculate_data_quality_stats(current_data, columns, task)

            all_cat_features = {}

            if current_features_stats.cat_features_stats is not None:
                all_cat_features.update(current_features_stats.cat_features_stats)

            if task == "classification" and current_features_stats.target_stats is not None:
                all_cat_features.update(current_features_stats.target_stats)

            if current_features_stats.cat_features_stats is not None:
                # calculate additional stats of representation reference dataset values in the current dataset
                for feature_name, cat_feature_stats in all_cat_features.items():
                    current_values_set = set(current_data[feature_name].unique())

                    if feature_name in reference_data:
                        reference_values_set = set(reference_data[feature_name].unique())

                    else:
                        reference_values_set = set()

                    unique_in_current = current_values_set - reference_values_set
                    new_in_current_values_count: int = len(unique_in_current)
                    unique_in_reference = reference_values_set - current_values_set
                    unused_in_current_values_count: int = len(unique_in_reference)

                    # take into account that NaN values in Python sets do not support substitution correctly
                    # {nan} - {nan} can be equals {nan}
                    # use pd.isnull because it supports strings values correctly, np.isnan raises and exception
                    if any(pd.isnull(list(unique_in_current))) and any(pd.isnull(list(unique_in_reference))):
                        new_in_current_values_count -= 1
                        unused_in_current_values_count -= 1

                    cat_feature_stats.new_in_current_values_count = new_in_current_values_count
                    cat_feature_stats.unused_in_current_values_count = unused_in_current_values_count

        else:
            current_features_stats = None

        # calculate correlations
        reference_correlations: Dict = calculate_correlations(reference_data, columns)

        if current_features_stats is not None:
            current_correlations: Dict = calculate_correlations(current_data, columns)

        else:
            current_correlations = {}

        results = DataQualityAnalyzerResults(
            columns=columns,
            reference_features_stats=reference_features_stats,
            reference_correlations=reference_correlations,
        )

        if current_features_stats is not None:
            results.current_features_stats = current_features_stats
            results.current_correlations = current_correlations

        return results
