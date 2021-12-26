#!/usr/bin/env python
# coding: utf-8
import collections
from typing import Any, Dict, List

import pandas as pd
import numpy as np
from dataclasses import dataclass, field

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import chi_stat_test, ks_stat_test, z_stat_test
from evidently.analyzers.utils import process_columns, DatasetUtilityColumns


def dataset_drift_evaluation(p_values, drift_share=0.5):
    n_drifted_features = sum([1 if x.p_value < (1. - x.confidence) else 0 for _, x in p_values.items()])
    share_drifted_features = n_drifted_features / len(p_values)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


PValueWithConfidence = collections.namedtuple("PValueWithConfidence", ["p_value", "confidence"])


@dataclass
class DataDriftAnalyzerResults:
    utility_columns: DatasetUtilityColumns
    cat_feature_names: List[str]
    num_feature_names: List[str]
    target_names: List[str]
    options: DataDriftOptions
    metrics: dict = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the analyser data to dict for data serialization"""
        return {
            'utility_columns': self.utility_columns.as_dict(),
            'cat_feature_names': self.cat_feature_names,
            'num_feature_names': self.num_feature_names,
            'target_names': self.target_names,
            'options': self.options.as_dict(),
            'metrics': self.metrics
        }

    def get_all_features_list(self) -> List[str]:
        """List all features names"""
        return self.cat_feature_names + self.num_feature_names


class DataDriftAnalyzer(Analyzer):
    @staticmethod
    def get_data_drift_results(analyzer_results) -> DataDriftAnalyzerResults:
        return analyzer_results[DataDriftAnalyzer]

    def calculate(
            self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping: ColumnMapping
    ) -> DataDriftAnalyzerResults:
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = DataDriftAnalyzerResults(
            utility_columns=columns.utility_columns,
            cat_feature_names=columns.cat_feature_names,
            num_feature_names=columns.num_feature_names,
            target_names=columns.target_names,
            options=options
        )

        num_feature_names = columns.num_feature_names
        cat_feature_names = columns.cat_feature_names
        drift_share = options.drift_share

        # calculate result
        result.metrics = {}

        p_values = {}
        for feature_name in num_feature_names:
            confidence = options.get_confidence(feature_name)
            func = options.get_feature_stattest_func(feature_name, ks_stat_test)
            p_value = func(reference_data[feature_name], current_data[feature_name])
            p_values[feature_name] = PValueWithConfidence(p_value, confidence)
            current_nbinsx = options.get_nbinsx(feature_name)
            result.metrics[feature_name] = dict(
                current_small_hist=[t.tolist() for t in
                                    np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                                 bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in
                                np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                feature_type='num',
                p_value=p_value
            )

        for feature_name in cat_feature_names:
            confidence = options.get_confidence(feature_name)
            func = options.get_feature_stattest_func(feature_name, ks_stat_test)
            keys = set(list(reference_data[feature_name][np.isfinite(reference_data[feature_name])].unique()) +
                       list(current_data[feature_name][np.isfinite(current_data[feature_name])].unique()))

            if len(keys) > 2:
                # CHI2 to be implemented for cases with different categories
                func = chi_stat_test if func is None else func
                p_value = func(reference_data[feature_name], current_data[feature_name])
            else:
                func = z_stat_test if func is None else func
                p_value = func(reference_data[feature_name], current_data[feature_name])

            p_values[feature_name] = PValueWithConfidence(p_value, confidence)

            current_nbinsx = options.get_nbinsx(feature_name)
            result.metrics[feature_name] = dict(
                current_small_hist=[t.tolist() for t in
                                    np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                                 bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in
                                np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                feature_type='cat',
                p_value=p_value
            )

        n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(p_values, drift_share)
        result.metrics['n_features'] = len(num_feature_names) + len(cat_feature_names)
        result.metrics['n_drifted_features'] = n_drifted_features
        result.metrics['share_drifted_features'] = share_drifted_features
        result.metrics['dataset_drift'] = dataset_drift
        return result
