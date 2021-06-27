#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

import numpy as np

from sklearn import metrics, preprocessing
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassPredDistrWidget(Widget):
    def __init__(self, title:str, dataset:str='reference'):
        super().__init__()
        self.title = title
        self.dataset = dataset #reference or current

    def analyzers(self):   
        return [ProbClassificationPerformanceAnalyzer]

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
        
        results = analyzers_results[ProbClassificationPerformanceAnalyzer]
        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
            if self.dataset == 'current':
                dataset_to_plot = current_data.copy(deep=False) if current_data is not None else None
            else:
                dataset_to_plot = reference_data.copy(deep=False)

            if dataset_to_plot is not None:
                dataset_to_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
                dataset_to_plot.dropna(axis=0, how='any', inplace=True)  
            
                #plot distributions
                graphs = []

                for label in results['utility_columns']['prediction']:

                    pred_distr = ff.create_distplot(
                        [
                            dataset_to_plot[dataset_to_plot[results['utility_columns']['target']] == label][label], 
                            dataset_to_plot[dataset_to_plot[results['utility_columns']['target']] != label][label]
                        ], 
                        [str(label), "other"],  
                        colors=[red, grey],
                        bin_size = 0.05,
                        show_curve = False,
                        show_rug=True
                    )

                    pred_distr.update_layout(
                        xaxis_title = "Probability",
                        yaxis_title = "Share",
                        legend = dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                        )
                    )

                    pred_distr_json = json.loads(pred_distr.to_json())

                    graphs.append({
                        "id": "tab_" + str(label),
                        "title": str(label),
                        "graph":{
                            "data":pred_distr_json["data"],
                            "layout":pred_distr_json["layout"],
                            }
                        })

                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="tabbed_graph",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1 if current_data is not None else 2,
                    params={
                        "graphs": graphs
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

