#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import probplot

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import (
    RegressionPerformanceAnalyzer,
)
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class RegErrorNormalityWidget(Widget):
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
        color_options = self.options_provider.get(ColorOptions)
        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)

        prediction_column = results.columns.utility_columns.prediction
        target_column = results.columns.utility_columns.target

        if target_column is None or prediction_column is None:
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
            axis=0, how="any", inplace=True, subset=[target_column, prediction_column]
        )

        # plot error normality
        error_norm = go.Figure()

        error = dataset_to_plot[prediction_column] - dataset_to_plot[target_column]
        qq_lines = probplot(error, dist="norm", plot=None)
        theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100)

        sample_quantile_trace = go.Scatter(
            x=qq_lines[0][0],
            y=qq_lines[0][1],
            mode="markers",
            name="Dataset Quantiles",
            marker=dict(size=6, color=color_options.primary_color),
        )

        theoretical_quantile_trace = go.Scatter(
            x=theoretical_q_x,
            y=qq_lines[1][0] * theoretical_q_x + qq_lines[1][1],
            mode="lines",
            name="Theoretical Quantiles",
            marker=dict(size=6, color=color_options.secondary_color),
        )

        error_norm.add_trace(sample_quantile_trace)
        error_norm.add_trace(theoretical_quantile_trace)

        error_norm.update_layout(
            xaxis_title="Theoretical Quantiles",
            yaxis_title="Dataset Quantiles",
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
        )

        error_norm_json = json.loads(error_norm.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": error_norm_json["data"],
                "layout": error_norm_json["layout"],
            },
        )
