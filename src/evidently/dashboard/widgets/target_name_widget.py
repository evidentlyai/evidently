#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget


class TargetNameWidget(Widget):
    def __init__(self, title: str, kind: str):
        super().__init__(title)
        self.kind = kind  # regression, classification or prob_classification

    def analyzers(self):
        if self.kind == 'regression':
            return [RegressionPerformanceAnalyzer]
        if self.kind == 'classification':
            return [ClassificationPerformanceAnalyzer]
        if self.kind == 'prob_classification':
            return [ProbClassificationPerformanceAnalyzer]
        raise ValueError(f"Unexpected kind({self.kind}) of TargetNameWidget")

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        if self.kind == 'regression':
            results = analyzers_results[RegressionPerformanceAnalyzer]
        elif self.kind == 'classification':
            results = analyzers_results[ClassificationPerformanceAnalyzer]
        elif self.kind == 'prob_classification':
            results = analyzers_results[ProbClassificationPerformanceAnalyzer]
        else:
            raise ValueError(f"Unexpected kind({self.kind}) of TagetNameWidget")

        if not results:
            raise ValueError(f"Widget [{self.title}]: analyzer results not found")
        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
        return BaseWidgetInfo(
            title="",
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": "",
                        "label": self.title + " Target: '" + results['utility_columns']['target'] + "'"
                    }
                ]
            },
        )
