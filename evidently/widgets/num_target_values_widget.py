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

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class NumTargetValuesWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        #self.wi = None

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        return self.wi
        #raise ValueError("No prediction data provided")

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping): 
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])] 

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])] 
        
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        if target_column is not None:
            #plot drift
            reference_mean = np.mean(reference_data[target_column])
            reference_std = np.std(reference_data[target_column], ddof = 1) 
            x_title = "Timestamp" if date_column else "Index"

            target_values = go.Figure()

            target_values.add_trace(go.Scatter(
                x = reference_data[date_column] if date_column else reference_data.index,
                y = reference_data[target_column],
                mode = 'markers',
                name = 'Reference',
                marker = dict(
                    size = 6,
                    color = grey
                )
            ))

            target_values.add_trace(go.Scatter(
                x = production_data[date_column] if date_column else production_data.index,
                y = production_data[target_column],
                mode = 'markers',
                name = 'Production',
                marker = dict(
                    size = 6,
                    color = red
                )
            ))

            target_values.update_layout(
                xaxis_title = x_title,
                yaxis_title = 'Target Value',
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

            target_values_json  = json.loads(target_values.to_json())

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
                    "data": target_values_json['data'],
                    "layout": target_values_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

