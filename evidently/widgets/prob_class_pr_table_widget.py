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

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo, TabInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassPRTableWidget(Widget):
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
            raise ValueError("no data for roc-curve widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[ProbClassificationPerformanceAnalyzer]
        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
            if self.dataset in results['metrics'].keys():
                if len(results['utility_columns']['prediction']) <= 2:
                    pr_table_data = results['metrics'][self.dataset]['pr_table']
                    params_data = []
                    for line in pr_table_data:
                        count = line[1]
                        prob = round(line[2],2)
                        top = round(line[0], 1)
                        tp = line[3]
                        fp = line[4]
                        precision = round(line[5], 1)
                        recall = round(line[6], 1)

                        params_data.append({ 'f1': float(top), 
                                       'f2' : int(count), 
                                       'f3' : float(prob),
                                       'f4' : int(tp), 
                                       'f5' : int(fp), 
                                       'f6' : float(precision), 
                                       'f7' : float(recall)})

                    self.wi = BaseWidgetInfo(
                    title = self.title,
                    type="big_table",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=1 if current_data is not None else 2,
                    params={
                        "rowsPerPage" : 21,
                        "columns": [
                            {
                                "title": "Top(%)",
                                "field": "f1",
                                "sort" : "asc"
                            },
                            {
                                "title": "Count",
                                "field": "f2"
                            },
                            {
                                "title": "Prob",
                                "field": "f3",
                            },
                            {
                                "title": "TP",
                                "field": "f4"
                            },
                            {
                                "title": "FP",
                                "field": "f5"
                            },
                            {
                                "title": "Precision",
                                "field": "f6"
                            },
                            {
                                "title": "Recall",
                                "field": "f7"
                            }
                        ],
                        "data": params_data
                    },
                    additionalGraphs = []
                )

                else:              
                    #create tables
                    tabs = []

                    for label in results['utility_columns']['prediction']:
                        params_data = []
                        pr_table_data = results['metrics'][self.dataset]['pr_table'][label]
                        
                        for line in pr_table_data:
                            count = line[1]
                            prob = round(line[2],2)
                            top = round(line[0], 1)
                            tp = line[3]
                            fp = line[4]
                            precision = round(line[5], 1)
                            recall = round(line[6], 1)

                            params_data.append({ 'f1': float(top), 
                                           'f2' : int(count), 
                                           'f3' : float(prob),
                                           'f4' : int(tp), 
                                           'f5' : int(fp), 
                                           'f6' : float(precision), 
                                           'f7' : float(recall)})

                        tabs.append(TabInfo(
                            id=label,
                            title=label,
                            widget=BaseWidgetInfo(
                                title="",
                                type="big_table",
                                details="",
                                alertStats=AlertStats(),
                                alerts=[],
                                alertsPosition="row",
                                insights=[],
                                size=2, #if current_data is not None else 2,
                                params={
                                    "rowsPerPage": 21,
                                    "columns": [
                                        {
                                            "title": "Top(%)",
                                            "field": "f1",
                                            "sort" : "asc"
                                        },
                                        {
                                            "title": "Count",
                                            "field": "f2"
                                        },
                                        {
                                            "title": "Prob",
                                            "field": "f3"
                                        },
                                        {
                                            "title": "TP",
                                            "field": "f4"
                                        },
                                        {
                                            "title": "FP",
                                            "field": "f5"
                                        },
                                        {
                                            "title": "Precision",
                                            "field": "f6"
                                        },
                                        {
                                            "title": "Recall",
                                            "field": "f7"
                                        }
                                    ],
                                    "data": params_data
                                },
                                additionalGraphs = []
                            )
                        ))

                    self.wi = BaseWidgetInfo(
                        type="tabs",
                        title=self.title,
                        size=1 if current_data is not None else 2,
                        details="",
                        tabs=tabs
                    )
            else:
                self.wi = None
        else:
            self.wi = None

