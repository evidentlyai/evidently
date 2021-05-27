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


class ClassConfusionBasedFeatureDistrTable(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def analyzers(self):
        return []

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("neither target nor prediction data provided")

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping, analyzes_results):
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            target_names = column_mapping.get('target_names')
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

            target_names = None

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        if prediction_column is not None and target_column is not None: 
            if production_data is not None:

                additional_graphs_data = []
                params_data = []

                for feature_name in num_feature_names + cat_feature_names: 
                    #add data for table in params
                    labels = sorted(set(reference_data[target_column]))

                    params_data.append(
                        {
                            "details": {
                                    "parts": [{"title":"All", "id":"All" + "_" + str(feature_name)}] + [{"title":str(label), "id": feature_name + "_" + str(label)} for label in labels],
                                    "insights": []
                                },
                            "f1": feature_name
                        }
                        )

                    #create confusion based plots 
                    reference_data['dataset'] = 'Reference'
                    production_data['dataset'] = 'Current'
                    merged_data = pd.concat([reference_data, production_data])

                    fig = px.histogram(merged_data, x=feature_name, color=target_column, facet_col="dataset", histnorm = '',
                        category_orders={"dataset": ["Reference", "Current"]})

                    fig_json  = json.loads(fig.to_json())

                    #write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            "All" + "_" + str(feature_name),
                            {
                                "data" : fig_json['data'],
                                "layout" : fig_json['layout']
                            }, 
                        )
                    )

                    for label in labels:
                        merged_data['Confusion'] = merged_data.apply(lambda x : 'TP' if (x['target'] == label and x['prediction'] == label) 
                                                 else ('FP' if(x['target'] != label and x['prediction'] == label) else \
                                                       ('FN' if (x['target'] == label and x['prediction'] != label) else 'TN')), axis = 1)
                        
                        fig = px.histogram(merged_data, x=feature_name, color='Confusion', facet_col="dataset", histnorm = '',
                            category_orders={"dataset": ["Reference", "Current"], "Confusion": ["TP", "TN", "FP", "FN"]})

                        fig_json  = json.loads(fig.to_json())

                        #write plot data in table as additional data
                        additional_graphs_data.append(
                            AdditionalGraphInfo(
                                feature_name + "_" + str(label),
                                {
                                    "data" : fig_json['data'],
                                    "layout" : fig_json['layout']
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

                additional_graphs_data = []
                params_data = []

                for feature_name in num_feature_names + cat_feature_names: 
                    #add data for table in params
                    labels = sorted(set(reference_data[target_column]))

                    params_data.append(
                        {
                            "details": {
                                    "parts": [{"title":"All", "id":"All" + "_" + str(feature_name)}] + [{"title":str(label), "id": feature_name + "_" + str(label)} for label in labels],
                                    "insights": []
                                },
                            "f1": feature_name
                        }
                        )

                    #create confusion based plots 
                    fig = px.histogram(reference_data, x=feature_name, color=target_column, histnorm = '')

                    fig_json  = json.loads(fig.to_json())

                    #write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            "All" + "_" + str(feature_name),
                            {
                                "data" : fig_json['data'],
                                "layout" : fig_json['layout']
                            }, 
                        )
                    )

                    for label in labels:
                        reference_data['Confusion'] = reference_data.apply(lambda x : 'TP' if (x['target'] == label and x['prediction'] == label) 
                                                 else ('FP' if(x['target'] != label and x['prediction'] == label) else \
                                                       ('FN' if (x['target'] == label and x['prediction'] != label) else 'TN')), axis = 1)
                        
                        fig = px.histogram(reference_data, x=feature_name, color='Confusion', histnorm = '', category_orders={"Confusion": ["TP", "TN", "FP", "FN"]})

                        fig_json  = json.loads(fig.to_json())

                        #write plot data in table as additional data
                        additional_graphs_data.append(
                            AdditionalGraphInfo(
                                feature_name + "_" + str(label),
                                {
                                    "data" : fig_json['data'],
                                    "layout" : fig_json['layout']
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