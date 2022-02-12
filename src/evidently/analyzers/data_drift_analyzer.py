#!/usr/bin/env python
# coding: utf-8
import collections
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

import pandas as pd
import numpy as np

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import chi_stat_test, ks_stat_test, z_stat_test
from evidently.analyzers.utils import process_columns


def dataset_drift_evaluation(p_values, drift_share=0.5) -> Tuple[int, float, bool]:
    n_drifted_features = sum([1 if x.p_value < (1. - x.confidence) else 0 for _, x in p_values.items()])
    share_drifted_features = n_drifted_features / len(p_values)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


PValueWithConfidence = collections.namedtuple("PValueWithConfidence", ["p_value", "confidence"])


@dataclass
class DataDriftAnalyzerFeatureMetrics:
    current_small_hist: list
    ref_small_hist: list
    feature_type: str
    p_value: float


@dataclass
class DataDriftAnalyzerMetrics:
    n_features: int
    n_drifted_features: int
    share_drifted_features: float
    dataset_drift: bool
    features: Dict[str, DataDriftAnalyzerFeatureMetrics]


@dataclass
class DataDriftAnalyzerResults(BaseAnalyzerResult):
    options: DataDriftOptions
    metrics: DataDriftAnalyzerMetrics


class DataDriftAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> DataDriftAnalyzerResults:
        return analyzer_results[DataDriftAnalyzer]

    def calculate(
            self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> DataDriftAnalyzerResults:
        if current_data is None:
            raise ValueError("current_data should be present")

        data_drift_options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        num_feature_names = columns.num_feature_names
        cat_feature_names = columns.cat_feature_names
        drift_share = data_drift_options.drift_share

        # calculate result
        features_metrics = {}
        p_values = {}

        for feature_name in num_feature_names:
            confidence = data_drift_options.get_confidence(feature_name)
            func = data_drift_options.get_feature_stattest_func(feature_name, ks_stat_test)
            p_value = func(reference_data[feature_name], current_data[feature_name])
            p_values[feature_name] = PValueWithConfidence(p_value, confidence)
            current_nbinsx = data_drift_options.get_nbinsx(feature_name)
            features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
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
            confidence = data_drift_options.get_confidence(feature_name)
            feature_ref_data = reference_data[feature_name].dropna()
            feature_cur_data = current_data[feature_name].dropna()
            keys = set(list(feature_ref_data.unique()) +
                       list(feature_cur_data.unique())) - {np.nan}

            if len(keys) > 2:
                # CHI2 to be implemented for cases with different categories
                func = data_drift_options.get_feature_stattest_func(feature_name, chi_stat_test)
            else:
                func = data_drift_options.get_feature_stattest_func(feature_name, z_stat_test)
            p_value = func(feature_ref_data, feature_cur_data)

            p_values[feature_name] = PValueWithConfidence(p_value, confidence)

            features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
                current_small_hist=list(reversed(list(map(list, zip(*feature_ref_data.value_counts().items()))))),
                ref_small_hist=list(reversed(list(map(list, zip(*feature_cur_data.value_counts().items()))))),
                feature_type='cat',
                p_value=p_value
            )

        n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(p_values, drift_share)
        result_metrics = DataDriftAnalyzerMetrics(
            n_features=len(num_feature_names) + len(cat_feature_names),
            n_drifted_features=n_drifted_features,
            share_drifted_features=share_drifted_features,
            dataset_drift=dataset_drift,
            features=features_metrics,
        )
        result = DataDriftAnalyzerResults(
            columns=columns,
            options=data_drift_options,
            metrics=result_metrics,
        )
        return result
