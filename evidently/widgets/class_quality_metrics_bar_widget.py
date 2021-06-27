#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import math

#from scipy.stats import ks_2samp
#from sklearn import metrics

from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ClassQualityMetricsBarWidget(Widget):
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
            #plot quality metrics bar
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
                            "value": str(round(results['metrics'][self.dataset]['accuracy'], 3)),
                            "label": "Accuracy"
                          },
                          {
                            "value": str(round(results['metrics'][self.dataset]['precision'], 3)),
                            "label": "Precision"
                          },
                          {
                            "value": str(round(results['metrics'][self.dataset]['recall'], 3)),
                            "label": "Recall"
                          },
                          {
                            "value": str(round(results['metrics'][self.dataset]['f1'], 3)),
                            "label": "F1"
                          }
                        ]
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

