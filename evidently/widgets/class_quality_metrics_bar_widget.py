#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class ClassQualityMetricsBarWidget(Widget):
    def __init__(self, title: str, dataset: str='reference'):
        super().__init__(title)
        self.dataset = dataset #reference or current

    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.dataset == 'reference':
            if self.wi:
                return self.wi
            raise ValueError("no data for quality metrics widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):

        results = analyzers_results[ClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            return
        if self.dataset not in results['metrics'].keys():
            return
        #plot quality metrics bar
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
                    "value": str(round(results['metrics'][self.dataset]['accuracy'], 3)),
                    "label": "Accuracy"
                  },
                  {
                    "value": str(round(results['metrics'][self.dataset]['precision'], 3)),
                    "label": "Precision"
                  },
                  {
                    "value": str(round(results['metrics'][self.dataset]['recall'], 3)),
                    "label": "Recall"
                  },
                  {
                    "value": str(round(results['metrics'][self.dataset]['f1'], 3)),
                    "label": "F1"
                  }
                ]
            },
            additionalGraphs=[],
        )
