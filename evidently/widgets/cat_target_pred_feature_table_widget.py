#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare

import plotly.graph_objs as go
import plotly.express as px

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class CatTargetPredFeatureTable(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def analyzers(self):
        return [CatTargetDriftAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("neither target nor prediction data provided")

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[CatTargetDriftAnalyzer]

        if results['utility_columns']['prediction'] is not None and results['utility_columns']['target'] is not None:           
            additional_graphs_data = []
            params_data = []
            for feature_name in results['num_feature_names'] + results['cat_feature_names']: 
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
                current_data['dataset'] = 'Current'
                merged_data = pd.concat([reference_data, current_data])

                target_fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['target'], facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Current"]})

                target_fig_json  = json.loads(target_fig.to_json())

                #create prediction plot
                pred_fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['prediction'], facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Current"]})

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

        elif results['utility_columns']['target'] is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in results['num_feature_names'] + results['cat_feature_names']: 
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
                #TO DO%: out pf the cycle
                reference_data['dataset'] = 'Reference'
                current_data['dataset'] = 'Current'
                merged_data = pd.concat([reference_data, current_data])

                target_fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['target'], facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Current"]})

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
        elif results['utility_columns']['prediction'] is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in results['num_feature_names'] + results['cat_feature_names']: 
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
                current_data['dataset'] = 'Current'
                merged_data = pd.concat([reference_data, current_data])

                prediction_fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['prediction'], facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Current"]})

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

        

