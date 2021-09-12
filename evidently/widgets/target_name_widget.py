#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class TargetNameWidget(Widget):
    def __init__(self, title: str, kind: str):
        super().__init__(title)
        self.kind = kind #regression, classification or prob_classification

    def analyzers(self):
        if self.kind == 'regression':
            return[RegressionPerformanceAnalyzer]
        elif self.kind == 'classification':
            return[ClassificationPerformanceAnalyzer]
        elif self.kind == 'prob_classification':
            return[ProbClassificationPerformanceAnalyzer]
        else:
            raise ValueError(f"Unexpected kind({self.kind}) of TagetNameWidget")

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):

        if self.kind == 'regression':
            results = analyzers_results[RegressionPerformanceAnalyzer]
        elif self.kind == 'classification':
            results = analyzers_results[ClassificationPerformanceAnalyzer]
        elif self.kind == 'prob_classification':
            results = analyzers_results[ProbClassificationPerformanceAnalyzer]
        else:
            raise ValueError(f"Unexpected kind({self.kind}) of TagetNameWidget")

        if not results:
            return
        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            return
        self.wi = BaseWidgetInfo(
            title="",
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
                    "value": "",
                    "label": self.title + " Target: '" + results['utility_columns']['target'] + "'"
                    }
                ]
            },
            additionalGraphs=[],
        )
