#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import (
    ClassificationPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class ClassQualityMetricsBarWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        results = ClassificationPerformanceAnalyzer.get_results(analyzers_results)
        target_name = results.columns.utility_columns.target
        prediction_name = results.columns.utility_columns.prediction

        if target_name is None or prediction_name is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns."
                )
            return None

        if self.dataset == "current":
            result_metrics = results.current_metrics

        elif self.dataset == "reference":
            result_metrics = results.reference_metrics

            if not result_metrics:
                raise ValueError(
                    f"Widget [{self.title}] required 'reference' results from"
                    f" {ClassificationPerformanceAnalyzer.__name__} but no data found"
                )

        else:
            raise ValueError(
                f"Widget [{self.title}] requires 'current' or 'reference' dataset value"
            )

        if result_metrics is None:
            return None

        # plot quality metrics bar
        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": str(round(result_metrics.accuracy, 3)),
                        "label": "Accuracy",
                    },
                    {
                        "value": str(round(result_metrics.precision, 3)),
                        "label": "Precision",
                    },
                    {"value": str(round(result_metrics.recall, 3)), "label": "Recall"},
                    {"value": str(round(result_metrics.f1, 3)), "label": "F1"},
                ]
            },
        )
