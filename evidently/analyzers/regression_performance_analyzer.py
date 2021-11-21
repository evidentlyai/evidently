#!/usr/bin/env python
# coding: utf-8
from dataclasses import dataclass
from typing import Dict

import pandas as pd
import numpy as np
from scipy.stats import probplot

from evidently.analyzers.base_analyzer import Analyzer
from .utils import process_columns


class ErrorWithQuantiles:
    def __init__(self, error, quantile_5, quantile_95):
        self.error = error
        self.quantile_5 = quantile_5
        self.quantile_95 = quantile_95


@dataclass
class FeatureBias:
    feature_type: str
    majority: float
    under: float
    over: float
    range: float

    def as_dict(self, prefix):
        return {
            prefix + 'majority': self.majority,
            prefix + 'under': self.under,
            prefix + 'over': self.over,
            prefix + 'range': self.range
        }


class RegressionPerformanceAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        num_feature_names = columns.num_feature_names
        cat_feature_names = columns.cat_feature_names

        result['metrics'] = {}
        if target_column is not None and prediction_column is not None:
            _prepare_dataset(reference_data)

            # calculate quality metrics
            result['metrics']['reference'] = _calculate_quality_metrics(reference_data, prediction_column,
                                                                        target_column)

            # error normality
            err_quantiles = _error_with_qantiles(reference_data, prediction_column, target_column)

            result['metrics']['reference']['error_normality'] = _calculate_error_normality(err_quantiles)

            # underperformance metrics
            result['metrics']['reference']['underperformance'] = _calculate_underperformance(err_quantiles)

            # error bias table
            error_bias = {}
            ref_feature_bias = _error_bias_table(reference_data, err_quantiles, num_feature_names, cat_feature_names)
            # convert to old format
            error_bias = {feature: dict(feature_type=bias.feature_type, **bias.as_dict('ref_'))
                          for feature, bias in ref_feature_bias.items()}

            if current_data is not None:
                _prepare_dataset(current_data)

                # calculate quality metrics
                result['metrics']['current'] = _calculate_quality_metrics(current_data, prediction_column,
                                                                          target_column)

                # error normality
                current_err_quantiles = _error_with_qantiles(current_data, prediction_column, target_column)
                result['metrics']['current']['error_normality'] = _calculate_error_normality(current_err_quantiles)

                # underperformance metrics
                result['metrics']['current']['underperformance'] = _calculate_underperformance(current_err_quantiles)

                # error bias table
                current_feature_bias = _error_bias_table(current_data, current_err_quantiles, num_feature_names,
                                                         cat_feature_names)
                for feature, bias in current_feature_bias.items():
                    ref_bias = error_bias.get(feature, {})
                    ref_bias.update(bias.as_dict("current_"))
                    error_bias[feature] = ref_bias

            result['metrics']['error_bias'] = error_bias

        return result


def _calculate_error_normality(error: ErrorWithQuantiles):
    qq_lines = probplot(error.error, dist="norm", plot=None)
    # theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100) # TODO: review  unused?

    qq_dots = [t.tolist() for t in qq_lines[0]]
    qq_line = list(qq_lines[1])
    return {
        'order_statistic_medians_x': [float(x) for x in qq_dots[0]],
        'order_statistic_medians_y': [float(x) for x in qq_dots[1]],
        'slope': float(qq_line[0]),
        'intercept': float(qq_line[1]),
        'r': float(qq_line[2])
    }


def _calculate_quality_metrics(dataset, prediction_column, target_column):
    me = np.mean(dataset[prediction_column] - dataset[target_column])
    sde = np.std(dataset[prediction_column] - dataset[target_column], ddof=1)

    abs_err = np.abs(dataset[prediction_column] - dataset[target_column])
    mae = np.mean(abs_err)
    sdae = np.std(abs_err, ddof=1)

    abs_perc_err = 100. * np.abs(dataset[prediction_column] - dataset[target_column]) / dataset[target_column]
    mape = np.mean(abs_perc_err)
    sdape = np.std(abs_perc_err, ddof=1)

    return {
        'mean_error': float(me),
        'mean_abs_error': float(mae),
        'mean_abs_perc_error': float(mape),
        'error_std': float(sde),
        'abs_error_std': float(sdae),
        'abs_perc_error_std': float(sdape)
    }


