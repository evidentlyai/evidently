#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn import metrics

from evidently.analyzers.base_analyzer import Analyzer
from .utils import process_columns


class ClassificationPerformanceAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, current_data: pd.DataFrame, column_mapping):
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction
        target_names = columns.target_names

        result['metrics'] = {}
        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            result['metrics']['reference'] = {}

            # calculate quality metrics
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

            # calculate class support and metrics matrix
            metrics_matrix = metrics.classification_report(
                reference_data[target_column],
                reference_data[prediction_column],
                output_dict=True)

            result['metrics']['reference']['metrics_matrix'] = metrics_matrix

            # calculate confusion matrix
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

                # calculate class support and metrics matrix
                metrics_matrix = metrics.classification_report(current_data[target_column],
                                                               current_data[prediction_column],
                                                               output_dict=True)

                result['metrics']['current']['metrics_matrix'] = metrics_matrix

                # calculate confusion matrix
                conf_matrix = metrics.confusion_matrix(current_data[target_column],
                                                       current_data[prediction_column])
                labels = target_names if target_names else sorted(set(current_data[target_column]))

                result['metrics']['current']['confusion_matrix'] = {}
                result['metrics']['current']['confusion_matrix']['labels'] = labels
                result['metrics']['current']['confusion_matrix']['values'] = conf_matrix.tolist()

        return result
