#!/usr/bin/env python
# coding: utf-8
import copy
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.calculations.regression_performance import RegressionPerformanceMetrics
from evidently.calculations.regression_performance import calculate_regression_performance
from evidently.utils.data_operations import process_columns


@dataclass
class RegressionPerformanceAnalyzerResults(BaseAnalyzerResult):
    reference_metrics: Optional[RegressionPerformanceMetrics] = None
    current_metrics: Optional[RegressionPerformanceMetrics] = None
    error_bias: Optional[dict] = None


class RegressionPerformanceAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> RegressionPerformanceAnalyzerResults:
        return analyzer_results[RegressionPerformanceAnalyzer]

    def calculate(
        self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> RegressionPerformanceAnalyzerResults:
        columns = process_columns(reference_data, column_mapping)
        result = RegressionPerformanceAnalyzerResults(columns=columns)

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction

        if target_column is not None and prediction_column is not None:
            result.reference_metrics = calculate_regression_performance(
                dataset=reference_data, columns=columns, error_bias_prefix="ref_"
            )

            if result.reference_metrics.error_bias is not None:
                error_bias = copy.deepcopy(result.reference_metrics.error_bias)

            else:
                error_bias = None

            if current_data is not None:
                result.current_metrics = calculate_regression_performance(
                    dataset=current_data, columns=columns, error_bias_prefix="current_"
                )
                if result.current_metrics.error_bias is not None:
                    if error_bias is not None:
                        for feature_name, current_bias in result.current_metrics.error_bias.items():
                            error_bias[feature_name].update(current_bias)

                    else:
                        error_bias = copy.deepcopy(result.current_metrics.error_bias)

            if error_bias:
                result.error_bias = error_bias

            else:
                result.error_bias = {}

        return result
