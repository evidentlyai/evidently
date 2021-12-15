#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer

from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.widgets.widget import Widget, RED, GREY


class ProbClassConfusionBasedFeatureDistrTable(Widget):
    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):

        results = analyzers_results[ProbClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            raise ValueError(f"Widget [{self.title}] requires 'target' or 'prediction' columns")

        if current_data is not None:
            ref_array_prediction = reference_data[results['utility_columns']['prediction']].to_numpy()
            ref_prediction_ids = np.argmax(ref_array_prediction, axis=-1)
            ref_prediction_labels = [results['utility_columns']['prediction'][x] for x in ref_prediction_ids]
            reference_data['prediction_labels'] = ref_prediction_labels

            current_array_prediction = current_data[results['utility_columns']['prediction']].to_numpy()
            current_prediction_ids = np.argmax(current_array_prediction, axis=-1)
            current_prediction_labels = [results['utility_columns']['prediction'][x] for x in
                                         current_prediction_ids]
            current_data['prediction_labels'] = current_prediction_labels

            additional_graphs_data = []
            params_data = []

            for feature_name in results["num_feature_names"] + results["cat_feature_names"]:
                # add data for table in params
                labels = results['utility_columns']['prediction']

                params_data.append(
                    {
                        "details": {
                            "parts": [{"title": "All", "id": "All" + "_" + str(feature_name)}] + [
                                {"title": str(label), "id": feature_name + "_" + str(label)} for label in labels],
                            "insights": []
                        },
                        "f1": feature_name
                    }
                )

                # create confusion based plots
                reference_data['dataset'] = 'Reference'
                current_data['dataset'] = 'Current'
                merged_data = pd.concat([reference_data, current_data])

                fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['target'],
                                   facet_col="dataset", histnorm='',
                                   category_orders={"dataset": ["Reference", "Current"]})

                fig_json = json.loads(fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        "All" + "_" + str(feature_name),
                        {
                            "data": fig_json['data'],
                            "layout": fig_json['layout']
                        },
                    )
                )

                for label in labels:
                    fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                    # REF
                    fig.add_trace(go.Scatter(
                        x=reference_data[reference_data[results['utility_columns']['target']] == label][
                            feature_name],
                        y=reference_data[reference_data[results['utility_columns']['target']] == label][label],
                        mode='markers',
                        name=str(label) + ' (ref)',
                        marker=dict(
                            size=6,
                            color=RED
                        )
                    ),
                        row=1, col=1
                    )

                    fig.add_trace(go.Scatter(
                        x=reference_data[reference_data[results['utility_columns']['target']] != label][
                            feature_name],
                        y=reference_data[reference_data[results['utility_columns']['target']] != label][label],
                        mode='markers',
                        name='other (ref)',
                        marker=dict(
                            size=6,
                            color=GREY
                        )
                    ),
                        row=1, col=1
                    )

                    fig.update_layout(
                        xaxis_title=feature_name,
                        yaxis_title='Probability',
                        xaxis=dict(
                            showticklabels=True
                        ),
                        yaxis=dict(
                            range=(-0.1, 1.1),
                            showticklabels=True
                        )
                    )

                    # current Prediction
                    fig.add_trace(go.Scatter(
                        x=current_data[current_data[results['utility_columns']['target']] == label][feature_name],
                        y=current_data[current_data[results['utility_columns']['target']] == label][label],
                        mode='markers',
                        name=str(label) + ' (curr)',
                        marker=dict(
                            size=6,
                            color=RED  # set color equal to a variable
                        )
                    ),
                        row=1, col=2
                    )

                    fig.add_trace(go.Scatter(
                        x=current_data[current_data[results['utility_columns']['target']] != label][feature_name],
                        y=current_data[current_data[results['utility_columns']['target']] != label][label],
                        mode='markers',
                        name='other (curr)',
                        marker=dict(
                            size=6,
                            color=GREY  # set color equal to a variable
                        )
                    ),
                        row=1, col=2
                    )

                    fig.update_layout(
                        xaxis_title=feature_name,
                        yaxis_title='Probability',
                        xaxis=dict(
                            showticklabels=True
                        ),
                        yaxis=dict(
                            range=(-0.1, 1.1),
                            showticklabels=True
                        )
                    )

                    # Update xaxis properties
                    fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)
                    fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=2)

                    # Update yaxis properties
                    fig.update_yaxes(title_text="Probability", showgrid=True, row=1, col=1)
                    fig.update_yaxes(title_text="Probability", showgrid=True, row=1, col=2)

                    fig_json = json.loads(fig.to_json())

                    # write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            feature_name + "_" + str(label),
                            {
                                "data": fig_json['data'],
                                "layout": fig_json['layout']
                            },
                        )
                    )
        else:
            ref_array_prediction = reference_data[results['utility_columns']['prediction']].to_numpy()
            ref_prediction_ids = np.argmax(ref_array_prediction, axis=-1)
            ref_prediction_labels = [results['utility_columns']['prediction'][x] for x in ref_prediction_ids]
            reference_data['prediction_labels'] = ref_prediction_labels

            additional_graphs_data = []
            params_data = []

            for feature_name in results["num_feature_names"] + results["cat_feature_names"]:
                # add data for table in params
                labels = results['utility_columns']['prediction']

                params_data.append(
                    {
                        "details": {
                            "parts": [{"title": "All", "id": "All" + "_" + str(feature_name)}] + [
                                {"title": str(label), "id": feature_name + "_" + str(label)} for label in labels],
                            "insights": []
                        },
                        "f1": feature_name
                    }
                )

                # create confusion based plots
                fig = px.histogram(reference_data, x=feature_name, color=results['utility_columns']['target'],
                                   histnorm='')

                fig_json = json.loads(fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        "All" + "_" + str(feature_name),
                        {
                            "data": fig_json['data'],
                            "layout": fig_json['layout']
                        },
                    )
                )

                for label in labels:
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=reference_data[reference_data[results['utility_columns']['target']] == label][
                            feature_name],
                        y=reference_data[reference_data[results['utility_columns']['target']] == label][label],
                        mode='markers',
                        name=str(label),
                        marker=dict(
                            size=6,
                            color=RED  # set color equal to a variable
                        )
                    ))

                    fig.add_trace(go.Scatter(
                        x=reference_data[reference_data[results['utility_columns']['target']] != label][
                            feature_name],
                        y=reference_data[reference_data[results['utility_columns']['target']] != label][label],
                        mode='markers',
                        name='other',
                        marker=dict(
                            size=6,
                            color=GREY
                        )
                    ))

                    fig.update_layout(
                        xaxis_title=feature_name,
                        yaxis_title='Probability',
                        xaxis=dict(
                            showticklabels=True
                        ),
                        yaxis=dict(
                            range=(-0.1, 1.1),
                            showticklabels=True
                        )
                    )

                    fig_json = json.loads(fig.to_json())

                    # write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            feature_name + "_" + str(label),
                            {
                                "data": fig_json['data'],
                                "layout": fig_json['layout']
                            },
                        )
                    )

        return BaseWidgetInfo(
            title=self.title,
            type="big_table",
            size=2,
            params={
                "rowsPerPage": min(len(results["num_feature_names"]) + len(results["cat_feature_names"]), 10),
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
