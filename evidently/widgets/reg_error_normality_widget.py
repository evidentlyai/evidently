#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, probplot
import plotly.graph_objs as go
#import plotly.figure_factory as ff

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class RegErrorNormalityWidget(Widget):
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
            raise ValueError("no data for predicted and actual in time widget provided")
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

                #plot error normality
                error_norm = go.Figure()

                error = dataset_to_plot[results['utility_columns']['prediction']] - dataset_to_plot[results['utility_columns']['target']] 
                qq_lines = probplot(error, dist="norm", plot=None)
                theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100)

                sample_quantile_trace = go.Scatter(
                    x = qq_lines[0][0],
                    y = qq_lines[0][1],
                    mode = 'markers',
                    name = 'Dataset Quantiles',
                    marker=dict(
                        size=6,
                        color=red
                    )
                )

                theoretical_quantile_trace = go.Scatter(
                    x = theoretical_q_x,
                    y = qq_lines[1][0]*theoretical_q_x + qq_lines[1][1],
                    mode = 'lines',
                    name = 'Theoretical Quantiles',
                    marker=dict(
                        size=6,
                        color=grey
                    )
                )

                error_norm.add_trace(sample_quantile_trace)
                error_norm.add_trace(theoretical_quantile_trace)

                error_norm.update_layout(
                    xaxis_title = "Theoretical Quantiles",
                    yaxis_title = "Dataset Quantiles",

                    legend = dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                    )
                )

                error_norm_json = json.loads(error_norm.to_json())

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
                        "data": error_norm_json['data'],
                        "layout": error_norm_json['layout']
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

