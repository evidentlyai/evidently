#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class NumOutputValuesWidget(Widget):
    def __init__(self, title:str, kind:str = 'target'):
        super().__init__()
        self.title = title
        self.kind = kind #target or prediction

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        #    return self.wi
        #raise ValueError("no widget info provided")
        return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[NumTargetDriftAnalyzer]

        if results['utility_columns'][self.kind] is not None:
            #plot values
            reference_mean = np.mean(reference_data[results['utility_columns'][self.kind]])
            reference_std = np.std(reference_data[results['utility_columns'][self.kind]], ddof = 1) 
            x_title = "Timestamp" if results['utility_columns']['date'] else "Index"

            output_values = go.Figure()

            output_values.add_trace(go.Scatter(
                x = reference_data[results['utility_columns']['date']] if results['utility_columns']['date'] else reference_data.index,
                y = reference_data[results['utility_columns'][self.kind]],
                mode = 'markers',
                name = 'Reference',
                marker = dict(
                    size = 6,
                    color = grey
                )
            ))

            output_values.add_trace(go.Scatter(
                x = current_data[results['utility_columns']['date']] if results['utility_columns']['date'] else current_data.index,
                y = current_data[results['utility_columns'][self.kind]],
                mode = 'markers',
                name = 'Current',
                marker = dict(
                    size = 6,
                    color = red
                )
            ))

            output_values.update_layout(
                xaxis_title = x_title,
                yaxis_title = self.kind.title() + ' Value',
                showlegend = True,
                legend = dict(
                orientation = "h",
                yanchor = "bottom",
                y=1.02,
                xanchor = "right",
                x = 1
                ),
                shapes = [
                    dict(
                        type = "rect",
                        # x-reference is assigned to the x-values
                        xref = "paper",
                        # y-reference is assigned to the plot paper [0,1]
                        yref = "y",
                        x0 = 0, 
                        y0 = reference_mean - reference_std, 
                        x1 = 1, 
                        y1 = reference_mean + reference_std, 
                        fillcolor = "LightGreen",
                        opacity = 0.5,
                        layer = "below",
                        line_width = 0,
                    ),
                    dict(
                        type="line",
                        name = 'Reference',
                        xref = "paper",
                        yref = "y",
                        x0 = 0, #min(testset_agg_by_date.index),
                        y0 = reference_mean,
                        x1 = 1, #max(testset_agg_by_date.index),
                        y1 = reference_mean,
                        line = dict(
                            color = "Green",
                            width = 3
                            )
                    ),
                ]  
            )

            output_values_json  = json.loads(output_values.to_json())

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
                    "data": output_values_json['data'],
                    "layout": output_values_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

