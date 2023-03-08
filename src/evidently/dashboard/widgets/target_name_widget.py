#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import (
    ClassificationPerformanceAnalyzer,
)
from evidently.analyzers.prob_classification_performance_analyzer import (
    ProbClassificationPerformanceAnalyzer,
)
from evidently.analyzers.regression_performance_analyzer import (
    RegressionPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class TargetNameWidget(Widget):
    def __init__(self, title: str, kind: str):
        super().__init__(title)
        self.kind = kind  # regression, classification or prob_classification

    def analyzers(self):
        if self.kind == "regression":
            return [RegressionPerformanceAnalyzer]
        if self.kind == "classification":
            return [ClassificationPerformanceAnalyzer]
        if self.kind == "prob_classification":
            return [ProbClassificationPerformanceAnalyzer]
        raise ValueError(f"Unexpected kind({self.kind}) of TargetNameWidget")

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        results_columns = None

        if self.kind == "regression":
            regression_results = RegressionPerformanceAnalyzer.get_results(
                analyzers_results
            )

            if regression_results:
                results_columns = regression_results.columns

        elif self.kind == "classification":
            classification_results = ClassificationPerformanceAnalyzer.get_results(
                analyzers_results
            )

            if classification_results:
                results_columns = classification_results.columns

        elif self.kind == "prob_classification":
            prob_classification_results = (
                ProbClassificationPerformanceAnalyzer.get_results(analyzers_results)
            )

            if prob_classification_results:
                results_columns = prob_classification_results.columns

        else:
            raise ValueError(f"Unexpected kind({self.kind}) of TagetNameWidget")

        if not results_columns:
            raise ValueError(f"Widget [{self.title}]: analyzer results not found")

        if (
            results_columns.utility_columns.target is None
            or results_columns.utility_columns.prediction is None
        ):
            raise ValueError(
                f"Widget [{self.title}] requires 'target' and 'prediction' columns"
            )

        return BaseWidgetInfo(
            title="",
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": "",
                        "label": self.title
                        + " Target: '"
                        + results_columns.utility_columns.target
                        + "'",
                    }
                ]
            },
        )
