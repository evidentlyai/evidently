#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import numpy as np

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget
from evidently.options import ColorOptions


class RegErrorTimeWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = RegressionPerformanceAnalyzer.get_results(analyzers_results)
        results_utility_columns = results.columns.utility_columns

        if results_utility_columns.target is None or results_utility_columns.prediction is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")

            return None

        if self.dataset == 'current':
            dataset_to_plot = current_data.copy(deep=False) if current_data is not None else None

        else:
            dataset_to_plot = reference_data.copy(deep=False)

        if dataset_to_plot is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires reference dataset but it is None")
            return None

        dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataset_to_plot.dropna(axis=0, how='any', inplace=True)

        # plot error in time
        error_in_time = go.Figure()

        error_trace = go.Scatter(
            x=dataset_to_plot[results_utility_columns.date] if results_utility_columns.date else dataset_to_plot.index,
            y=dataset_to_plot[results_utility_columns.prediction] - dataset_to_plot[results_utility_columns.target],
            mode='lines',
            name='Predicted - Actual',
            marker=dict(
                size=6,
                color=color_options.primary_color
            )
        )

        zero_trace = go.Scatter(
            x=dataset_to_plot[results_utility_columns.date] if results_utility_columns.date else dataset_to_plot.index,
            y=[0] * dataset_to_plot.shape[0],
            mode='lines',
            opacity=0.5,
            marker=dict(
                size=6,
                color=color_options.zero_line_color,
            ),
            showlegend=False,
        )

        error_in_time.add_trace(error_trace)
        error_in_time.add_trace(zero_trace)

        error_in_time.update_layout(
            xaxis_title="Timestamp" if results_utility_columns.date else "Index",
            yaxis_title="Error",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        error_in_time_json = json.loads(error_in_time.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": error_in_time_json['data'],
                "layout": error_in_time_json['layout']
            },
            additionalGraphs=[],
        )
