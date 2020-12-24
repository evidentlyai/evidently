#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class NumTargetCorrWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        return self.wi
        #raise ValueError("No prediction data provided")

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

        if target_column is not None:

            #calculate corr
            ref_target_corr = reference_data.corr()[target_column]
            prod_target_corr = production_data.corr()[target_column]
            
            #plot output correlations
            target_corr = go.Figure()

            target_corr.add_trace(go.Bar(y = ref_target_corr, x = ref_target_corr.index, 
                marker_color = grey, name = 'Reference'))

            target_corr.add_trace(go.Bar(y = prod_target_corr, x = ref_target_corr.index, 
                marker_color = red, name = 'Production'))

            target_corr.update_layout(xaxis_title = "Features", yaxis_title = "Correlation",
                yaxis = dict(
                    range=(-1, 1),
                    showticklabels=True
                ))

            target_corr_json  = json.loads(target_corr.to_json())

            self.wi = BaseWidgetInfo(
                title=self.title,
                type="big_graph",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=1,
                params={
                    "data": target_corr_json['data'],
                    "layout": target_corr_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None

