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

        
        reference_data['err'] = list(map(lambda x : x[0] - x[1], 
            zip(reference_data[prediction_column], reference_data[target_column])))

        quntile_5 = np.quantile(reference_data['err'], .05)
        quntile_95 = np.quantile(reference_data['err'], .95)

        reference_data['Error bias'] = reference_data.err.apply(lambda x : 'Underestimation' if x <= quntile_5 else 'Expected error' 
                                          if x < quntile_95 else 'Overestimation')

        params_data = []
        additional_graphs_data = []

        for feature_name in num_feature_names:# + cat_feature_names: #feature_names:

            feature_type = 'num'
            ref_overal_value = np.mean(reference_data[feature_name])
            ref_under_value = np.mean(reference_data[reference_data.err <= quntile_5][feature_name])
            ref_expected_value = np.mean(reference_data[(reference_data.err > quntile_5) & (reference_data.err < quntile_95)][feature_name])
            ref_over_value = np.mean(reference_data[reference_data.err >= quntile_95][feature_name])

            hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm = 'percent')

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
                        "f5": round(ref_expected_value, 2),
                        "f6": round(ref_over_value, 2)
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
            ref_under_value = reference_data[reference_data.err <= quntile_5][feature_name].value_counts().idxmax()
            ref_expected_value = reference_data[(reference_data.err > quntile_5) & (reference_data.err < quntile_95)][feature_name].value_counts().idxmax()
            ref_over_value = reference_data[reference_data.err >= quntile_95][feature_name].value_counts().idxmax()

            hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm = 'percent')

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
                        "f3": int(ref_overal_value), 
                        "f4": int(ref_under_value), 
                        "f5": int(ref_expected_value),
                        "f6": int(ref_over_value), 
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
                        "title": "Overal",
                        "field": "f3"
                    },
                    {
                        "title": "Underestimation",
                        "field": "f4"
                    },
                    {
                        "title": "Expected error",
                        "field": "f5"
                    },
                    {
                        "title": "Overestimation",
                        "field": "f6"
                    }
                ],
                "data": params_data
            },

            additionalGraphs = additional_graphs_data
        )
