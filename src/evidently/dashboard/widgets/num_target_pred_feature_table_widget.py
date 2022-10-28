#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class NumTargetPredFeatureTable(Widget):
    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        color_options = self.options_provider.get(ColorOptions)
        results = NumTargetDriftAnalyzer.get_results(analyzers_results)

        if current_data is None:
            raise ValueError("current_data should be present")

        target_column = results.columns.utility_columns.target
        prediction_column = results.columns.utility_columns.prediction

        if target_column and prediction_column:
            return None

        additional_graphs_data = []
        params_data = []

        for feature_name in results.columns.get_all_features_list(cat_before_num=False):
            # add data for table in params
            params_data.append(
                {
                    "details": {
                        "parts": [
                            {"title": "Feature values", "id": feature_name + "_values"}
                        ],
                        "insights": [],
                    },
                    "f1": feature_name,
                }
            )

            # create plot
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

            if prediction_column is not None:
                fig.add_trace(
                    go.Scattergl(
                        x=reference_data[feature_name],
                        y=reference_data[prediction_column],
                        mode="markers",
                        name="Prediction (ref)",
                        marker=dict(size=6, color=color_options.secondary_color),
                    ),
                    row=1,
                    col=1,
                )

            if target_column is not None:
                fig.add_trace(
                    go.Scattergl(
                        x=reference_data[feature_name],
                        y=reference_data[target_column],
                        mode="markers",
                        name="Target (ref)",
                        marker=dict(size=6, color=color_options.primary_color),
                    ),
                    row=1,
                    col=1,
                )

            if prediction_column is not None:
                fig.add_trace(
                    go.Scatter(
                        x=current_data[feature_name],
                        y=current_data[prediction_column],
                        mode="markers",
                        name="Prediction (curr)",
                        marker=dict(size=6, color=color_options.secondary_color),
                    ),
                    row=1,
                    col=2,
                )

            if target_column is not None:
                fig.add_trace(
                    go.Scatter(
                        x=current_data[feature_name],
                        y=current_data[target_column],
                        mode="markers",
                        name="Target (curr)",
                        marker=dict(size=6, color=color_options.primary_color),
                    ),
                    row=1,
                    col=2,
                )

            # Update xaxis properties
            fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)
            fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=2)

            # Update yaxis properties
            fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=1)
            fig.update_yaxes(title_text="Value", showgrid=True, row=1, col=2)

            fig_json = json.loads(fig.to_json())

            # write plot data in table as additional data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    feature_name + "_values",
                    {"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )

        return BaseWidgetInfo(
            title=self.title,
            type="big_table",
            size=2,
            params={
                "rowsPerPage": min(results.columns.get_features_len(), 10),
                "columns": [{"title": "Feature", "field": "f1"}],
                "data": params_data,
            },
            additionalGraphs=additional_graphs_data,
        )
