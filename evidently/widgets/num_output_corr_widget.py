#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class NumOutputCorrWidget(Widget):
    def __init__(self, title:str, kind:str = 'target'):
        super().__init__()
        self.title = title
        self.kind = kind #target or prediction

    def analyzers(self):
        return [NumTargetDriftAnalyzer]

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
        
        results = analyzers_results[NumTargetDriftAnalyzer]

        if results['utility_columns'][self.kind] is not None:

            #calculate corr
            ref_output_corr = results['metrics'][self.kind + '_correlations']['reference']
            current_output_corr = results['metrics'][self.kind + '_correlations']['current']
            
            #plot output correlations
            output_corr = go.Figure()

            output_corr.add_trace(go.Bar(y = list(ref_output_corr.values()), x = list(ref_output_corr.keys()), 
                marker_color = grey, name = 'Reference'))

            output_corr.add_trace(go.Bar(y = list(current_output_corr.values()), x = list(ref_output_corr.keys()), 
                marker_color = red, name = 'Current'))

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

