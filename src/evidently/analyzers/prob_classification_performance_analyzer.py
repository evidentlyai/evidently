#!/usr/bin/env python
# coding: utf-8
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import pandas as pd
from sklearn import metrics

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.base_analyzer import BaseAnalyzerResult
from evidently.calculations.classification_performance import calculate_confusion_by_classes
from evidently.options import QualityMetricsOptions
from evidently.utils.data_operations import process_columns


@dataclass
class ConfusionMatrix:
    labels: List[str]
    values: list


@dataclass
class ProbClassificationPerformanceMetrics:
    """Class for performance metrics values"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    log_loss: float
    metrics_matrix: dict
    confusion_matrix: ConfusionMatrix
    confusion_by_classes: Dict[Union[str, int], Dict[str, int]]
    roc_aucs: Optional[list] = None
    roc_curve: Optional[dict] = None
    pr_curve: Optional[dict] = None
    pr_table: Optional[Union[dict, list]] = None


@dataclass
class ProbClassificationPerformanceAnalyzerResults(BaseAnalyzerResult):
    quality_metrics_options: QualityMetricsOptions
    reference_metrics: Optional[ProbClassificationPerformanceMetrics] = None
    current_metrics: Optional[ProbClassificationPerformanceMetrics] = None


class ProbClassificationPerformanceAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> ProbClassificationPerformanceAnalyzerResults:
        return analyzer_results[ProbClassificationPerformanceAnalyzer]

    def calculate(
        self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame], column_mapping: ColumnMapping
    ) -> ProbClassificationPerformanceAnalyzerResults:
        if reference_data is None:
            raise ValueError("reference_data should be present")

        columns = process_columns(reference_data, column_mapping)
        target_column = columns.utility_columns.target
        prediction_column = columns.utility_columns.prediction
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        result = ProbClassificationPerformanceAnalyzerResults(
            columns=columns,
            quality_metrics_options=quality_metrics_options,
        )
        classification_threshold = quality_metrics_options.classification_threshold

        if target_column is not None and prediction_column is not None:
            target_and_preds = [target_column]
            if isinstance(prediction_column, str):
                target_and_preds += [prediction_column]
            else:
                target_and_preds += prediction_column
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how="any", inplace=True, subset=target_and_preds)
            binaraized_target = (reference_data[target_column].values.reshape(-1, 1) == prediction_column).astype(int)
            array_prediction = reference_data[prediction_column].to_numpy()

            if len(prediction_column) > 2:
                prediction_ids = np.argmax(array_prediction, axis=-1)
                prediction_labels = [prediction_column[x] for x in prediction_ids]

            else:
                maper = {True: prediction_column[0], False: prediction_column[1]}
                prediction_labels = (reference_data[prediction_column[0]] >= classification_threshold).map(maper)

            labels = sorted(set(reference_data[target_column]))

            # calculate quality metrics
            roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average="macro")
            log_loss = metrics.log_loss(binaraized_target, array_prediction)
            accuracy_score = metrics.accuracy_score(reference_data[target_column], prediction_labels)
            avg_precision = metrics.precision_score(reference_data[target_column], prediction_labels, average="macro")
            avg_recall = metrics.recall_score(reference_data[target_column], prediction_labels, average="macro")
            avg_f1 = metrics.f1_score(reference_data[target_column], prediction_labels, average="macro")

            # calculate class support and metrics matrix
            metrics_matrix = metrics.classification_report(
                reference_data[target_column], prediction_labels, output_dict=True
            )

            roc_aucs = None

            if len(prediction_column) > 2:
                roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None).tolist()

            # calculate confusion matrix
            conf_matrix = metrics.confusion_matrix(reference_data[target_column], prediction_labels)
            confusion_by_classes = calculate_confusion_by_classes(conf_matrix, labels)

            result.reference_metrics = ProbClassificationPerformanceMetrics(
                accuracy=accuracy_score,
                precision=avg_precision,
                recall=avg_recall,
                f1=avg_f1,
                roc_auc=roc_auc,
                log_loss=log_loss,
                metrics_matrix=metrics_matrix,
                confusion_matrix=ConfusionMatrix(labels=labels, values=conf_matrix.tolist()),
                roc_aucs=roc_aucs,
                confusion_by_classes=confusion_by_classes,
            )

            # calculate ROC and PR curves, PR table
            if len(prediction_column) <= 2:
                binaraized_target = pd.DataFrame(binaraized_target[:, 0])
                binaraized_target.columns = ["target"]

                fpr, tpr, thrs = metrics.roc_curve(binaraized_target, reference_data[prediction_column[0]])
                result.reference_metrics.roc_curve = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "thrs": thrs.tolist()}

                pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target, reference_data[prediction_column[0]])
                result.reference_metrics.pr_curve = {"pr": pr.tolist(), "rcl": rcl.tolist(), "thrs": thrs.tolist()}

                pr_table = []
                step_size = 0.05
                binded = list(zip(binaraized_target["target"].tolist(), reference_data[prediction_column[0]].tolist()))
                binded.sort(key=lambda item: item[1], reverse=True)
                data_size = len(binded)
                target_class_size = sum([x[0] for x in binded])
                offset = max(round(data_size * step_size), 1)

                for step in np.arange(offset, data_size + offset, offset):
                    count = min(step, data_size)
                    prob = round(binded[min(step, data_size - 1)][1], 2)
                    top = round(100.0 * min(step, data_size) / data_size, 1)
                    tp = sum([x[0] for x in binded[: min(step, data_size)]])
                    fp = count - tp
                    precision = round(100.0 * tp / count, 1)
                    recall = round(100.0 * tp / target_class_size, 1)
                    pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])

                result.reference_metrics.pr_table = pr_table

            else:
                binaraized_target = pd.DataFrame(binaraized_target)
                binaraized_target.columns = prediction_column

                result.reference_metrics.roc_curve = {}
                result.reference_metrics.pr_curve = {}
                result.reference_metrics.pr_table = {}

                for label in prediction_column:
                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], reference_data[label])
                    result.reference_metrics.roc_curve[label] = {
                        "fpr": fpr.tolist(),
                        "tpr": tpr.tolist(),
                        "thrs": thrs.tolist(),
                    }

                    pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], reference_data[label])
                    result.reference_metrics.pr_curve[label] = {
                        "pr": pr.tolist(),
                        "rcl": rcl.tolist(),
                        "thrs": thrs.tolist(),
                    }

                    pr_table = []
                    step_size = 0.05
                    binded = list(zip(binaraized_target[label].tolist(), reference_data[label].tolist()))
                    binded.sort(key=lambda item: item[1], reverse=True)
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size * step_size), 1)

                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size - 1)][1], 2)
                        top = round(100.0 * min(step, data_size) / data_size, 1)
                        tp = sum([x[0] for x in binded[: min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0 * tp / count, 1)
                        recall = round(100.0 * tp / target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])
                    result.reference_metrics.pr_table[label] = pr_table

            if current_data is not None:
                current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                current_data.dropna(axis=0, how="any", inplace=True, subset=target_and_preds)

                binaraized_target = (current_data[target_column].values.reshape(-1, 1) == prediction_column).astype(int)

                array_prediction = current_data[prediction_column].to_numpy()

                if len(prediction_column) > 2:
                    prediction_ids = np.argmax(array_prediction, axis=-1)
                    prediction_labels = [prediction_column[x] for x in prediction_ids]

                else:
                    maper = {True: prediction_column[0], False: prediction_column[1]}
                    prediction_labels = (current_data[prediction_column[0]] >= classification_threshold).map(maper)

                # calculate quality metrics
                roc_auc = metrics.roc_auc_score(binaraized_target, array_prediction, average="macro")
                log_loss = metrics.log_loss(binaraized_target, array_prediction)
                accuracy_score = metrics.accuracy_score(current_data[target_column], prediction_labels)
                avg_precision = metrics.precision_score(current_data[target_column], prediction_labels, average="macro")
                avg_recall = metrics.recall_score(current_data[target_column], prediction_labels, average="macro")
                avg_f1 = metrics.f1_score(current_data[target_column], prediction_labels, average="macro")

                # calculate class support and metrics matrix
                metrics_matrix = metrics.classification_report(
                    current_data[target_column], prediction_labels, output_dict=True
                )

                roc_aucs = None

                if len(prediction_column) > 2:
                    roc_aucs = metrics.roc_auc_score(binaraized_target, array_prediction, average=None).tolist()

                # calculate confusion matrix
                conf_matrix = metrics.confusion_matrix(current_data[target_column], prediction_labels)
                # get TP, FP, TN, FN metrics for each class
                confusion_by_classes = calculate_confusion_by_classes(conf_matrix, labels)

                result.current_metrics = ProbClassificationPerformanceMetrics(
                    accuracy=accuracy_score,
                    precision=avg_precision,
                    recall=avg_recall,
                    f1=avg_f1,
                    roc_auc=roc_auc,
                    log_loss=log_loss,
                    metrics_matrix=metrics_matrix,
                    confusion_matrix=ConfusionMatrix(labels=labels, values=conf_matrix.tolist()),
                    roc_aucs=roc_aucs,
                    confusion_by_classes=confusion_by_classes,
                )

                # calculate ROC and PR curves, PR table
                if len(prediction_column) <= 2:
                    binaraized_target = pd.DataFrame(binaraized_target[:, 0])
                    binaraized_target.columns = ["target"]

                    fpr, tpr, thrs = metrics.roc_curve(binaraized_target, current_data[prediction_column[0]])
                    result.current_metrics.roc_curve = {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "thrs": thrs.tolist()}

                    pr, rcl, thrs = metrics.precision_recall_curve(
                        binaraized_target, current_data[prediction_column[0]]
                    )
                    result.current_metrics.pr_curve = {"pr": pr.tolist(), "rcl": rcl.tolist(), "thrs": thrs.tolist()}

                    pr_table = []
                    step_size = 0.05
                    binded = list(
                        zip(binaraized_target["target"].tolist(), current_data[prediction_column[0]].tolist())
                    )
                    binded.sort(key=lambda item: item[1], reverse=True)
                    data_size = len(binded)
                    target_class_size = sum([x[0] for x in binded])
                    offset = max(round(data_size * step_size), 1)

                    for step in np.arange(offset, data_size + offset, offset):
                        count = min(step, data_size)
                        prob = round(binded[min(step, data_size - 1)][1], 2)
                        top = round(100.0 * min(step, data_size) / data_size, 1)
                        tp = sum([x[0] for x in binded[: min(step, data_size)]])
                        fp = count - tp
                        precision = round(100.0 * tp / count, 1)
                        recall = round(100.0 * tp / target_class_size, 1)
                        pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])

                    result.current_metrics.pr_table = pr_table

                else:
                    binaraized_target = pd.DataFrame(binaraized_target)
                    binaraized_target.columns = prediction_column

                    result.current_metrics.roc_curve = {}
                    result.current_metrics.pr_curve = {}
                    result.current_metrics.pr_table = {}

                    for label in prediction_column:
                        fpr, tpr, thrs = metrics.roc_curve(binaraized_target[label], current_data[label])
                        result.current_metrics.roc_curve[label] = {
                            "fpr": fpr.tolist(),
                            "tpr": tpr.tolist(),
                            "thrs": thrs.tolist(),
                        }

                        pr, rcl, thrs = metrics.precision_recall_curve(binaraized_target[label], current_data[label])
                        result.current_metrics.pr_curve[label] = {
                            "pr": pr.tolist(),
                            "rcl": rcl.tolist(),
                            "thrs": thrs.tolist(),
                        }

                        pr_table = []
                        step_size = 0.05
                        binded = list(zip(binaraized_target[label].tolist(), current_data[label].tolist()))
                        binded.sort(key=lambda item: item[1], reverse=True)
                        data_size = len(binded)
                        target_class_size = sum([x[0] for x in binded])
                        offset = max(round(data_size * step_size), 1)

                        for step in np.arange(offset, data_size + offset, offset):
                            count = min(step, data_size)
                            prob = round(binded[min(step, data_size - 1)][1], 2)
                            top = round(100.0 * min(step, data_size) / data_size, 1)
                            tp = sum([x[0] for x in binded[: min(step, data_size)]])
                            fp = count - tp
                            precision = round(100.0 * tp / count, 1)
                            recall = round(100.0 * tp / target_class_size, 1)
                            pr_table.append([top, int(count), prob, int(tp), int(fp), precision, recall])

                        result.current_metrics.pr_table[label] = pr_table

        return result
