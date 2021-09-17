#!/usr/bin/env python
# coding: utf-8

import json

import pandas as pd
import plotly.graph_objs as go

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget, RED, GREY

class NumOutputCorrWidget(Widget):
    def __init__(self, title: str, kind: str = 'target'):
        super().__init__(title)
        self.title = title
        self.kind = kind #target or prediction

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

        if results['utility_columns'][self.kind] is not None:

            #calculate corr
            ref_output_corr = results['metrics'][self.kind + '_correlations']['reference']
            current_output_corr = results['metrics'][self.kind + '_correlations']['current']

            #plot output correlations
            output_corr = go.Figure()

            output_corr.add_trace(go.Bar(y = list(ref_output_corr.values()), x = list(ref_output_corr.keys()),
                marker_color = GREY, name = 'Reference'))

            output_corr.add_trace(go.Bar(y = list(current_output_corr.values()), x = list(ref_output_corr.keys()),
                marker_color = RED, name = 'Current'))

            output_corr.update_layout(xaxis_title = "Features", yaxis_title = "Correlation",
                yaxis = dict(
                    range=(-1, 1),
                    showticklabels=True
                ))

            output_corr_json  = json.loads(output_corr.to_json())

            self.wi = BaseWidgetInfo(
                title=self.title,
                type="big_graph",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=1,
                params={
                    "data": output_corr_json['data'],
                    "layout": output_corr_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None
