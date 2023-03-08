#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import (
    ProbClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class ProbClassQualityMetricBarWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        results = ProbClassificationPerformanceAnalyzer.get_results(analyzers_results)
        utility_columns = results.columns.utility_columns

        if utility_columns.target is None or utility_columns.prediction is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns"
                )

            return None

        if self.dataset == "reference":
            metrics = results.reference_metrics

            if metrics is None:
                raise ValueError(
                    f"Widget [{self.title}] required 'reference' results from"
                    f" {ProbClassificationPerformanceAnalyzer.__name__} but no data found"
                )

        elif self.dataset == "current":
            metrics = results.current_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] required 'current' or 'reference' dataset value"
            )

        if metrics is None:
            return None

        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {"value": str(round(metrics.accuracy, 3)), "label": "Accuracy"},
                    {"value": str(round(metrics.precision, 3)), "label": "Precision"},
                    {"value": str(round(metrics.recall, 3)), "label": "Recall"},
                    {"value": str(round(metrics.f1, 3)), "label": "F1"},
                    {"value": str(round(metrics.roc_auc, 3)), "label": "ROC AUC"},
                    {"value": str(round(metrics.log_loss, 3)), "label": "LogLoss"},
                ]
            },
        )
