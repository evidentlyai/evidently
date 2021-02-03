#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class UnderperformSegmTableWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no widget info provided")

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

        
        if production_data is not None:
            production_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            production_data.dropna(axis=0, how='any', inplace=True)

            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            ref_error = reference_data[prediction_column] - reference_data[target_column]
            prod_error = production_data[prediction_column] - production_data[target_column]

            ref_quntile_5 = np.quantile(ref_error, .05)
            ref_quntile_95 = np.quantile(ref_error, .95)

            prod_quntile_5 = np.quantile(prod_error, .05)
            prod_quntile_95 = np.quantile(prod_error, .95)

            #create subplots
            reference_data['dataset'] = 'Reference'
            reference_data['Error bias'] = list(map(lambda x : 'Underestimation' if x <= ref_quntile_5 else 'Majority' 
                                          if x < ref_quntile_95 else 'Overestimation', ref_error))

            production_data['dataset'] = 'Production'
            production_data['Error bias'] = list(map(lambda x : 'Underestimation' if x <= prod_quntile_5 else 'Majority' 
                                          if x < prod_quntile_95 else 'Overestimation', prod_error))
            merged_data = pd.concat([reference_data, production_data])

            reference_data.drop(['dataset', 'Error bias'], axis=1, inplace=True)
            production_data.drop(['dataset', 'Error bias'], axis=1, inplace=True)

            params_data = []
            additional_graphs_data = []

            for feature_name in num_feature_names:
                feature_type = 'num'

                ref_overal_value = np.mean(reference_data[feature_name])
                ref_under_value = np.mean(reference_data[ref_error <= ref_quntile_5][feature_name])
                ref_expected_value = np.mean(reference_data[(ref_error > ref_quntile_5) & (ref_error < ref_quntile_95)][feature_name])
                ref_over_value = np.mean(reference_data[ref_error >= ref_quntile_95][feature_name])
                ref_range_value = 0 if ref_over_value == ref_under_value else 100*abs(ref_over_value - ref_under_value)/(np.max(reference_data[feature_name]) - np.min(reference_data[feature_name]))

                prod_overal_value = np.mean(production_data[feature_name])
                prod_under_value = np.mean(production_data[prod_error <= prod_quntile_5][feature_name])
                prod_expected_value = np.mean(production_data[(prod_error > prod_quntile_5) & (prod_error < prod_quntile_95)][feature_name])
                prod_over_value = np.mean(production_data[prod_error >= prod_quntile_95][feature_name])
                prod_range_value = 0 if prod_over_value == prod_under_value else 100*abs(prod_over_value - prod_under_value)/(np.max(production_data[feature_name]) - np.min(production_data[feature_name]))


                feature_hist = px.histogram(merged_data, x=feature_name, color='Error bias', facet_col="dataset",
                    histnorm = 'percent', barmode='overlay', category_orders={"dataset": ["Reference", "Production"], "Error bias": ["Underestimation", "Overestimation", "Majority"]})

                feature_hist_json  = json.loads(feature_hist.to_json())

                params_data.append(
                {
                    "details": 
                        {
                            "parts": [
                                {
                                    "title": "Error bias",
                                    "id": feature_name + "_hist"
                                }
                            ],
                            "insights": []
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": round(ref_expected_value, 2),
                        "f4": round(ref_under_value, 2),
                        "f5": round(ref_over_value, 2),
                        "f6": round(ref_range_value, 2),
                        "f7": round(prod_expected_value, 2),
                        "f8": round(prod_under_value, 2),
                        "f9": round(prod_over_value, 2),
                        "f10": round(prod_range_value, 2)
                }
                )

                additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_hist',
                    {
                        "data" : feature_hist_json['data'],
                        "layout" : feature_hist_json['layout']
                    }
                    )
                )

            for feature_name in cat_feature_names:
                feature_type = 'cat'

                ref_overal_value = reference_data[feature_name].value_counts().idxmax()
                ref_under_value = reference_data[ref_error <= ref_quntile_5][feature_name].value_counts().idxmax()
                #ref_expected_value = reference_data[(ref_error > ref_quntile_5) & (ref_error < ref_quntile_95)][feature_name].value_counts().idxmax()
                ref_over_value = reference_data[ref_error >= ref_quntile_95][feature_name].value_counts().idxmax()
                ref_range_value = 1 if (ref_overal_value != ref_under_value) or (ref_over_value != ref_overal_value) \
                   or (ref_under_value != ref_overal_value) else 0

                prod_overal_value = production_data[feature_name].value_counts().idxmax()
                prod_under_value = production_data[prod_error <= prod_quntile_5][feature_name].value_counts().idxmax()
                #prod_expected_value = production_data[(prod_error > prod_quntile_5) & (prod_error < prod_quntile_95)][feature_name].value_counts().idxmax()
                prod_over_value = production_data[prod_error >= prod_quntile_95][feature_name].value_counts().idxmax()
                prod_range_value = 1 if (prod_overal_value != prod_under_value) or (prod_over_value != prod_overal_value) \
                   or (prod_under_value != prod_overal_value) else 0

                feature_hist = px.histogram(merged_data, x=feature_name, color='Error bias', facet_col="dataset",
                    histnorm = 'percent', barmode='overlay', category_orders={"dataset": ["Reference", "Production"], "Error bias": ["Underestimation", "Overestimation", "Majority"]})

                feature_hist_json  = json.loads(feature_hist.to_json())

                params_data.append(
                {
                    "details": 
                        {
                            "parts": [
                                {
                                    "title": "Error bias",
                                    "id": feature_name + "_hist"
                                }
                            ],
                            "insights": []
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": str(ref_overal_value),
                        "f4": str(ref_under_value),
                        "f5": str(ref_over_value),
                        "f6": str(ref_range_value),
                        "f7": str(prod_overal_value),
                        "f8": str(prod_under_value),
                        "f9": str(prod_over_value),
                        "f10": int(prod_range_value)
                }
                )

                additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_hist',
                    {
                        "data" : feature_hist_json['data'],
                        "layout" : feature_hist_json['layout']
                    }
                    )
                )

            self.wi = BaseWidgetInfo(
                title = self.title,
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
                        },
                        {
                            "title": "Type",
                            "field": "f2"
                        },
                        {
                            "title": "REF: Majority",
                            "field": "f3"
                        },
                        {
                            "title": "REF: Under",
                            "field": "f4"
                        },
                        {
                            "title": "REF: Over",
                            "field": "f5"
                        },
                        {
                            "title": "REF: Range(%)",
                            "field": "f6"
                        },
                        {
                            "title": "PROD: Majority",
                            "field": "f7"
                        },
                        {
                            "title": "PROD: Under",
                            "field": "f8"
                        },
                        {
                            "title": "PROD: Over",
                            "field": "f9"
                        },
                        {
                            "title": "PROD: Range(%)",
                            "field": "f10",
                            "sort" : "desc"
                        }

                    ],
                    "data": params_data
                },

                additionalGraphs = additional_graphs_data
            )

        else:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            error = reference_data[prediction_column] - reference_data[target_column]

            quntile_5 = np.quantile(error, .05)
            quntile_95 = np.quantile(error, .95)

            reference_data['Error bias'] = reference_data['Error bias'] = list(map(lambda x : 'Underestimation' if x <= quntile_5 else 'Majority' 
                                          if x < quntile_95 else 'Overestimation', error))

            params_data = []
            additional_graphs_data = []

            for feature_name in num_feature_names:# + cat_feature_names: #feature_names:

                feature_type = 'num'
                ref_overal_value = np.mean(reference_data[feature_name])
                ref_under_value = np.mean(reference_data[error <= quntile_5][feature_name])
                #ref_expected_value = np.mean(reference_data[(error > quntile_5) & (error < quntile_95)][feature_name])
                ref_over_value = np.mean(reference_data[error >= quntile_95][feature_name])
                ref_range_value = 100*abs(ref_over_value - ref_under_value)/(np.max(reference_data[feature_name]) - np.min(reference_data[feature_name]))

                hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm = 'percent', barmode='overlay', 
                    category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]})

                #hist_fig = px.histogram(reference_data, x=feature_name, color=target_column, facet_col="dataset",
                #        category_orders={"dataset": ["Reference", "Production"]})

                hist_figure = json.loads(hist.to_json())

                params_data.append(
                    {
                        "details": 
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name,
                            "f2": feature_type,
                            "f3": round(ref_overal_value, 2),
                            "f4": round(ref_under_value, 2),
                            "f5": round(ref_over_value, 2),
                            "f6": round(ref_range_value, 2)
                    }
                )

                additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_hist',
                    {
                        "data" : hist_figure['data'],
                        "layout" : hist_figure['layout']
                    }
                    )
                )

            for feature_name in cat_feature_names: #feature_names:

                feature_type = 'cat'
                ref_overal_value = reference_data[feature_name].value_counts().idxmax()
                ref_under_value = reference_data[error <= quntile_5][feature_name].value_counts().idxmax()
                #ref_expected_value = reference_data[(error > quntile_5) & (error < quntile_95)][feature_name].value_counts().idxmax()
                ref_over_value = reference_data[error >= quntile_95][feature_name].value_counts().idxmax()
                ref_range_value = 1 if (ref_overal_value != ref_under_value) or (ref_over_value != ref_overal_value) \
                   or (ref_under_value != ref_overal_value) else 0

                hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm = 'percent', 
                    barmode='overlay', category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]})

                #hist_fig = px.histogram(reference_data, x=feature_name, color=target_column, facet_col="dataset",
                #        category_orders={"dataset": ["Reference", "Production"]})

                hist_figure = json.loads(hist.to_json())

                params_data.append(
                    {
                        "details": 
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    }
                                ],
                                "insights": []
                            },
                            "f1": feature_name,
                            "f2": feature_type,
                            "f3": str(ref_overal_value), 
                            "f4": str(ref_under_value), 
                            "f5": str(ref_over_value),
                            "f6": int(ref_range_value)
                    }
                )

                additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_hist',
                    {
                        "data" : hist_figure['data'],
                        "layout" : hist_figure['layout']
                    }
                    )
                )

            reference_data.drop('Error bias', axis=1, inplace=True)

            self.wi = BaseWidgetInfo(
                title = self.title,
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
                        },
                        {
                            "title": "Type",
                            "field": "f2"
                        },
                        {
                            "title": "Majority",
                            "field": "f3"
                        },
                        {
                            "title": "Underestimation",
                            "field": "f4"
                        },
                        {
                            "title": "Overestimation",
                            "field": "f5"
                        },
                        {
                            "title": "Range(%)",
                            "field": "f6",
                            "sort" : "desc"
                        }
                    ],
                    "data": params_data
                },

                additionalGraphs = additional_graphs_data
            )
