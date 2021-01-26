#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class UnderperformSegmMetricsWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no widget info provided")

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

        
        reference_data['err'] = list(map(lambda x : x[0] - x[1], 
            zip(reference_data[prediction_column], reference_data[target_column])))

        quntile_5 = np.quantile(reference_data['err'], .05)
        quntile_95 = np.quantile(reference_data['err'], .95)

        reference_data['Error bias'] = reference_data.err.apply(lambda x : 'Underestimation' if x <= quntile_5 else 'Expected error' 
                                          if x < quntile_95 else 'Overestimation')

        mae = np.mean(reference_data['err'])
        mae_under = np.mean(reference_data[reference_data.err <= quntile_5]['err'])
        mae_exp = np.mean(reference_data[(reference_data.err > quntile_5) & (reference_data.err < quntile_95)]['err'])
        mae_over = np.mean(reference_data[reference_data.err >= quntile_95]['err'])

        sd = np.std(reference_data['err'], ddof = 1)
        sd_under = np.std(reference_data[reference_data.err <= quntile_5]['err'], ddof = 1)
        sd_exp = np.std(reference_data[(reference_data.err > quntile_5) & (reference_data.err < quntile_95)]['err'], ddof = 1)
        sd_over = np.std(reference_data[reference_data.err >= quntile_95]['err'], ddof = 1)
        
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
                    "value": str(round(mae, 2)) + " (+/-" + str(round(sd,2)) + ")",
                    "label": "Overall"
                  },
                  {
                    "value": str(round(mae_exp, 2)) + " (+/-" + str(round(sd_exp,2)) + ")",
                    "label": "Expected \n error"
                  },
                  {
                    "value": str(round(mae_under, 2)) + " (+/-" + str(round(sd_under, 2)) + ")",
                    "label": "Underestimation"
                  },
                  {
                    "value": str(round(mae_over, 2)) + " (+/-" + str(round(sd_over, 2)) + ")",
                    "label": "Overestimation"
                  }
                ]
            },
            additionalGraphs=[]
        )
