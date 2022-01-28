#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.utils import process_columns
from evidently.options import QualityMetricsOptions


class ProbClassificationPerformanceAnalyzer(Analyzer):
    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping):
        columns = process_columns(reference_data, column_mapping)
        result = columns.as_dict()

        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        classification_threshold = quality_metrics_options.classification_threshold

        result['options'] = quality_metrics_options.as_dict()
        result['metrics'] = {}
        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            binaraized_target = (reference_data[target_column].values.reshape(-1, 1) == prediction_column).astype(int)

            array_prediction = reference_data[prediction_column].to_numpy()

            if len(prediction_column) > 2:
                prediction_ids = np.argmax(array_prediction, axis=-1)
                prediction_labels = [prediction_column[x] for x in prediction_ids]
            else:
                maper = {True: prediction_column[0], False: prediction_column[1]}
                prediction_labels = (reference_data[prediction_column[0]] >= classification_threshold).map(maper)

            labels = sorted(set(reference_data[target_column]))

            result['metrics']['reference'] = {}

            # calculate quality metrics
            roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average='macro')
            log_loss = metrics.log_loss(binaraized_target, array_prediction)
            accuracy_score = metrics.accuracy_score(reference_data[target_column], prediction_labels)
            avg_precision = metrics.precision_score(reference_data[target_column], prediction_labels,
                                                    average='macro')
            avg_recall = metrics.recall_score(reference_data[target_column], prediction_labels,
                                              average='macro')
            avg_f1 = metrics.f1_score(reference_data[target_column], prediction_labels,
                                      average='macro')

            result['metrics']['reference']['accuracy'] = accuracy_score
            result['metrics']['reference']['precision'] = avg_precision
            result['metrics']['reference']['recall'] = avg_recall
            result['metrics']['reference']['f1'] = avg_f1
            result['metrics']['reference']['roc_auc'] = roc_auc
            result['metrics']['reference']['log_loss'] = log_loss

            # calculate class support and metrics matrix
            metrics_matrix = metrics.classification_report(reference_data[target_column], prediction_labels,
                                                           output_dict=True)
            result['metrics']['reference']['metrics_matrix'] = metrics_matrix
            if len(prediction_column) > 2:
                roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None)
                result['metrics']['reference']['roc_aucs'] = roc_aucs.tolist()

            # calculate confusion matrix
            conf_matrix = metrics.confusion_matrix(reference_data[target_column], prediction_labels)

            result['metrics']['reference']['confusion_matrix'] = {}
            result['metrics']['reference']['confusion_matrix']['labels'] = labels
            result['metrics']['reference']['confusion_matrix']['values'] = conf_matrix.tolist()

            # calulate ROC and PR curves, PR table
            if len(prediction_column) <= 2:
                binaraized_target = pd.DataFrame(binaraized_target[:, 0])
                binaraized_target.columns = ['target']

                fpr, tpr, thrs = metrics.roc_curve(binaraized_target, reference_data[prediction_column[0]])
                result['metrics']['reference']['roc_curve'] = {'fpr': fpr.tolist(), 'tpr': tpr.tolist(),
                                                               'thrs': thrs.tolist()}

                pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, reference_data[prediction_column[0]])
                result['metrics']['reference']['pr_curve'] = {'pr': pr.tolist(), 'rcl': rcl.tolist(),
                                                              'thrs': thrs.tolist()}

                pr_table = []
                step_size = 0.05
                binded = list(zip(binaraized_target['target'].tolist(),
                                  reference_data[prediction_column[0]].tolist()))
                binded.sort(key=lambda item: item[1], reverse=True)
                data_size = len(binded)
                target_class_size = sum([x[0] for x in binded])
                offset = max(round(data_size * step_size), 1)
                for step in np.arange(offset, data_size + offset, offset):
                    count = min(step, data_size)
                    prob = round(binded[min(step, data_size - 1)][1], 2)
                    top = round(100.0 * min(step, data_size) / data_size, 1)
                    tp = sum([x[0] for x in binded[:min(step, data_size)]])
                    fp = count - tp
                    precision = round(100.0 * tp / count, 1)
                    recall = round(100.0 * tp / target_class_size, 1)
                    pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                result['metrics']['reference']['pr_table'] = pr_table

            else:
                binaraized_target = pd.DataFrame(binaraized_target)
                binaraized_target.columns = prediction_column

                result['metrics']['reference']['roc_curve'] = {}
                result['metrics']['reference']['pr_curve'] = {}
                result['metrics']['reference']['pr_table'] = {}
                for label in prediction_column:
                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], reference_data[label])
                    result['metrics']['reference']['roc_curve'][label] = {'fpr': fpr.tolist(), 'tpr': tpr.tolist(),
                                                                          'thrs': thrs.tolist()}

                    pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], reference_data[label])
                    result['metrics']['reference']['pr_curve'][label] = {'pr': pr.tolist(), 'rcl': rcl.tolist(),
                                                                         'thrs': thrs.tolist()}

                    pr_table = []
                    step_size = 0.05
                    binded = list(zip(binaraized_target[label].tolist(),
                                      reference_data[label].tolist()))
                    binded.sort(key=lambda item: item[1], reverse=True)
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size * step_size), 1)
                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size - 1)][1], 2)
                        top = round(100.0 * min(step, data_size) / data_size, 1)
                        tp = sum([x[0] for x in binded[:min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0 * tp / count, 1)
                        recall = round(100.0 * tp / target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                    result['metrics']['reference']['pr_table'][label] = pr_table

            if current_data is not None:
                current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                current_data.dropna(axis=0, how='any', inplace=True)

                binaraized_target = (current_data[target_column].values.reshape(-1, 1) == prediction_column).astype(int)

                array_prediction = current_data[prediction_column].to_numpy()

                if len(prediction_column) > 2:
                    prediction_ids = np.argmax(array_prediction, axis=-1)
                    prediction_labels = [prediction_column[x] for x in prediction_ids]
                else:
                    maper = {True: prediction_column[0], False: prediction_column[1]}
                    prediction_labels = (current_data[prediction_column[0]] >= classification_threshold).map(maper)

                result['metrics']['current'] = {}

                # calculate quality metrics
                roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average='macro')
                log_loss = metrics.log_loss(binaraized_target, array_prediction)
                accuracy_score = metrics.accuracy_score(current_data[target_column], prediction_labels)
                avg_precision = metrics.precision_score(current_data[target_column], prediction_labels,
                                                        average='macro')
                avg_recall = metrics.recall_score(current_data[target_column], prediction_labels,
                                                  average='macro')
                avg_f1 = metrics.f1_score(current_data[target_column], prediction_labels,
                                          average='macro')

                result['metrics']['current']['accuracy'] = accuracy_score
                result['metrics']['current']['precision'] = avg_precision
                result['metrics']['current']['recall'] = avg_recall
                result['metrics']['current']['f1'] = avg_f1
                result['metrics']['current']['roc_auc'] = roc_auc
                result['metrics']['current']['log_loss'] = log_loss

                # calculate class support and metrics matrix
                metrics_matrix = metrics.classification_report(current_data[target_column], prediction_labels,
                                                               output_dict=True)
                result['metrics']['current']['metrics_matrix'] = metrics_matrix

                if len(prediction_column) > 2:
                    roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None)
                    result['metrics']['current']['roc_aucs'] = roc_aucs.tolist()

                # calculate confusion matrix
                conf_matrix = metrics.confusion_matrix(current_data[target_column], prediction_labels)
                result['metrics']['current']['confusion_matrix'] = {}
                result['metrics']['current']['confusion_matrix']['labels'] = labels
                result['metrics']['current']['confusion_matrix']['values'] = conf_matrix.tolist()

                # calulate ROC and PR curves, PR table
                if len(prediction_column) <= 2:
                    binaraized_target = pd.DataFrame(binaraized_target[:, 0])
                    binaraized_target.columns = ['target']

                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target, current_data[prediction_column[0]])
                    result['metrics']['current']['roc_curve'] = {'fpr': fpr.tolist(), 'tpr': tpr.tolist(),
                                                                 'thrs': thrs.tolist()}

                    pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target,
                                                                   current_data[prediction_column[0]])
                    result['metrics']['current']['pr_curve'] = {'pr': pr.tolist(), 'rcl': rcl.tolist(),
                                                                'thrs': thrs.tolist()}

                    pr_table = []
                    step_size = 0.05
                    binded = list(zip(binaraized_target['target'].tolist(),
                                      current_data[prediction_column[0]].tolist()))
                    binded.sort(key=lambda item: item[1], reverse=True)
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size * step_size), 1)
                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size - 1)][1], 2)
                        top = round(100.0 * min(step, data_size) / data_size, 1)
                        tp = sum([x[0] for x in binded[:min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0 * tp / count, 1)
                        recall = round(100.0 * tp / target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                    result['metrics']['current']['pr_table'] = pr_table

                else:
                    binaraized_target = pd.DataFrame(binaraized_target)
                    binaraized_target.columns = prediction_column

                    result['metrics']['current']['roc_curve'] = {}
                    result['metrics']['current']['pr_curve'] = {}
                    result['metrics']['current']['pr_table'] = {}
                    for label in prediction_column:
                        fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], current_data[label])
                        result['metrics']['current']['roc_curve'][label] = {'fpr': fpr.tolist(), 'tpr': tpr.tolist(),
                                                                            'thrs': thrs.tolist()}

                        pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], current_data[label])
                        result['metrics']['current']['pr_curve'][label] = {'pr': pr.tolist(), 'rcl': rcl.tolist(),
                                                                           'thrs': thrs.tolist()}

                        pr_table = []
                        step_size = 0.05
                        binded = list(zip(binaraized_target[label].tolist(),
                                          current_data[label].tolist()))
                        binded.sort(key=lambda item: item[1], reverse=True)
                        data_size = len(binded)
                        target_class_size = sum([x[0] for x in binded])
                        offset = max(round(data_size * step_size), 1)
                        for step in np.arange(offset, data_size + offset, offset):
                            count = min(step, data_size)
                            prob = round(binded[min(step, data_size - 1)][1], 2)
                            top = round(100.0 * min(step, data_size) / data_size, 1)
                            tp = sum([x[0] for x in binded[:min(step, data_size)]])
                            fp = count - tp
                            precision = round(100.0 * tp / count, 1)
                            recall = round(100.0 * tp / target_class_size, 1)
                            pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                        result['metrics']['current']['pr_table'][label] = pr_table

        return result
