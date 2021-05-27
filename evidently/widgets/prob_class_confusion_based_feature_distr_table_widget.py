#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
from sklearn import preprocessing

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassConfusionBasedFeatureDistrTable(Widget):
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
            binaraizer = preprocessing.LabelBinarizer()
            binaraizer.fit(reference_data[target_column])
            binaraized_target = binaraizer.transform(reference_data[target_column])
            if production_data is not None:
                ref_array_prediction = reference_data[prediction_column].to_numpy()
                ref_prediction_ids = np.argmax(ref_array_prediction, axis=-1)
                ref_prediction_labels = [prediction_column[x] for x in ref_prediction_ids]
                reference_data['prediction_labels'] = ref_prediction_labels

                prod_array_prediction = production_data[prediction_column].to_numpy()
                prod_prediction_ids = np.argmax(prod_array_prediction, axis=-1)
                prod_prediction_labels = [prediction_column[x] for x in prod_prediction_ids]
                production_data['prediction_labels'] = prod_prediction_labels

                additional_graphs_data = []
                params_data = []

                for feature_name in num_feature_names + cat_feature_names: 
                    #add data for table in params
                    labels = prediction_column

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
                        fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                        #REF 
                        fig.add_trace(go.Scatter(
                            x = reference_data[reference_data[target_column] == label][feature_name],
                            y = reference_data[reference_data[target_column] == label][label],
                            mode = 'markers',
                            name = str(label) + ' (ref)',
                            marker=dict(
                                size=6,
                                color=red 
                                )
                            ),
                            row=1, col=1
                        )

                        fig.add_trace(go.Scatter(
                            x = reference_data[reference_data[target_column] != label][feature_name],
                            y = reference_data[reference_data[target_column] != label][label],
                            mode = 'markers',
                            name = 'other (ref)',
                            marker=dict(
                                size=6,
                                color=grey 
                                )
                            ),
                            row=1, col=1
                        )


                        fig.update_layout(
                            xaxis_title=feature_name,
                            yaxis_title='Probability',
                            xaxis = dict(
                                showticklabels=True
                            ),
                             yaxis = dict(
                                range=(0, 1),
                                showticklabels=True
                            )
                        )

                        #PROD Prediction
                        fig.add_trace(go.Scatter(
                            x = production_data[production_data[target_column] == label][feature_name],
                            y = production_data[production_data[target_column] == label][label],
                            mode = 'markers',
                            name = str(label) + ' (curr)',
                            marker=dict(
                                size=6,
                                color=red #set color equal to a variable
                                )
                            ),
                            row=1, col=2
                        )

                        fig.add_trace(go.Scatter(
                            x = production_data[production_data[target_column] != label][feature_name],
                            y = production_data[production_data[target_column] != label][label],
                            mode = 'markers',
                            name = 'other (curr)',
                            marker=dict(
                                size=6,
                                color=grey #set color equal to a variable
                                )
                            ),
                            row=1, col=2
                        )

                        fig.update_layout(
                            xaxis_title=feature_name,
                            yaxis_title='Probability',
                            xaxis = dict(
                                showticklabels=True
                            ),
                             yaxis = dict(
                                range=(0, 1),
                                showticklabels=True
                            )
                        )

                        # Update xaxis properties
                        fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)
                        fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=2)

                        # Update yaxis properties
                        fig.update_yaxes(title_text="Probability", showgrid=True, row=1, col=1)
                        fig.update_yaxes(title_text="Probability", showgrid=True, row=1, col=2)

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
                ref_array_prediction = reference_data[prediction_column].to_numpy()
                ref_prediction_ids = np.argmax(ref_array_prediction, axis=-1)
                ref_prediction_labels = [prediction_column[x] for x in ref_prediction_ids]
                reference_data['prediction_labels'] = ref_prediction_labels

                additional_graphs_data = []
                params_data = []

                for feature_name in num_feature_names + cat_feature_names: 
                    #add data for table in params
                    labels = prediction_column

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

                        fig = go.Figure()

                        fig.add_trace(go.Scatter(
                            x = reference_data[reference_data[target_column] == label][feature_name],
                            y = reference_data[reference_data[target_column] == label][label],
                            mode = 'markers',
                            name = str(label),
                            marker=dict(
                                size=6,
                                color=red #set color equal to a variable
                            )
                        ))

                        fig.add_trace(go.Scatter(
                            x = reference_data[reference_data[target_column] != label][feature_name],
                            y = reference_data[reference_data[target_column] != label][label],
                            mode = 'markers',
                            name = 'other',
                            marker=dict(
                                size=6,
                                color=grey 
                            )
                        ))


                        fig.update_layout(
                            xaxis_title=feature_name,
                            yaxis_title='Probability',
                            xaxis = dict(
                                showticklabels=True
                            ),
                             yaxis = dict(
                                range=(0, 1),
                                showticklabels=True
                            )
                        )

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