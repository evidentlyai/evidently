#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import math

from scipy.stats import ks_2samp
from statsmodels.graphics.gofplots import qqplot
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class TargetNameWidget(Widget):
    def __init__(self, title:str, kind:str):
        super().__init__()
        self.title = title
        self.kind = kind #regression, classification or prob_classification

    def analyzers(self):   
        if self.kind == 'regression':
            return[RegressionPerformanceAnalyzer]
        elif self.kind == 'classification':
            return[ClassificationPerformanceAnalyzer]
        elif self.kind == 'prob_classification':
            return[ProbClassificationPerformanceAnalyzer]  
        else: return []  

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no widget info provided")

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results):
        
        if self.kind == 'regression':
            results = analyzers_results[RegressionPerformanceAnalyzer]
        elif self.kind == 'classification':
            results = analyzers_results[ClassificationPerformanceAnalyzer]
        elif self.kind == 'prob_classification':
            results = analyzers_results[ProbClassificationPerformanceAnalyzer]
        else:
            results = None

        if results: 
            if results['utility_columns']['target'] is not None and results['utility_columns']['prediction'] is not None:
                self.wi = BaseWidgetInfo(
                    title="",
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
                            "value": "",
                            "label": self.title + " Target: '" + results['utility_columns']['target'] + "'"
                          }
                        ]
                    },
                    additionalGraphs=[],
                )
            else:
                self.wi = None
        else:
            self.wi = None

