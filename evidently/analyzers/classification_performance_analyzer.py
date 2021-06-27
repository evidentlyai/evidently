#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
from sklearn import metrics

class ClassificationPerformanceAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        result = dict()
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            target_names = column_mapping.get('target_names')
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

            target_names = None

        result["utility_columns"] = {'date':date_column, 'id':id_column, 'target':target_column, 'prediction':prediction_column}
        result["cat_feature_names"] = cat_feature_names
        result["num_feature_names"] = num_feature_names
        result["target_names"] = target_names

        result['metrics'] = {}
        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            result['metrics']['reference'] = {}

            #calculate quality metrics
            accuracy_score = metrics.accuracy_score(reference_data[target_column], reference_data[prediction_column])
            avg_precision = metrics.precision_score(reference_data[target_column], reference_data[prediction_column],
                average='macro')
            avg_recall = metrics.recall_score(reference_data[target_column], reference_data[prediction_column],
                average='macro')
            avg_f1 = metrics.f1_score(reference_data[target_column], reference_data[prediction_column],
                average='macro')

            result['metrics']['reference']['accuracy'] = accuracy_score
            result['metrics']['reference']['precision'] = avg_precision
            result['metrics']['reference']['recall'] = avg_recall
            result['metrics']['reference']['f1'] = avg_f1

            #calculate class support and metrics matrix
            metrics_matrix = metrics.classification_report(reference_data[target_column], reference_data[prediction_column],
             output_dict=True)

            result['metrics']['reference']['metrics_matrix'] = metrics_matrix

            #calculate confusion matrix
            conf_matrix = metrics.confusion_matrix(reference_data[target_column], 
                reference_data[prediction_column])
            labels = target_names if target_names else sorted(set(reference_data[target_column]))
            
            result['metrics']['reference']['confusion_matrix'] = {}
            result['metrics']['reference']['confusion_matrix']['labels'] = labels
            result['metrics']['reference']['confusion_matrix']['values'] = conf_matrix.tolist()

            if current_data is not None:
                current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                current_data.dropna(axis=0, how='any', inplace=True)

                result['metrics']['current'] = {}
            
                accuracy_score = metrics.accuracy_score(current_data[target_column], current_data[prediction_column])
                avg_precision = metrics.precision_score(current_data[target_column], current_data[prediction_column],
                    average='macro')
                avg_recall = metrics.recall_score(current_data[target_column], current_data[prediction_column],
                    average='macro')
                avg_f1 = metrics.f1_score(current_data[target_column], current_data[prediction_column],
                    average='macro')

                result['metrics']['current']['accuracy'] = accuracy_score
                result['metrics']['current']['precision'] = avg_precision
                result['metrics']['current']['recall'] = avg_recall
                result['metrics']['current']['f1'] = avg_f1

                #calculate class support and metrics matrix
                metrics_matrix = metrics.classification_report(current_data[target_column], current_data[prediction_column],
                 output_dict=True)

                result['metrics']['current']['metrics_matrix'] = metrics_matrix

                #calculate confusion matrix
                conf_matrix = metrics.confusion_matrix(current_data[target_column],
                    current_data[prediction_column])
                labels = target_names if target_names else sorted(set(current_data[target_column]))
            
                result['metrics']['current']['confusion_matrix'] = {}
                result['metrics']['current']['confusion_matrix']['labels'] = labels
                result['metrics']['current']['confusion_matrix']['values'] = conf_matrix.tolist()

        return result
