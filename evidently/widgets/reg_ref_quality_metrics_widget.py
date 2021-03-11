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

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class RegRefQualityMetricsWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("No reference data with target and prediction provided")

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

        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)
            
            #calculate quality metrics
            me = np.mean(reference_data[prediction_column] - reference_data[target_column])
            sde = np.std(reference_data[prediction_column] - reference_data[target_column], ddof = 1)

            abs_err = list(map(lambda x : abs(x[0] - x[1]), 
                zip(reference_data[target_column], reference_data[prediction_column])))
            mae = np.mean(abs_err)
            sdae = np.std(abs_err, ddof = 1)

            abs_perc_err = list(map(lambda x : 100*abs(x[0] - x[1])/x[0], 
                zip(reference_data[target_column], reference_data[prediction_column])))
            mape = np.mean(abs_perc_err)
            sdape = np.std(abs_perc_err, ddof = 1)

            #sqrt_err = list(map(lambda x : (x[0] - x[1])**2, 
            #    zip(reference_data[target_column], reference_data[prediction_column])))
            #mse = np.mean(sqrt_err)
            #sdse = np.std(sqrt_err, ddof = 1)

            #error_norm_json = json.loads(error_norm.to_json())

            self.wi = BaseWidgetInfo(
                title="Reference: Model Quality (+/- std)",
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
                        "value": str(round(me, 2)) + " (" + str(round(sde,2)) + ")",
                        "label": "ME"
                      },
                      {
                        "value": str(round(mae, 2)) + " (" + str(round(sdae,2)) + ")",
                        "label": "MAE"
                      },
                      {
                        "value": str(round(mape, 2)) + " (" + str(round(sdape, 2)) + ")",
                        "label": "MAPE"
                      }#,
                      #{
                      #  "value": str(round(mse, 2)) + " (" + str(round(sdse, 2)) + ")",
                      #  "label": "MSE"
                      #}
                    ]
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

