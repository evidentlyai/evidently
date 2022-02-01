#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceMetrics
from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget


class RegUnderperformMetricsWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.title = title
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)
        results_utility_columns = results.columns.utility_columns

        if results_utility_columns.target is None or results_utility_columns.prediction is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
            return None

        result_metrics = None

        if self.dataset == 'current':
            result_metrics = results.current_metrics
            if result_metrics is None:
                return None

        elif self.dataset == 'reference':
            result_metrics = results.reference_metrics

            if result_metrics is None:
                raise ValueError(f"Widget [{self.title}] required 'reference' results from"
                                 f" {RegressionPerformanceAnalyzer.__name__} but no data found")

        if result_metrics is None:
            raise ValueError(f"Widget [{self.title}] unexpected behaviour. Var 'result_metrics should be set")

        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": _format_value(result_metrics, 'majority'),
                        "label": "Majority(90%)"
                    },
                    {
                        "value": _format_value(result_metrics, 'underestimation'),
                        "label": "Underestimation(5%)"
                    },
                    {
                        "value": _format_value(result_metrics, 'overestimation'),
                        "label": "Overestimation(5%)"
                    }
                ]
            },
        )


def _format_value(results: RegressionPerformanceMetrics, counter_type):
    return f"{round(results.underperformance[counter_type]['mean_error'], 2)}" \
           f" ({round(results.underperformance[counter_type]['std_error'], 2)})"
