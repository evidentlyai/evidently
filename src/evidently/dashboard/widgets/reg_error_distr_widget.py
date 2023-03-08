#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import (
    RegressionPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class RegErrorDistrWidget(Widget):
    def __init__(self, title: str, dataset: str = "reference"):
        super().__init__(title)
        self.title = title
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
        color_options = self.options_provider.get(ColorOptions)
        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)
        results_utility_columns = results.columns.utility_columns

        if (
            results_utility_columns.target is None
            or results_utility_columns.prediction is None
        ):
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires 'target' and 'prediction' columns"
                )

            return None

        if self.dataset == "current":
            dataset_to_plot = (
                current_data.copy(deep=False) if current_data is not None else None
            )

        else:
            dataset_to_plot = reference_data.copy(deep=False)

        if dataset_to_plot is None:
            if self.dataset == "reference":
                raise ValueError(
                    f"Widget [{self.title}] requires reference dataset but it is None"
                )

            return None

        dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataset_to_plot.dropna(
            axis=0,
            how="any",
            inplace=True,
            subset=[results_utility_columns.target, results_utility_columns.prediction],
        )

        # plot distributions
        error_distr = go.Figure()

        error = (
            dataset_to_plot[results_utility_columns.prediction]
            - dataset_to_plot[results_utility_columns.target]
        )

        error_distr.add_trace(
            go.Histogram(
                x=error,
                marker_color=color_options.primary_color,
                name="error distribution",
                histnorm="percent",
            )
        )

        error_distr.update_layout(
            xaxis_title="Error (Predicted - Actual)",
            yaxis_title="Percentage",
        )

        error_distr_json = json.loads(error_distr.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": error_distr_json["data"],
                "layout": error_distr_json["layout"],
            },
        )
