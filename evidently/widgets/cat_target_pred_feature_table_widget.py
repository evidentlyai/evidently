#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare

import plotly.graph_objs as go
import plotly.express as px

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class CatTargetPredFeatureTable(Widget):
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

        if prediction_column is not None and target_column is not None:           
            additional_graphs_data = []
            params_data = []
            for feature_name in num_feature_names + cat_feature_names: 
                #add data for table in params
                params_data.append(
                    {
                        "details": {
                                "parts": [
                                    {
                                        "title": "Target",
                                        "id": feature_name + "_target_values"
                                    },
                                    {
                                        "title": "Prediction",
                                        "id": feature_name + "_prediction_values"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name
                    }
                    )

                #create target plot
                reference_data['dataset'] = 'Reference'
                production_data['dataset'] = 'Production'
                merged_data = pd.concat([reference_data, production_data])

                target_fig = px.histogram(merged_data, x=feature_name, color=target_column, facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Production"]})

                target_fig_json  = json.loads(target_fig.to_json())

                #create prediction plot
                pred_fig = px.histogram(merged_data, x=feature_name, color=prediction_column, facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Production"]})

                pred_fig_json  = json.loads(pred_fig.to_json())

                #write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_target_values',
                        {
                            "data" : target_fig_json['data'],
                            "layout" : target_fig_json['layout']
                        }, 
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_prediction_values',
                        {
                            "data" : pred_fig_json['data'],
                            "layout" : pred_fig_json['layout']
                        }, 
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

        elif target_column is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in num_feature_names + cat_feature_names: 
                #add data for table in params
                params_data.append(
                    {
                        "details": {
                                "parts": [
                                    {
                                        "title": "Target",
                                        "id": feature_name + "_target_values"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name
                    }
                    )

                #create target plot
                reference_data['dataset'] = 'Reference'
                production_data['dataset'] = 'Production'
                merged_data = pd.concat([reference_data, production_data])

                target_fig = px.histogram(merged_data, x=feature_name, color=target_column, facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Production"]})

                target_fig_json  = json.loads(target_fig.to_json())

                #write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_target_values',
                        {
                            "data" : target_fig_json['data'],
                            "layout" : target_fig_json['layout']
                        }, 
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
        elif prediction_column is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in num_feature_names + cat_feature_names: 
                #add data for table in params
                params_data.append(
                    {
                        "details": {
                                "parts": [
                                    {
                                        "title": "Prediction",
                                        "id": feature_name + "_prediction_values"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name
                    }
                    )

                #create target plot
                reference_data['dataset'] = 'Reference'
                production_data['dataset'] = 'Production'
                merged_data = pd.concat([reference_data, production_data])

                prediction_fig = px.histogram(merged_data, x=feature_name, color=prediction_column, facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Production"]})

                prediction_fig_json  = json.loads(prediction_fig.to_json())

                #write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_prediction_values',
                        {
                            "data" : prediction_fig_json['data'],
                            "layout" : prediction_fig_json['layout']
                        }, 
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

        

