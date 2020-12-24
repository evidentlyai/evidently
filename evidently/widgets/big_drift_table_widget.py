#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
#import matplotlib.pyplot as plt
import plotly.graph_objs as go

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class BigDriftTableWidget(Widget):
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

        #set params data
        params_data = []
        drifted_fetures_count = 0
        #plt.ioff()
        for feature_name in num_feature_names:# + cat_feature_names: #feature_names:
            prod_small_hist = np.histogram(production_data[feature_name][np.isfinite(production_data[feature_name])], bins = 10, density = True)
            ref_small_hist = np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])], bins = 10, density = True)

            feature_type = 'num'

            p_value = ks_2samp(reference_data[feature_name], production_data[feature_name])[1]

            distr_sim_test = "Detected" if p_value < 0.05 else "Not Detected"
            drifted_fetures_count += 1 if p_value < 0.05 else 0

            params_data.append(
                {
                    "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": feature_name + "_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": feature_name + "_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": feature_name,
                        "f6": feature_type,
                        "f3": {
                            "x": list(ref_small_hist[1]),
                            "y": list(ref_small_hist[0])
                        },
                        "f4": {
                            "x": list(prod_small_hist[1]),
                            "y": list(prod_small_hist[0])
                        },
                        "f2": distr_sim_test,
                        "f5": round(p_value, 6) 
                }
                )

        for feature_name in cat_feature_names: #feature_names:
            prod_small_hist = np.histogram(production_data[feature_name][np.isfinite(production_data[feature_name])], bins = 10, density = True)
            ref_small_hist = np.histogram(reference_data[feature_name][np.isfinite(reference_data[feature_name])], bins = 10, density = True)

            feature_type = 'cat'

            #p_value = ks_2samp(reference_data[feature_name], production_data[feature_name])[1]
            #CHI2 to be implemented for cases with different categories
            ref_feature_vc = reference_data[feature_name][np.isfinite(reference_data[feature_name])].value_counts()
            prod_feature_vc = production_data[feature_name][np.isfinite(production_data[feature_name])].value_counts()

            keys = set(list(reference_data[feature_name][np.isfinite(reference_data[feature_name])].unique()) + 
                list(production_data[feature_name][np.isfinite(production_data[feature_name])].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            prod_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(prod_feature_vc.index, prod_feature_vc.values):
                prod_feature_dict[key] = item

            f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
            f_obs = [value[1] for value in sorted(prod_feature_dict.items())]

            p_value = chisquare(f_exp, f_obs)[1]

            distr_sim_test = "Detected" if p_value < 0.05 else "Not Detected"
            drifted_fetures_count += 1 if p_value < 0.05 else 0

            params_data.append(
                {
                    "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": feature_name + "_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": feature_name + "_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": feature_name,
                        "f6": feature_type,
                        "f3": {
                            "x": list(ref_small_hist[1]),
                            "y": list(ref_small_hist[0])
                        },
                        "f4": {
                            "x": list(prod_small_hist[1]),
                            "y": list(prod_small_hist[0])
                        },
                        "f2": distr_sim_test,
                        "f5": round(p_value, 6) 
                }
                )


        #set additionalGraphs
        additional_graphs_data = []
        for feature_name in num_feature_names + cat_feature_names: #feature_names:

            #plot distributions
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=reference_data[feature_name], 
                 marker_color=grey, opacity=0.6, nbinsx=10,  name='Reference', histnorm='probability'))

            fig.add_trace(go.Histogram(x=production_data[feature_name],
                 marker_color=red, opacity=0.6,nbinsx=10, name='Production', histnorm='probability'))

            fig.update_layout(
                legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                ),
                xaxis_title = feature_name,
                yaxis_title = "Share"
            )
    
            distr_figure = json.loads(fig.to_json())
        
            #plot drift
            reference_mean = np.mean(reference_data[feature_name][np.isfinite(reference_data[feature_name])])
            reference_std = np.std(reference_data[feature_name][np.isfinite(reference_data[feature_name])], ddof = 1) 
            x_title = "Timestamp" if date_column else "Index"

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x = production_data[date_column] if date_column else production_data.index,
                y = production_data[feature_name],
                mode = 'markers',
                name = 'Production',
                marker = dict(
                    size = 6,
                    color = grey
                )
            ))


            fig.update_layout(
                xaxis_title = x_title,
                yaxis_title = feature_name,
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

            drift_figure = json.loads(fig.to_json())

            #add distributions data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_distr',
                    {
                        "data" : distr_figure['data'],
                        "layout" : distr_figure['layout']
                    }
                )
            )

            #add drift data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + '_drift',
                    {
                        "data" : drift_figure['data'],
                        "layout" : drift_figure['layout']
                    }
                )
            )

        self.wi = BaseWidgetInfo(
            title="Data Drift: drift detected for " + str(drifted_fetures_count) +
                " out of " + str(len(num_feature_names) + len(cat_feature_names)) + " features",
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
                        "field": "f6"
                    },
                    {
                        "title": "Reference Distribution",
                        "field": "f3",
                        "type": "histogram",
                        "options": {
                            "xField": "x",
                            "yField": "y"
                        }
                    },
                    {
                        "title": "Production Distribution",
                        "field": "f4",
                        "type": "histogram",
                        "options": {
                            "xField": "x",
                            "yField": "y"
                        }
                    },
                    {
                        "title": "Data drift",
                        "field": "f2"
                    },
                    {
                        "title": "P-Value for Similarity Test",
                        "field": "f5",
                        "sort" : "asc"
                    }
                ],
                "data": params_data
            },

            additionalGraphs = additional_graphs_data
        )
