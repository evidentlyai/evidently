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
from evidently.dashboard.widgets.widget import Widget, RED


class RegAbsPercErrorTimeWidget(Widget):
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

        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
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

        # plot absolute error in time
        abs_perc_error_time = go.Figure()

        abs_perc_error = 100. * np.abs(
            dataset_to_plot[results['utility_columns']['prediction']]
            - dataset_to_plot[results['utility_columns']['target']]
        ) / dataset_to_plot[results['utility_columns']['target']]

        error_trace = go.Scatter(
            x=dataset_to_plot[results['utility_columns']['date']] if results['utility_columns'][
                'date'] else dataset_to_plot.index,
            y=abs_perc_error,
            mode='lines',
            name='Absolute Percentage Error',
            marker=dict(
                size=6,
                color=RED
            )
        )

        zero_trace = go.Scatter(
            x=dataset_to_plot[results['utility_columns']['date']] if results['utility_columns'][
                'date'] else dataset_to_plot.index,
            y=[0] * dataset_to_plot.shape[0],
            mode='lines',
            opacity=0.5,
            marker=dict(
                size=6,
                color='green',
            ),
            showlegend=False,
        )

        abs_perc_error_time.add_trace(error_trace)
        abs_perc_error_time.add_trace(zero_trace)

        abs_perc_error_time.update_layout(
            xaxis_title="Timestamp" if results['utility_columns']['date'] else "Index",
            yaxis_title="Percent",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        abs_perc_error_time_json = json.loads(abs_perc_error_time.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": abs_perc_error_time_json['data'],
                "layout": abs_perc_error_time_json['layout']
            },
            additionalGraphs=[],
        )
