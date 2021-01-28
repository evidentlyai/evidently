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


class RegRefErrorTimeWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("No prediction data provided")

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

        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)
            
            #plot output correlations
            pred_actual_time = go.Figure()

            error_trace = go.Scatter(
                x = reference_data[date_column] if date_column else reference_data.index,
                y = reference_data[prediction_column] - reference_data[target_column],
                mode = 'lines',
                name = 'Predicted - Actual',
                marker=dict(
                    size=6,
                    color=red
                )
            )

            zero_trace = go.Scatter(
                x = reference_data[date_column] if date_column else reference_data.index,
                y = [0]*reference_data.shape[0],
                mode = 'lines',
                opacity=0.5,
                marker=dict(
                    size=6,
                    color='green',
                ),
                showlegend=False,
            )

            pred_actual_time.add_trace(error_trace)
            pred_actual_time.add_trace(zero_trace)

            pred_actual_time.update_layout(
                xaxis_title = "Timestamp" if date_column else "Index",
                yaxis_title = "Error",
                legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                )
            )

            pred_actual_time_json = json.loads(pred_actual_time.to_json())

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
                    "data": pred_actual_time_json['data'],
                    "layout": pred_actual_time_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

