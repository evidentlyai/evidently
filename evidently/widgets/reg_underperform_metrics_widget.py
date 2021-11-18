#!/usr/bin/env python
# coding: utf-8

from typing import Optional

import pandas as pd

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class RegUnderperformMetricsWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.title = title
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def get_info(self) -> Optional[BaseWidgetInfo]:
        if self.dataset == 'reference':
            if self.wi:
                return self.wi
            raise ValueError("no data for underperformance quality metrics widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):

        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            return
        if self.dataset not in results['metrics'].keys():
            return
        self.wi = BaseWidgetInfo(
            title=self.title,
            type="counter",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
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
            additionalGraphs=[]
        )


def _format_value(results, dataset, counter_type):
    return f"{round(results['metrics'][dataset]['underperformance'][counter_type]['mean_error'], 2)}" \
           + f" ({round(results['metrics'][dataset]['underperformance'][counter_type]['std_error'], 2)})"
