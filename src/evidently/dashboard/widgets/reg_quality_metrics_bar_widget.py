#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import (
    RegressionPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class RegQualityMetricsBarWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)

        if (
            results.columns.utility_columns.target is None
            or results.columns.utility_columns.prediction is None
        ):
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns"
                )
            return None

        if self.dataset == "reference":
            results_metrics = results.reference_metrics

        elif self.dataset == "current":
            results_metrics = results.current_metrics

        else:
            raise ValueError(
                f"Widget [{self.title}] required '{self.dataset}' results from"
                f" {RegressionPerformanceAnalyzer.__name__} but no data found"
            )

        if results_metrics is None:
            return None

        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": f"{round(results_metrics.mean_error, 2)}"
                        f" ({round(results_metrics.error_std, 2)})",
                        "label": "ME",
                    },
                    {
                        "value": f"{round(results_metrics.mean_abs_error, 2)}"
                        f" ({round(results_metrics.abs_error_std, 2)})",
                        "label": "MAE",
                    },
                    {
                        "value": f"{round(results_metrics.mean_abs_perc_error, 2)}"
                        f" ({round(results_metrics.abs_perc_error_std, 2)})",
                        "label": "MAPE",
                    },
                ]
            },
        )
