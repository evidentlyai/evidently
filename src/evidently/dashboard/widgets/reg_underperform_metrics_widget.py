#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
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

        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
            return None
        if self.dataset not in results['metrics'].keys():
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] required 'reference' results from"
                                 f" {RegressionPerformanceAnalyzer.__name__} but no data found")
            return None

        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": _format_value(results, self.dataset, 'majority'),
                        "label": "Majority(90%)"
                    },
                    {
                        "value": _format_value(results, self.dataset, 'underestimation'),
                        "label": "Underestimation(5%)"
                    },
                    {
                        "value": _format_value(results, self.dataset, 'overestimation'),
                        "label": "Overestimation(5%)"
                    }
                ]
            },
        )


def _format_value(results, dataset, counter_type):
    return f"{round(results['metrics'][dataset]['underperformance'][counter_type]['mean_error'], 2)}" \
           + f" ({round(results['metrics'][dataset]['underperformance'][counter_type]['std_error'], 2)})"
