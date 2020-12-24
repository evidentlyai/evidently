#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import chisquare
#import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class CatTargetDriftWidget(Widget):
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

        if target_column is not None:
            #calculate output drift
            ref_feature_vc = reference_data[target_column][np.isfinite(reference_data[target_column])].value_counts()
            prod_feature_vc = production_data[target_column][np.isfinite(production_data[target_column])].value_counts()

            keys = set(list(reference_data[target_column][np.isfinite(reference_data[target_column])].unique()) + 
                list(production_data[target_column][np.isfinite(production_data[target_column])].unique()))

            ref_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(ref_feature_vc.index, ref_feature_vc.values):
                ref_feature_dict[key] = item

            prod_feature_dict = dict.fromkeys(keys, 0)
            for key, item in zip(prod_feature_vc.index, prod_feature_vc.values):
                prod_feature_dict[key] = item

            f_exp = [value[1] for value in sorted(ref_feature_dict.items())]
            f_obs = [value[1] for value in sorted(prod_feature_dict.items())]

            target_p_value = chisquare(f_exp, f_obs)[1]

            target_sim_test = "detected" if target_p_value < 0.05 else "not detected"

            #plot output distributions
            fig = go.Figure()

            fig.add_trace(go.Histogram(x=reference_data[target_column], 
                 marker_color=grey, opacity=0.6, nbinsx=10,  name='Reference', histnorm='probability'))

            fig.add_trace(go.Histogram(x=production_data[target_column],
                 marker_color=red, opacity=0.6,nbinsx=10, name='Production', histnorm='probability'))

            fig.update_layout(
                legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
                ),
                xaxis_title = target_column,
                yaxis_title = "Share"
            )

            target_drift_json  = json.loads(fig.to_json())

            self.wi = BaseWidgetInfo(
                title="Target Drift: " + target_sim_test + ", p_value=" + str(round(target_p_value, 6)),
                type="big_graph",
                details="",
                alertStats=AlertStats(),
                alerts=[],
                alertsPosition="row",
                insights=[],
                size=2,
                params={
                    "data": target_drift_json['data'],
                    "layout": target_drift_json['layout']
                },
                additionalGraphs=[],
            )
        else:
            self.wi = None
