#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class NumTargetPredFeatureTable(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("neither target nor prediction data provided")

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

        if prediction_column is not None or target_column is not None:           
            additional_graphs_data = []
            params_data = []
            for feature_name in num_feature_names + cat_feature_names: 
                #add data for table in params
                params_data.append(
                    {
                        "details": {
                                "parts": [
                                    {
                                        "title": "Feature values",
                                        "id": feature_name + "_values"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name
                    }
                    )

                #create plot
                fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Production"))

                if prediction_column is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = reference_data[feature_name],
                        y = reference_data[prediction_column],
                        mode = 'markers',
                        name = 'Prediction (ref)',
                        marker = dict(
                            size = 6,
                            color = grey
                            )
                        ),
                        row=1, col=1
                    )

                if target_column is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = reference_data[feature_name],
                        y = reference_data[target_column],
                        mode = 'markers',
                        name = 'Target (ref)',
                        marker = dict(
                            size = 6,
                            color = red
                            )
                        ),
                        row=1, col=1
                    )

                if prediction_column is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = production_data[feature_name],
                        y = production_data[prediction_column],
                        mode = 'markers',
                        name = 'Prediction (prod)',
                        marker = dict(
                            size = 6,
                            color = grey
                            )
                        ),
                        row=1, col=2
                    )

                if target_column is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = production_data[feature_name],
                        y = production_data[target_column],
                        mode = 'markers',
                        name = 'Target (prod)',
                        marker = dict(
                            size = 6,
                            color = red
                            )
                        ),
                        row=1, col=2
                    )

                # Update xaxis properties
                fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)
                fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=2)

                # Update yaxis properties
                fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=1)
                fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=2)

                fig_json  = json.loads(fig.to_json())

                #write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_values',
                        {
                            "data" : fig_json['data'],
                            "layout" : fig_json['layout']
                        }
                    )
                )

            self.wi = BaseWidgetInfo(
                title=self.title,
                type="big_table",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=2,
                params={
                    "rowsPerPage" : min(len(num_feature_names) + len(cat_feature_names), 10),
                    "columns": [
                        {
                            "title": "Feature",
                            "field": "f1"
                        }
                    ],
                    "data": params_data
                },
                additionalGraphs=additional_graphs_data
            )

        else:
            self.wi = None

        

