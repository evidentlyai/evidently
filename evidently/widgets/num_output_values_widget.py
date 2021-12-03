#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import numpy as np

import plotly.graph_objs as go

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo
from evidently.widgets.widget import Widget, GREY, RED


class NumOutputValuesWidget(Widget):
    def __init__(self, title: str, kind: str = 'target'):
        super().__init__(title)
        self.title = title
        self.kind = kind  # target or prediction

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[NumTargetDriftAnalyzer]

        if results['utility_columns'][self.kind] is None:
            return None
        # plot values
        reference_mean = np.mean(reference_data[results['utility_columns'][self.kind]])
        reference_std = np.std(reference_data[results['utility_columns'][self.kind]], ddof=1)
        x_title = "Timestamp" if results['utility_columns']['date'] else "Index"

        output_values = go.Figure()

        output_values.add_trace(go.Scatter(
            x=reference_data[results['utility_columns']['date']] if results['utility_columns'][
                'date'] else reference_data.index,
            y=reference_data[results['utility_columns'][self.kind]],
            mode='markers',
            name='Reference',
            marker=dict(
                size=6,
                color=GREY
            )
        ))

        output_values.add_trace(go.Scatter(
            x=current_data[results['utility_columns']['date']] if results['utility_columns'][
                'date'] else current_data.index,
            y=current_data[results['utility_columns'][self.kind]],
            mode='markers',
            name='Current',
            marker=dict(
                size=6,
                color=RED
            )
        ))

        output_values.update_layout(
            xaxis_title=x_title,
            yaxis_title=self.kind.title() + ' Value',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            shapes=[
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    x0=0,
                    y0=reference_mean - reference_std,
                    x1=1,
                    y1=reference_mean + reference_std,
                    fillcolor="LightGreen",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ),
                dict(
                    type="line",
                    name='Reference',
                    xref="paper",
                    yref="y",
                    x0=0,  # min(testset_agg_by_date.index),
                    y0=reference_mean,
                    x1=1,  # max(testset_agg_by_date.index),
                    y1=reference_mean,
                    line=dict(
                        color="Green",
                        width=3
                    )
                ),
            ]
        )

        output_values_json = json.loads(output_values.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": output_values_json['data'],
                "layout": output_values_json['layout']
            },
        )
