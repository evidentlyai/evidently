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
from evidently.analyzers.stattests import get_stattest
from evidently.options import DataDriftOptions
from evidently.analyzers.utils import process_columns, recognize_task


def dataset_drift_evaluation(p_values, drift_share=0.5) -> Tuple[int, float, bool]:
    n_drifted_features = sum([1 if x.drifted else 0 for _, x in p_values.items()])
    share_drifted_features = n_drifted_features / len(p_values)
    dataset_drift = bool(share_drifted_features >= drift_share)
    return n_drifted_features, share_drifted_features, dataset_drift


PValueWithDrift = collections.namedtuple("PValueWithDrift", ["p_value", "drifted"])


@dataclass
class DataDriftAnalyzerFeatureMetrics:
    current_small_hist: list
    ref_small_hist: list
    feature_type: str
    stattest_name: str
    p_value: float
    threshold: float
    drift_detected: bool


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
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction
        drift_share = data_drift_options.drift_share

        # define type of target and prediction
        if target_column is not None:
            task = recognize_task(target_column, reference_data)
            if task == 'regression':
                num_feature_names += [target_column]
            else:
                cat_feature_names += [target_column]
        if prediction_column is not None:
            if isinstance(prediction_column, list) and len(prediction_column) > 2:
                reference_data['predicted_labels'] = self._get_pred_labels_from_prob(reference_data, prediction_column)
                current_data['predicted_labels'] = self._get_pred_labels_from_prob(current_data, prediction_column)
                columns.utility_columns.prediction = 'predicted_labels'
                cat_feature_names += [columns.utility_columns.prediction]
            elif isinstance(prediction_column, list) and len(prediction_column) == 2:
                reference_data['prediction'] = reference_data[prediction_column[0]].values
                current_data['prediction'] = current_data[prediction_column[0]].values
                columns.utility_columns.prediction = 'prediction'
                num_feature_names += [columns.utility_columns.prediction]
            elif isinstance(prediction_column, str):
                if reference_data[prediction_column].nunique() > 5:
                    num_feature_names += [prediction_column]
                else:
                    cat_feature_names += [prediction_column]

        # calculate result
        features_metrics = {}
        p_values = {}

        for feature_name in num_feature_names:
            threshold = data_drift_options.get_threshold(feature_name)
            feature_type = "num"
            ref_feature = reference_data[feature_name].replace([-np.inf, np.inf], np.nan).dropna()
            curr_feature = current_data[feature_name].replace([-np.inf, np.inf], np.nan).dropna()
            test = get_stattest(ref_feature,
                                curr_feature,
                                feature_type,
                                data_drift_options.get_feature_stattest_func(feature_name, feature_type))
            drift_result = test(
                ref_feature,
                curr_feature,
                feature_type,
                threshold
            )
            p_value = drift_result.drift_score
            drifted = drift_result.drifted
            threshold = drift_result.actual_threshold
            p_values[feature_name] = PValueWithDrift(p_value, drifted)
            current_nbinsx = data_drift_options.get_nbinsx(feature_name)
            features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
                current_small_hist=[t.tolist() for t in
                                    np.histogram(current_data[feature_name][np.isfinite(current_data[feature_name])],
                                                 bins=current_nbinsx, density=True)],
                ref_small_hist=[t.tolist() for t in
                                np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])],
                                             bins=current_nbinsx, density=True)],
                feature_type='num',
                stattest_name=test.display_name,
                p_value=p_value,
                drift_detected=drifted,
                threshold=threshold,
            )

        for feature_name in cat_feature_names:
            threshold = data_drift_options.get_threshold(feature_name)
            feature_ref_data = reference_data[feature_name].dropna()
            feature_cur_data = current_data[feature_name].dropna()

            feature_type = "cat"
            stat_test = get_stattest(feature_ref_data,
                                     feature_cur_data,
                                     feature_type,
                                     data_drift_options.get_feature_stattest_func(feature_name, feature_type))
            drift_result = stat_test(feature_ref_data, feature_cur_data, feature_type, threshold)
            p_value = drift_result.drift_score
            drifted = drift_result.drifted
            threshold = drift_result.actual_threshold

            p_values[feature_name] = PValueWithDrift(p_value, drifted)

            ref_counts = feature_ref_data.value_counts(sort=False)
            cur_counts = feature_cur_data.value_counts(sort=False)
            keys = set(ref_counts.keys()).union(set(cur_counts.keys()))
            for key in keys:
                if key not in ref_counts:
                    ref_counts[key] = 0
                if key not in cur_counts:
                    cur_counts[key] = 0
            ref_small_hist = list(reversed(list(map(list, zip(*sorted(ref_counts.items(), key=lambda x: x[0]))))))
            cur_small_hist = list(reversed(list(map(list, zip(*sorted(cur_counts.items(), key=lambda x: x[0]))))))
            features_metrics[feature_name] = DataDriftAnalyzerFeatureMetrics(
                ref_small_hist=ref_small_hist,
                current_small_hist=cur_small_hist,
                feature_type='cat',
                stattest_name=stat_test.display_name,
                p_value=p_value,
                drift_detected=drifted,
                threshold=threshold,
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

    @staticmethod
    def _get_pred_labels_from_prob(data: pd.DataFrame, prediction_column: list):
        array_prediction = data[prediction_column].to_numpy()
        prediction_ids = np.argmax(array_prediction, axis=-1)
        prediction_labels = [prediction_column[x] for x in prediction_ids]
        return prediction_labels
