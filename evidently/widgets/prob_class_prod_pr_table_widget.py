#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

import numpy as np

from sklearn import metrics, preprocessing
from pandas.api.types import is_numeric_dtype

import plotly.graph_objs as go
import plotly.figure_factory as ff

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo, TabInfo
from evidently.widgets.widget import Widget

red = "#ed0400"
grey = "#4d4d4d"


class ProbClassProdPRTableWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def analyzers(self):
        return []

    def get_info(self) -> BaseWidgetInfo:
        #if self.wi:
        return self.wi
        #raise ValueError("No prediction or target data provided")

    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping, analyzes_results):
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            #target_names = column_mapping.get('target_names')
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

            #target_names = None

        if current_data is not None and target_column is not None and prediction_column is not None:
            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            #array_prediction = reference_data[prediction_column].to_numpy()

            #prediction_ids = np.argmax(array_prediction, axis=-1)
            #prediction_labels = [prediction_column[x] for x in prediction_ids]
            if len(prediction_column) <= 2:
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(current_data[target_column]))
                binaraized_target.columns = ['target']

                params_data = []

                step_size = 0.05
                binded = list(zip(binaraized_target['target'].tolist(),  
                    current_data[prediction_column[0]].tolist()))
                binded.sort(key = lambda item: item[1], reverse = True)
                
                data_size = len(binded)
                target_class_size = sum([x[0] for x in binded])

                #result = pd.DataFrame(columns = ['Top(%)', 'Count', 'TP', 'FP', 'precision', 'recall'])

                offset = max(round(data_size*step_size), 1)
                for step in np.arange(offset, data_size + offset, offset):
                    count = min(step, data_size)
                    prob = round(binded[min(step, data_size-1)][1],2)
                    top = round(100.0*min(step, data_size)/data_size, 1)
                    tp = sum([x[0] for x in binded[:min(step, data_size)]])
                    fp = count - tp
                    precision = round(100.0*tp/count, 1)
                    recall = round(100.0*tp/target_class_size, 1)

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
                size=1,
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
                            "field": "f2",
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
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(current_data[target_column]))
                binaraized_target.columns = prediction_column
                
                #create tables
                tabs = []

                for label in prediction_column:
                    params_data = []

                    step_size = 0.05
                    binded = list(zip(binaraized_target[label].tolist(),  
                        current_data[label].tolist()))
                    binded.sort(key = lambda item: item[1], reverse = True)
                    
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])

                    #result = pd.DataFrame(columns = ['Top(%)', 'Count', 'TP', 'FP', 'precision', 'recall'])

                    offset = max(round(data_size*step_size), 1)
                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size-1)][1],2)
                        top = round(100.0*min(step, data_size)/data_size, 1)
                        tp = sum([x[0] for x in binded[:min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0*tp/count, 1)
                        recall = round(100.0*tp/target_class_size, 1)

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
                            size=2,
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
                                        "field": "f2", 
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
                    ))

                self.wi = BaseWidgetInfo(
                    type="tabs",
                    title=self.title,
                    size=1,
                    details="",
                    tabs=tabs
                )
        else:
            self.wi = None

