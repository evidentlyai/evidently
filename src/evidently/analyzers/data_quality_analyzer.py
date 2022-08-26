#!/usr/bin/env python
# coding: utf-8
from typing import Dict
from typing import Callable
from typing import Optional
from typing import Union

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.utils.data_operations import process_columns
from evidently.utils.data_operations import recognize_task
from evidently.utils.data_operations import DatasetColumns
from evidently.calculations.data_quality import DataQualityStats
from evidently.calculations.data_quality import FeatureQualityStats


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

    def _calculate_stats(self, dataset: pd.DataFrame, columns: DatasetColumns, task: Optional[str]) -> DataQualityStats:
        result = DataQualityStats()

        result.num_features_stats = {
            feature_name: self._get_features_stats(dataset[feature_name], feature_type="num")
            for feature_name in columns.num_feature_names
        }

        result.cat_features_stats = {
            feature_name: self._get_features_stats(dataset[feature_name], feature_type="cat")
            for feature_name in columns.cat_feature_names
        }

        if columns.utility_columns.date:
            date_list = columns.datetime_feature_names + [columns.utility_columns.date]

        else:
            date_list = columns.datetime_feature_names

        result.datetime_features_stats = {
            feature_name: self._get_features_stats(dataset[feature_name], feature_type="datetime")
            for feature_name in date_list
        }

        target_name = columns.utility_columns.target

        if target_name is not None and target_name in dataset:
            result.target_stats = {}

            if task == "classification":
                result.target_stats[target_name] = self._get_features_stats(dataset[target_name], feature_type="cat")

            else:
                result.target_stats[target_name] = self._get_features_stats(dataset[target_name], feature_type="num")

        prediction_name = columns.utility_columns.prediction

        if isinstance(prediction_name, str) and prediction_name in dataset:
            result.prediction_stats = {}

            if task == "classification":
                result.prediction_stats[prediction_name] = self._get_features_stats(
                    dataset[prediction_name], feature_type="cat"
                )

            else:
                result.prediction_stats[prediction_name] = self._get_features_stats(
                    dataset[prediction_name], feature_type="num"
                )

        return result

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

        reference_features_stats = self._calculate_stats(reference_data, columns, task)

        current_features_stats: Optional[DataQualityStats]

        if current_data is not None:
            current_features_stats = self._calculate_stats(current_data, columns, task)

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

        num_for_corr, cat_for_corr = self._select_features_for_corr(reference_features_stats, target_name)
        reference_correlations = {}
        current_correlations = {}
        for kind in ["pearson", "spearman", "kendall", "cramer_v"]:
            reference_correlations[kind] = self._calculate_correlations(
                reference_data, num_for_corr, cat_for_corr, kind
            )
            if current_data is not None:
                current_correlations[kind] = self._calculate_correlations(
                    current_data, num_for_corr, cat_for_corr, kind
                )
        results = DataQualityAnalyzerResults(
            columns=columns,
            reference_features_stats=reference_features_stats,
            reference_correlations=reference_correlations,
        )
        if current_features_stats is not None:
            results.current_features_stats = current_features_stats
            results.current_correlations = current_correlations

        return results

    @staticmethod
    def _get_features_stats(feature: pd.Series, feature_type: str) -> FeatureQualityStats:
        def get_percentage_from_all_values(value: Union[int, float]) -> float:
            return np.round(100 * value / all_values_count, 2)

        result = FeatureQualityStats(feature_type=feature_type)
        all_values_count = feature.shape[0]

        if not all_values_count > 0:
            # we have no data, return default stats for en empty dataset
            return result

        result.missing_count = int(feature.isnull().sum())
        result.count = int(feature.count())
        all_values_count = feature.shape[0]
        value_counts = feature.value_counts(dropna=False)
        result.missing_percentage = np.round(100 * result.missing_count / all_values_count, 2)
        unique_count: int = feature.nunique()
        result.unique_count = unique_count
        result.unique_percentage = get_percentage_from_all_values(unique_count)
        result.most_common_value = value_counts.index[0]
        result.most_common_value_percentage = get_percentage_from_all_values(value_counts.iloc[0])

        if result.count > 0 and pd.isnull(result.most_common_value):
            result.most_common_not_null_value = value_counts.index[1]
            result.most_common_not_null_value_percentage = get_percentage_from_all_values(value_counts.iloc[1])

        if feature_type == "num":
            # round most common feature value for numeric features to 1e-5
            if not np.issubdtype(feature, np.number):
                feature = feature.astype(float)
            result.most_common_value = np.round(result.most_common_value, 5)
            result.infinite_count = int(np.sum(np.isinf(feature)))
            result.infinite_percentage = get_percentage_from_all_values(result.infinite_count)
            result.max = np.round(feature.max(), 2)
            result.min = np.round(feature.min(), 2)
            common_stats = dict(feature.describe())
            std = common_stats["std"]
            result.std = np.round(std, 2)
            result.mean = np.round(common_stats["mean"], 2)
            result.percentile_25 = np.round(common_stats["25%"], 2)
            result.percentile_50 = np.round(common_stats["50%"], 2)
            result.percentile_75 = np.round(common_stats["75%"], 2)

        if feature_type == "datetime":
            # cast datetime value to str for datetime features
            result.most_common_value = str(result.most_common_value)
            # cast datetime value to str for datetime features
            result.max = str(feature.max())
            result.min = str(feature.min())

        return result

    def _select_features_for_corr(
        self, reference_features_stats: DataQualityStats, target_name: Optional[str]
    ) -> tuple:
        """Define which features should be used for calculating correlation matrices:
            - for pearson, spearman, and kendall correlation matrices we select numerical features which have > 1
                unique values;
            - for kramer_v correlation matrix, we select categorical features which have > 1 unique values.
        Args:
            reference_features_stats: all features data quality metrics.
            target_name: name of target column.
        Returns:
            num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
            cat_for_corr: list of feature names for kramer_v correlation matrix.
        """
        num_for_corr = []
        if reference_features_stats.num_features_stats is not None:
            for feature in reference_features_stats.num_features_stats:
                unique_count = reference_features_stats[feature].unique_count
                if unique_count and unique_count > 1:
                    num_for_corr.append(feature)
        cat_for_corr = []
        if reference_features_stats.cat_features_stats is not None:
            for feature in reference_features_stats.cat_features_stats:
                unique_count = reference_features_stats[feature].unique_count
                if unique_count and unique_count > 1:
                    cat_for_corr.append(feature)

        if target_name is not None and reference_features_stats.target_stats is not None:
            target_type = reference_features_stats.target_stats[target_name].feature_type
            unique_count = reference_features_stats.target_stats[target_name].unique_count

            if target_type == "num" and unique_count and unique_count > 1:
                num_for_corr.append(target_name)

            elif target_type == "cat" and unique_count and unique_count > 1:
                cat_for_corr.append(target_name)

        return num_for_corr, cat_for_corr

    def _cramer_v(self, x: pd.Series, y: pd.Series) -> float:
        """Calculate Cramér's V: a measure of association between two nominal variables.
        Args:
            x: The array of observed values.
            y: The array of observed values.
        Returns:
            Value of the Cramér's V
        """
        arr = pd.crosstab(x, y).values
        chi2_stat = chi2_contingency(arr, correction=False)
        phi2 = chi2_stat[0] / arr.sum()
        n_rows, n_cols = arr.shape
        if min(n_cols - 1, n_rows - 1) == 0:
            value = np.nan
        else:
            value = np.sqrt(phi2 / min(n_cols - 1, n_rows - 1))

        return value

    def _corr_matrix(self, df: pd.Series, func: Callable[[pd.Series, pd.Series], float]) -> pd.DataFrame:
        """Compute pairwise correlation of columns
        Args:
            df: initial data frame.
            func: function for computing pairwise correlation.
        Returns:
            Correlation matrix.
        """
        columns = df.columns
        K = df.shape[1]
        if K <= 1:
            return pd.DataFrame()
        else:
            corr_array = np.eye(K)

            for i in range(K):
                for j in range(K):
                    if i <= j:
                        continue
                    c = func(df[columns[i]], df[columns[j]])
                    corr_array[i, j] = c
                    corr_array[j, i] = c
            return pd.DataFrame(data=corr_array, columns=columns, index=columns)

    def _calculate_correlations(self, df, num_for_corr, cat_for_corr, kind):
        """Calculate correlation matrix depending on the kind parameter
        Args:
            df: initial data frame.
            num_for_corr: list of feature names for pearson, spearman, and kendall correlation matrices.
            cat_for_corr: list of feature names for kramer_v correlation matrix.
            kind: Method of correlation:
                - pearson - standard correlation coefficient
                - kendall - Kendall Tau correlation coefficient
                - spearman - Spearman rank correlation
                - cramer_v - Cramer’s V measure of association
        Returns:
            Correlation matrix.
        """
        if kind == "pearson":
            return df[num_for_corr].corr("pearson")
        elif kind == "spearman":
            return df[num_for_corr].corr("spearman")
        elif kind == "kendall":
            return df[num_for_corr].corr("kendall")
        elif kind == "cramer_v":
            return self._corr_matrix(df[cat_for_corr], self._cramer_v)
