#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

import plotly.graph_objs as go

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class RegErrorTimeWidget(Widget):
    def __init__(self, title:str, dataset:str='reference'):
        super().__init__()
        self.title = title
        self.dataset = dataset #reference or current

    def analyzers(self):   
        return [RegressionPerformanceAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.dataset == 'reference':
            if self.wi:
                return self.wi
            raise ValueError("no data for predicted vs actual widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
            if self.dataset == 'current':
                dataset_to_plot = current_data.copy(deep=False) if current_data is not None else None
            else:
                dataset_to_plot = reference_data.copy(deep=False)

            if dataset_to_plot is not None:
                dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
                dataset_to_plot.dropna(axis=0, how='any', inplace=True)
            
                #plot error in time
                error_in_time = go.Figure()

                error_trace = go.Scatter(
                    x = dataset_to_plot[results['utility_columns']['date']] if results['utility_columns']['date'] else dataset_to_plot.index,
                    y = dataset_to_plot[results['utility_columns']['prediction']] - dataset_to_plot[results['utility_columns']['target']],
                    mode = 'lines',
                    name = 'Predicted - Actual',
                    marker=dict(
                        size=6,
                        color=red
                    )
                )

                zero_trace = go.Scatter(
                    x = dataset_to_plot[results['utility_columns']['date']] if results['utility_columns']['date'] else dataset_to_plot.index,
                    y = [0]*dataset_to_plot.shape[0],
                    mode = 'lines',
                    opacity=0.5,
                    marker=dict(
                        size=6,
                        color='green',
                    ),
                    showlegend=False,
                )

                error_in_time.add_trace(error_trace)
                error_in_time.add_trace(zero_trace)

                error_in_time.update_layout(
                    xaxis_title = "Timestamp" if results['utility_columns']['date'] else "Index",
                    yaxis_title = "Error",
                    legend = dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                    )
                )

                error_in_time_json = json.loads(error_in_time.to_json())

                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="big_graph",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1,
                    params={
                        "data": error_in_time_json['data'],
                        "layout": error_in_time_json['layout']
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

