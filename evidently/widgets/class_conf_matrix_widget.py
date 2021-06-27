#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

import numpy as np

from sklearn import metrics
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ClassConfMatrixWidget(Widget):
    def __init__(self, title:str, dataset:str='reference'):
        super().__init__()
        self.title = title
        self.dataset = dataset #reference or current

    def analyzers(self):   
        return [ClassificationPerformanceAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.dataset == 'reference':
            if self.wi:
                return self.wi
            raise ValueError("no data for quality metrics widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[ClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
            if self.dataset in results['metrics'].keys():          
                #plot confusion matrix
                conf_matrix = results['metrics'][self.dataset]['confusion_matrix']['values']

                labels = results['metrics'][self.dataset]['confusion_matrix']['labels']

                z = [[int(y) for y in x] for x in conf_matrix]

                # change each element of z to type string for annotations
                z_text = [[str(y) for y in x] for x in z]

                fig = ff.create_annotated_heatmap(z, x=labels, y=labels, annotation_text=z_text, 
                    colorscale='bluered',showscale=True)

                fig.update_layout(
                    xaxis_title="Predicted value", 
                    yaxis_title="Actual value")

                conf_matrix_json = json.loads(fig.to_json())

                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="big_graph",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1 if current_data is not None else 2,
                    params={
                        "data": conf_matrix_json['data'],
                        "layout": conf_matrix_json['layout']
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

