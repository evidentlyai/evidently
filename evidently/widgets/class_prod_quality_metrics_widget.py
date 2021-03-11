#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import math

from scipy.stats import ks_2samp
from sklearn import metrics

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ClassProdQualityMetricsWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        return self.wi
        #raise ValueError("No reference data with target and prediction provided")

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping): 
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])] 

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])] 
        
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

        if production_data is not None:
            if target_column is not None and prediction_column is not None:
                production_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                production_data.dropna(axis=0, how='any', inplace=True)
            
                #calculate quality metrics
                accuracy_score = metrics.accuracy_score(production_data[target_column], production_data[prediction_column])
                avg_precision = metrics.precision_score(production_data[target_column], production_data[prediction_column],
                    average='macro')
                avg_recall = metrics.recall_score(production_data[target_column], production_data[prediction_column],
                    average='macro')
                avg_f1 = metrics.f1_score(production_data[target_column], production_data[prediction_column],
                    average='macro')

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
                            "value": str(round(accuracy_score, 3)),
                            "label": "Accuracy"
                          },
                          {
                            "value": str(round(avg_precision, 3)),
                            "label": "Precision"
                          },
                          {
                            "value": str(round(avg_recall, 3)),
                            "label": "Recall"
                          },
                          {
                            "value": str(round(avg_f1, 3)),
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

