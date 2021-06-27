#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare

import plotly.graph_objs as go
import plotly.express as px

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ClassConfusionBasedFeatureDistrTable(Widget):
    def __init__(self, title:str):
        super().__init__()
        self.title = title

    def analyzers(self):   
        return [ClassificationPerformanceAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no data for quality metrics widget provided")


    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[ClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None: 
            if current_data is not None:

                additional_graphs_data = []
                params_data = []

                for feature_name in results['num_feature_names'] + results['cat_feature_names']: 
                    #add data for table in params
                    labels = sorted(set(reference_data[results['utility_columns']['target']]))

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
                    current_data['dataset'] = 'Current'
                    merged_data = pd.concat([reference_data, current_data])

                    fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['target'], facet_col="dataset", histnorm = '',
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
                        merged_data['Confusion'] = merged_data.apply(lambda x : 'TP' if (x[results['utility_columns']['target']] == label and x[results['utility_columns']['prediction']] == label) 
                                                 else ('FP' if(x[results['utility_columns']['target']] != label and x[results['utility_columns']['prediction']] == label) else \
                                                       ('FN' if (x[results['utility_columns']['target']] == label and x[results['utility_columns']['prediction']] != label) else 'TN')), axis = 1)
                        
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
                        "rowsPerPage" : min(len(results['num_feature_names']) + len(results['cat_feature_names']), 10),
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

                for feature_name in results['num_feature_names'] + results['cat_feature_names']: 
                    #add data for table in params
                    labels = sorted(set(reference_data[results['utility_columns']['target']]))

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
                    fig = px.histogram(reference_data, x=feature_name, color=results['utility_columns']['target'], histnorm = '')

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
                        reference_data['Confusion'] = reference_data.apply(lambda x : 'TP' if (x[results['utility_columns']['target']] == label and x[results['utility_columns']['prediction']] == label) 
                                                 else ('FP' if(x[results['utility_columns']['target']] != label and x[results['utility_columns']['prediction']] == label) else \
                                                       ('FN' if (x[results['utility_columns']['target']] == label and x[results['utility_columns']['prediction']] != label) else 'TN')), axis = 1)
                        
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
                        "rowsPerPage" : min(len(results['num_feature_names']) + len(results['cat_feature_names']), 10),
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