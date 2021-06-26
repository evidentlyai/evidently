#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import chisquare
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class CatOutputDriftWidget(Widget):
    def __init__(self, title:str, kind:str = 'target'):
        super().__init__()
        self.title = title
        self.kind = kind

    def analyzers(self):
        return [CatTargetDriftAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        #    return self.wi
        #raise ValueError("no widget info provided")
        return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[CatTargetDriftAnalyzer]

        if results['utility_columns'][self.kind] is not None:
            output_name = results['metrics'][self.kind + '_name'] 
            output_type = results['metrics'][self.kind + '_type'] 
            output_p_value = results['metrics'][self.kind + '_drift'] 
            output_sim_test = "detected" if output_p_value < 0.05 else "not detected"
            #plot output distributions
            fig = go.Figure()

            fig.add_trace(go.Histogram(x=reference_data[output_name], 
                 marker_color=grey, opacity=0.6, nbinsx=10,  name='Reference', histnorm='probability'))

            fig.add_trace(go.Histogram(x=current_data[output_name],
                 marker_color=red, opacity=0.6,nbinsx=10, name='Current', histnorm='probability'))

            fig.update_layout(
                legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                ),
                xaxis_title = output_name.title(),
                yaxis_title = "Share"
            )

            output_drift_json  = json.loads(fig.to_json())

            self.wi = BaseWidgetInfo(
                title= self.kind.title() + " drift: ".title() + output_sim_test + ", p_value=" + str(round(output_p_value, 6)),
                type="big_graph",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=2,
                params={
                    "data": output_drift_json['data'],
                    "layout": output_drift_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None
