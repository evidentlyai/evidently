#!/usr/bin/env python
# coding: utf-8
from typing import Optional

from dataclasses import dataclass
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.analyzers.utils import process_columns
from evidently.metrics.calculations.regression_performance import calculate_regression_performance
from evidently.metrics.calculations.regression_performance import RegressionPerformanceMetrics


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
            error_bias = result.reference_metrics.error_bias

            if current_data is not None:
                result.current_metrics = calculate_regression_performance(
                    dataset=current_data, columns=columns, error_bias_prefix="current_"

                )
                if error_bias is not None:
                    for feature_name, current_bias in result.current_metrics.error_bias.items():
                        error_bias[feature_name].update(current_bias)

            if error_bias:
                result.error_bias = error_bias

            else:
                result.error_bias = {}

        return result
