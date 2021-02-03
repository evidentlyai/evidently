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


class ProdUnderperformMetricsWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        return self.wi

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
            production_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            production_data.dropna(axis=0, how='any', inplace=True)
            
            prod_error = production_data[prediction_column] - production_data[target_column]

            prod_quantile_5 = np.quantile(prod_error, .05)
            prod_quantile_95 = np.quantile(prod_error, .95)

            prod_mae = np.mean(prod_error)
            prod_mae_under = np.mean(prod_error[prod_error <= prod_quantile_5])
            prod_mae_exp = np.mean(prod_error[(prod_error > prod_quantile_5) & (prod_error < prod_quantile_95)])
            prod_mae_over = np.mean(prod_error[prod_error >= prod_quantile_95])

            prod_sd = np.std(prod_error, ddof = 1)
            prod_sd_under = np.std(prod_error[prod_error <= prod_quantile_5], ddof = 1)
            prod_sd_exp = np.std(prod_error[(prod_error > prod_quantile_5) & (prod_error < prod_quantile_95)], ddof = 1)
            prod_sd_over = np.std(prod_error[prod_error >= prod_quantile_95], ddof = 1)
            
            self.wi = BaseWidgetInfo(
                title="Production: Mean Error per Group (+/- std)",
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
                        "value": str(round(prod_mae_exp, 2)) + " (" + str(round(prod_sd_exp, 2)) + ")",
                        "label": "Majority(90%)"
                      },
                      #{
                      #  "value": str(round(prod_mae_exp, 2)) + " (" + str(round(prod_sd_exp,2)) + ")",
                      #  "label": "Expected"
                      #},
                      {
                        "value": str(round(prod_mae_under, 2)) + " (" + str(round(prod_sd_under, 2)) + ")",
                        "label": "Underestimation(5%)"
                      },
                      {
                        "value": str(round(prod_mae_over, 2)) + " (" + str(round(prod_sd_over, 2)) + ")",
                        "label": "Overestimation(5%)"
                      }
                    ]
                },
                additionalGraphs=[]
            )
        else:
            self.wi = None
