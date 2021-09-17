#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget, RED, GREY


class NumTargetPredFeatureTable(Widget):
    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):

        results = analyzers_results[NumTargetDriftAnalyzer]

        if results['utility_columns']['prediction'] is not None or results['utility_columns']['target'] is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in results['num_feature_names'] + results['cat_feature_names']:
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
                fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                if results['utility_columns']['prediction'] is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = reference_data[feature_name],
                        y = reference_data[results['utility_columns']['prediction']],
                        mode = 'markers',
                        name = 'Prediction (ref)',
                        marker = dict(
                            size = 6,
                            color = GREY
                            )
                        ),
                        row=1, col=1
                    )

                if results['utility_columns']['target'] is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = reference_data[feature_name],
                        y = reference_data[results['utility_columns']['target']],
                        mode = 'markers',
                        name = 'Target (ref)',
                        marker = dict(
                            size = 6,
                            color = RED
                            )
                        ),
                        row=1, col=1
                    )

                if results['utility_columns']['prediction'] is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = current_data[feature_name],
                        y = current_data[results['utility_columns']['prediction']],
                        mode = 'markers',
                        name = 'Prediction (curr)',
                        marker = dict(
                            size = 6,
                            color = GREY
                            )
                        ),
                        row=1, col=2
                    )

                if results['utility_columns']['target'] is not None:
                    fig.add_trace(
                        go.Scatter(
                        x = current_data[feature_name],
                        y = current_data[results['utility_columns']['target']],
                        mode = 'markers',
                        name = 'Target (curr)',
                        marker = dict(
                            size = 6,
                            color = RED
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
