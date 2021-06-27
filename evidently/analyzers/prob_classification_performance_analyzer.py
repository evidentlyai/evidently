#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare
from sklearn import metrics, preprocessing

class ProbClassificationPerformanceAnalyzer(Analyzer):
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

            binaraizer = preprocessing.LabelBinarizer()
            binaraizer.fit(reference_data[target_column])
            binaraized_target = binaraizer.transform(reference_data[target_column])

            array_prediction = reference_data[prediction_column].to_numpy()

            prediction_ids = np.argmax(array_prediction, axis=-1)
            prediction_labels = [prediction_column[x] for x in prediction_ids]

            labels = sorted(set(reference_data[target_column]))

            result['metrics']['reference'] = {}

            #calculate quality metrics
            if len(prediction_column) > 2:
                roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average='macro')
                log_loss = metrics.log_loss(binaraized_target, array_prediction)
            else:
                roc_auc = metrics.roc_auc_score(binaraized_target, reference_data[prediction_column[0]], #problem!!!
                average='macro')
                log_loss = metrics.log_loss(binaraized_target, reference_data[prediction_column[0]]) #problem!!!

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

            #calculate class support and metrics matrix
            metrics_matrix = metrics.classification_report(reference_data[target_column], prediction_labels, 
                output_dict=True)
            result['metrics']['reference']['metrics_matrix'] = metrics_matrix
            if len(prediction_column) > 2:
                roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None)
                result['metrics']['reference']['roc_aucs'] = roc_aucs.tolist()

            #calculate confusion matrix
            conf_matrix = metrics.confusion_matrix(reference_data[target_column], 
                prediction_labels)
            
            result['metrics']['reference']['confusion_matrix'] = {}
            result['metrics']['reference']['confusion_matrix']['labels'] = labels
            result['metrics']['reference']['confusion_matrix']['values'] = conf_matrix.tolist()

            #calulate ROC and PR curves, PR table
            if len(prediction_column) <= 2:
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(reference_data[target_column]))
                binaraized_target.columns = ['target']

                fpr, tpr, thrs = metrics.roc_curve(binaraized_target, reference_data[prediction_column[0]])
                result['metrics']['reference']['roc_curve'] = {'fpr':fpr.tolist(), 'tpr':tpr.tolist(), 'thrs':thrs.tolist()}
                
                pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, reference_data[prediction_column[0]])
                result['metrics']['reference']['pr_curve'] = {'pr':pr.tolist(), 'rcl':rcl.tolist(), 'thrs':thrs.tolist()}

                pr_table = []
                step_size = 0.05
                binded = list(zip(binaraized_target['target'].tolist(),  
                    reference_data[prediction_column[0]].tolist()))
                binded.sort(key = lambda item: item[1], reverse = True)  
                data_size = len(binded)
                target_class_size = sum([x[0] for x in binded])
                offset = max(round(data_size*step_size), 1)
                for step in np.arange(offset, data_size + offset, offset):
                    count = min(step, data_size)
                    prob = round(binded[min(step, data_size-1)][1],2)
                    top = round(100.0*min(step, data_size)/data_size, 1)
                    tp = sum([x[0] for x in binded[:min(step, data_size)]])
                    fp = count - tp
                    precision = round(100.0*tp/count, 1)
                    recall = round(100.0*tp/target_class_size, 1)
                    pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                result['metrics']['reference']['pr_table'] = pr_table

            else:
                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = pd.DataFrame(binaraizer.transform(reference_data[target_column]))
                binaraized_target.columns = prediction_column
                
                result['metrics']['reference']['roc_curve'] = {}
                result['metrics']['reference']['pr_curve'] = {}
                result['metrics']['reference']['pr_table'] = {}
                for label in prediction_column:
                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], reference_data[label])
                    result['metrics']['reference']['roc_curve'][label] = {'fpr':fpr.tolist(), 'tpr':tpr.tolist(), 'thrs':thrs.tolist()}

                    pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], reference_data[label])
                    result['metrics']['reference']['pr_curve'][label] = {'pr':pr.tolist(), 'rcl':rcl.tolist(), 'thrs':thrs.tolist()}

                    pr_table = []
                    step_size = 0.05
                    binded = list(zip(binaraized_target[label].tolist(),  
                        reference_data[label].tolist()))
                    binded.sort(key = lambda item: item[1], reverse = True)
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size*step_size), 1)
                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size-1)][1],2)
                        top = round(100.0*min(step, data_size)/data_size, 1)
                        tp = sum([x[0] for x in binded[:min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0*tp/count, 1)
                        recall = round(100.0*tp/target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                    result['metrics']['reference']['pr_table'][label] = pr_table

            if current_data is not None:
                current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                current_data.dropna(axis=0, how='any', inplace=True)

                binaraizer = preprocessing.LabelBinarizer()
                binaraizer.fit(reference_data[target_column])
                binaraized_target = binaraizer.transform(current_data[target_column])

                array_prediction = current_data[prediction_column].to_numpy()

                prediction_ids = np.argmax(array_prediction, axis=-1)
                prediction_labels = [prediction_column[x] for x in prediction_ids]

                result['metrics']['current'] = {}
            
                #calculate quality metrics
                if len(prediction_column) > 2:
                    roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average='macro')
                    log_loss = metrics.log_loss(binaraized_target, array_prediction)
                else:
                    roc_auc = metrics.roc_auc_score(binaraized_target, current_data[prediction_column[0]]) #problem!!!
                    log_loss = metrics.log_loss(binaraized_target, current_data[prediction_column[0]]) #problem!!!

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

                #calculate class support and metrics matrix
                metrics_matrix = metrics.classification_report(current_data[target_column], prediction_labels,
                    output_dict=True)
                result['metrics']['current']['metrics_matrix'] = metrics_matrix

                if len(prediction_column) > 2:
                    roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None)
                    result['metrics']['current']['roc_aucs'] = roc_aucs.tolist()

                #calculate confusion matrix
                conf_matrix = metrics.confusion_matrix(current_data[target_column], 
                    prediction_labels)
            
                result['metrics']['current']['confusion_matrix'] = {}
                result['metrics']['current']['confusion_matrix']['labels'] = labels
                result['metrics']['current']['confusion_matrix']['values'] = conf_matrix.tolist()

                #calulate ROC and PR curves, PR table
                if len(prediction_column) <= 2:
                    binaraizer = preprocessing.LabelBinarizer()
                    binaraizer.fit(current_data[target_column])
                    binaraized_target = pd.DataFrame(binaraizer.transform(current_data[target_column]))
                    binaraized_target.columns = ['target']

                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target, current_data[prediction_column[0]])
                    result['metrics']['current']['roc_curve'] = {'fpr':fpr.tolist(), 'tpr':tpr.tolist(), 'thrs':thrs.tolist()}
                    
                    pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, current_data[prediction_column[0]])
                    result['metrics']['current']['pr_curve'] = {'pr':pr.tolist(), 'rcl':rcl.tolist(), 'thrs':thrs.tolist()}

                    pr_table = []
                    step_size = 0.05
                    binded = list(zip(binaraized_target['target'].tolist(),  
                        current_data[prediction_column[0]].tolist()))
                    binded.sort(key = lambda item: item[1], reverse = True)  
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size*step_size), 1)
                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size-1)][1],2)
                        top = round(100.0*min(step, data_size)/data_size, 1)
                        tp = sum([x[0] for x in binded[:min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0*tp/count, 1)
                        recall = round(100.0*tp/target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                    result['metrics']['current']['pr_table'] = pr_table

                else:
                    binaraizer = preprocessing.LabelBinarizer()
                    binaraizer.fit(current_data[target_column])
                    binaraized_target = pd.DataFrame(binaraizer.transform(current_data[target_column]))
                    binaraized_target.columns = prediction_column
                    
                    result['metrics']['current']['roc_curve'] = {}
                    result['metrics']['current']['pr_curve'] = {}
                    result['metrics']['current']['pr_table'] = {}
                    for label in prediction_column:
                        fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], current_data[label])
                        result['metrics']['current']['roc_curve'][label] = {'fpr':fpr.tolist(), 'tpr':tpr.tolist(), 'thrs':thrs.tolist()}

                        pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], current_data[label])
                        result['metrics']['current']['pr_curve'][label] = {'pr':pr.tolist(), 'rcl':rcl.tolist(), 'thrs':thrs.tolist()}

                        pr_table = []
                        step_size = 0.05
                        binded = list(zip(binaraized_target[label].tolist(),  
                            current_data[label].tolist()))
                        binded.sort(key = lambda item: item[1], reverse = True)
                        data_size = len(binded)
                        target_class_size = sum([x[0] for x in binded])
                        offset = max(round(data_size*step_size), 1)
                        for step in np.arange(offset, data_size + offset, offset):
                            count = min(step, data_size)
                            prob = round(binded[min(step, data_size-1)][1],2)
                            top = round(100.0*min(step, data_size)/data_size, 1)
                            tp = sum([x[0] for x in binded[:min(step, data_size)]])
                            fp = count - tp
                            precision = round(100.0*tp/count, 1)
                            recall = round(100.0*tp/target_class_size, 1)
                            pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                        result['metrics']['current']['pr_table'][label] = pr_table

        return result
