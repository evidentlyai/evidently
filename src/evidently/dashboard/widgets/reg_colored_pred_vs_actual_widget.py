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


class RegColoredPredActualWidget(Widget):
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

        error = dataset_to_plot[results_utility_columns.prediction] - dataset_to_plot[results_utility_columns.target]

        quantile_5 = np.quantile(error, .05)
        quantile_95 = np.quantile(error, .95)

        dataset_to_plot['Error bias'] = list(map(
            lambda x: 'Underestimation'
                      if x <= quantile_5 else 'Majority'
                      if x < quantile_95 else 'Overestimation', error))

        # plot output correlations
        pred_actual = go.Figure()

        pred_actual.add_trace(go.Scatter(
            x=dataset_to_plot[dataset_to_plot['Error bias'] == 'Underestimation'][results_utility_columns.target],
            y=dataset_to_plot[dataset_to_plot['Error bias'] == 'Underestimation'][results_utility_columns.prediction],
            mode='markers',
            name='Underestimation',
            marker=dict(
                color='#6574f7',
                showscale=False
            )
        ))

        pred_actual.add_trace(go.Scatter(
            x=dataset_to_plot[dataset_to_plot['Error bias'] == 'Overestimation'][results_utility_columns.target],
            y=dataset_to_plot[dataset_to_plot['Error bias'] == 'Overestimation'][results_utility_columns.prediction],
            mode='markers',
            name='Overestimation',
            marker=dict(
                color='#ee5540',
                showscale=False
            )
        ))

        pred_actual.add_trace(go.Scatter(
            x=dataset_to_plot[dataset_to_plot['Error bias'] == 'Majority'][results_utility_columns.target],
            y=dataset_to_plot[dataset_to_plot['Error bias'] == 'Majority'][results_utility_columns.prediction],
            mode='markers',
            name='Majority',
            marker=dict(
                color='#1acc98',
                showscale=False
            )
        ))

        pred_actual.update_layout(
            xaxis_title="Actual value",
            yaxis_title="Predicted value",
            xaxis=dict(
                showticklabels=True
            ),
            yaxis=dict(
                showticklabels=True
            ),
        )

        pred_actual_json = json.loads(pred_actual.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1 if current_data is not None else 2,
            params={
                "data": pred_actual_json['data'],
                "layout": pred_actual_json['layout']
            },
            additionalGraphs=[],
        )
