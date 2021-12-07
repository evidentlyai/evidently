#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.options import DataDriftOptions
from evidently.analyzers.stattests import chi_stat_test, ks_stat_test, z_stat_test
from evidently.analyzers.utils import process_columns


def dataset_drift_evaluation(p_values, confidence=0.95, drift_share=0.5):
    n_drifted_features = sum([1 if x < (1. - confidence) else 0 for x in p_values])
    share_drifted_features = n_drifted_features / len(p_values)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


class DataDriftAnalyzerResults:
    pass


class DataDriftAnalyzer(Analyzer):
    results: DataDriftAnalyzerResults

    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping: ColumnMapping):
        options = self.options_provider.get(DataDriftOptions)
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        num_feature_names = columns.num_feature_names
        cat_feature_names = columns.cat_feature_names
        nbinsx = options.nbinsx
        confidence = options.confidence
        drift_share = options.drift_share
        # calculate result
        result['metrics'] = {}

        p_values = []

        for feature_name in num_feature_names:
            func = None if options.feature_stattest_func is None \
                else options.feature_stattest_func.get(feature_name, None)
            func = options.stattest_func if func is None else func
            func = ks_stat_test if func is None else func
            p_value = func(reference_data[feature_name], current_data[feature_name])
            p_values.append(p_value)
            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name] = dict(
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
            func = None if options.feature_stattest_func is None \
                else options.feature_stattest_func.get(feature_name, None)
            func = options.stattest_func if func is None else func
            keys = set(list(reference_data[feature_name][np.isfinite(reference_data[feature_name])].unique()) +
                       list(current_data[feature_name][np.isfinite(current_data[feature_name])].unique()))

            if len(keys) > 2:
                # CHI2 to be implemented for cases with different categories
                func = chi_stat_test if func is None else func
                p_value = func(reference_data[feature_name], current_data[feature_name])
            else:
                func = z_stat_test if func is None else func
                p_value = func(reference_data[feature_name], current_data[feature_name])

            p_values.append(p_value)

            if nbinsx:
                current_nbinsx = nbinsx.get(feature_name) if nbinsx.get(feature_name) else 10
            else:
                current_nbinsx = 10
            result['metrics'][feature_name] = dict(
                current_small_hist=[t.tolist() for t in
                                    np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                                 bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in
                                np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                feature_type='cat',
                p_value=p_value
            )

        n_drifted_features, share_drifted_features, dataset_drift = dataset_drift_evaluation(p_values, confidence,
                                                                                             drift_share)
        result['metrics']['n_features'] = len(num_feature_names) + len(cat_feature_names)
        result['metrics']['n_drifted_features'] = n_drifted_features
        result['metrics']['share_drifted_features'] = share_drifted_features
        result['metrics']['dataset_drift'] = dataset_drift
        return result