def _prepare_dataset(dataset):
    dataset.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataset.dropna(axis=0, how='any', inplace=True)


def _calculate_underperformance(err_quantiles: ErrorWithQuantiles):
    error = err_quantiles.error
    quantile_5 = err_quantiles.quantile_5
    quantile_95 = err_quantiles.quantile_95
    mae_under = np.mean(error[error <= quantile_5])
    mae_exp = np.mean(error[(error > quantile_5) & (error < quantile_95)])
    mae_over = np.mean(error[error >= quantile_95])

    sd_under = np.std(error[error <= quantile_5], ddof=1)
    sd_exp = np.std(error[(error > quantile_5) & (error < quantile_95)], ddof=1)
    sd_over = np.std(error[error >= quantile_95], ddof=1)

    return {
        'majority': {'mean_error': float(mae_exp), 'std_error': float(sd_exp)},
        'underestimation': {'mean_error': float(mae_under), 'std_error': float(sd_under)},
        'overestimation': {'mean_error': float(mae_over), 'std_error': float(sd_over)}
    }


def _error_bias_table(dataset, err_quantiles, num_feature_names, cat_feature_names) -> Dict[str, FeatureBias]:
    num_bias = {feature_name: _error_num_feature_bias(dataset, feature_name, err_quantiles)
                for feature_name in num_feature_names}
    cat_bias = {feature_name: _error_cat_feature_bias(dataset, feature_name, err_quantiles)
                for feature_name in cat_feature_names}
    error_bias = num_bias.copy()
    error_bias.update(cat_bias)
    return error_bias


def _error_num_feature_bias(dataset, feature_name, err_quantiles: ErrorWithQuantiles) -> FeatureBias:
    error = err_quantiles.error
    quantile_5 = err_quantiles.quantile_5
    quantile_95 = err_quantiles.quantile_95
    ref_overal_value = np.mean(dataset[feature_name])
    ref_under_value = np.mean(dataset[error <= quantile_5][feature_name])
    # ref_expected_value = np.mean(dataset[(error > quantile_5) & (error < quantile_95)][feature_name])
    ref_over_value = np.mean(dataset[error >= quantile_95][feature_name])
    if ref_over_value == ref_under_value:
        ref_range_value = 0
    else:
        ref_range_value = 100 * abs(ref_over_value - ref_under_value) / (np.max(dataset[feature_name])
                                                                         - np.min(dataset[feature_name]))

    return FeatureBias(
        feature_type='num',
        majority=float(ref_overal_value),
        under=float(ref_under_value),
        over=float(ref_over_value),
        range=float(ref_range_value))


def _error_cat_feature_bias(dataset, feature_name, err_quantiles: ErrorWithQuantiles) -> FeatureBias:
    error = err_quantiles.error
    quantile_5 = err_quantiles.quantile_5
    quantile_95 = err_quantiles.quantile_95
    ref_overal_value = dataset[feature_name].value_counts().idxmax()
    ref_under_value = dataset[error <= quantile_5][feature_name].value_counts().idxmax()
    ref_over_value = dataset[error >= quantile_95][feature_name].value_counts().idxmax()
    if (ref_overal_value != ref_under_value) or (ref_over_value != ref_overal_value)\
            or (ref_under_value != ref_overal_value):
        ref_range_value = 1
    else:
        ref_range_value = 0

    return FeatureBias(
        feature_type='cat',
        majority=float(ref_overal_value),
        under=float(ref_under_value),
        over=float(ref_over_value),
        range=float(ref_range_value))


def _error_with_qantiles(dataset, prediction_column, target_column):
    error = dataset[prediction_column] - dataset[target_column]

    # underperformance metrics
    quantile_5 = np.quantile(error, .05)
    quantile_95 = np.quantile(error, .95)
    return ErrorWithQuantiles(error, quantile_5, quantile_95)
