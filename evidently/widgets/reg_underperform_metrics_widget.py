#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class RegUnderperformMetricsWidget(Widget):
    def __init__(self, title:str, dataset:str='reference'):
        super().__init__()
        self.title = title
        self.dataset = dataset #reference or current

    def analyzers(self):   
        return [RegressionPerformanceAnalyzer]

    def get_info(self) -> BaseWidgetInfo:
        if self.dataset == 'reference':
            if self.wi:
                return self.wi
            raise ValueError("no data for underperformance quality metrics widget provided")
        else:
            return self.wi

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
            if self.dataset in results['metrics'].keys():
                self.wi = BaseWidgetInfo(
                    title=self.title,
                    type="counter",
                    details="",
                    alertStats=AlertStats(),
                    alerts=[],
                    alertsPosition="row",
                    insights=[],
                    size=2,
                    params={   
                        "counters": [
                          {
                            "value": str(round(results['metrics'][self.dataset]['underperformance']['majority']['mean_error'], 2)) + \
                            " (" + str(round(results['metrics'][self.dataset]['underperformance']['majority']['std_error'],2)) + ")",
                            "label": "Majority(90%)"
                          },
                          {
                            "value": str(round(results['metrics'][self.dataset]['underperformance']['underestimation']['mean_error'], 2)) + \
                            " (" + str(round(results['metrics'][self.dataset]['underperformance']['underestimation']['std_error'], 2)) +  ")",
                            "label": "Underestimation(5%)"
                          },
                          {
                            "value": str(round(results['metrics'][self.dataset]['underperformance']['overestimation']['mean_error'], 2)) + \
                            " (" + str(round(results['metrics'][self.dataset]['underperformance']['overestimation']['std_error'], 2)) + ")",
                            "label": "Overestimation(5%)"
                          }
                        ]
                    },
                    additionalGraphs=[]
                )
            else:
                self.wi = None
        else:
            self.wi = None
