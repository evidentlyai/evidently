#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget


class ProbClassQualityMetricBarWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[ProbClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")
            return None
        if self.dataset not in results['metrics'].keys():
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] required 'reference' results from"
                                 f" {ProbClassificationPerformanceAnalyzer.__name__} but no data found")
            return None
        return BaseWidgetInfo(
            title=self.title,
            type="counter",
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
                    },
                    {
                        "value": str(round(results['metrics'][self.dataset]['roc_auc'], 3)),
                        "label": "ROC AUC"
                    },
                    {
                        "value": str(round(results['metrics'][self.dataset]['log_loss'], 3)),
                        "label": "LogLoss"
                    }
                ]
            },
        )
