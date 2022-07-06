import abc
from typing import Optional

import numpy as np

from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetrics
from evidently.metrics.classification_performance_metrics import DatasetClassificationPerformanceMetrics
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestResult


class SimpleClassificationTest(Test):
    group = "classification"
    name: str
    metric: ClassificationPerformanceMetrics

    def __init__(self, threshold: Optional[float] = None, metric: Optional[ClassificationPerformanceMetrics] = None):
        if metric is None:
            metric = ClassificationPerformanceMetrics()
        self.metric = metric
        self.threshold = threshold

    def check(self):
        metrics = self.metric.get_result().current_metrics
        ref_metrics = self.metric.get_result().reference_metrics
        dummy_metrics = self.metric.get_result().dummy_metrics
        if self.threshold:
            return self._compare(self.get_value(metrics), self.threshold)
        if ref_metrics:
            return self._compare_with_reference(self.get_value(metrics), self.get_value(ref_metrics))
        return self._compare(self.get_value(metrics), self.get_value(dummy_metrics))

    @abc.abstractmethod
    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        raise NotImplementedError()

    @abc.abstractmethod
    def _success_description(self, actual_value: float, threshold: float):
        raise NotImplementedError()

    @abc.abstractmethod
    def _fail_description(self, actual_value: float, threshold: float):
        raise NotImplementedError()

    @abc.abstractmethod
    def _success_description_reference(self, actual_value: float, reference_value: float):
        raise NotImplementedError()

    @abc.abstractmethod
    def _fail_description_reference(self, actual_value: float, reference_value: float):
        raise NotImplementedError()

    def _compare(self, actual_value: float, threshold: float):
        if actual_value > threshold:
            return TestResult(
                name=self.name,
                description=self._success_description(actual_value, threshold),
                status=TestResult.SUCCESS,
            )
        return TestResult(
            name=self.name, description=self._fail_description(actual_value, threshold), status=TestResult.FAIL
        )

    def _compare_with_reference(self, actual_value: float, reference_value: float):
        if np.isclose(actual_value, reference_value, atol=0.1):
            return TestResult(
                name=self.name,
                description=self._success_description_reference(actual_value, reference_value),
                status=TestResult.SUCCESS,
            )
        return TestResult(
            name=self.name,
            description=self._fail_description_reference(actual_value, reference_value),
            status=TestResult.FAIL,
        )


class TestAccuracyScore(SimpleClassificationTest):
    name = "Test Accuracy Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.accuracy

    def _success_description(self, actual_value: float, threshold: float):
        return f"Accuracy Score is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"Accuracy Score is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"Accuracy Score is close to Accuracy on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"Accuracy Score differs from Accuracy on reference: {actual_value} <> {reference_value}"


class TestPrecisionScore(SimpleClassificationTest):
    name = "Test Precision Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.precision

    def _success_description(self, actual_value: float, threshold: float):
        return f"Precision Score is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"Precision Score is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"Precision Score is close to Precision on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"Precision Score differs from Precision on reference: {actual_value} <> {reference_value}"


class TestF1Score(SimpleClassificationTest):
    name = "Test F1 Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.f1

    def _success_description(self, actual_value: float, threshold: float):
        return f"F1 Score is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"F1 Score is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"F1 Score is close to F1 on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"F1 Score differs from F1 on reference: {actual_value} <> {reference_value}"


class TestRecallScore(SimpleClassificationTest):
    name = "Test Recall Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.recall

    def _success_description(self, actual_value: float, threshold: float):
        return f"Recall Score is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"Recall Score is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"Recall Score is close to Recall on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"Recall Score differs from Recall on reference: {actual_value} <> {reference_value}"


class TestRocAuc(SimpleClassificationTest):
    name = "Test ROC AUC Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.roc_auc

    def _success_description(self, actual_value: float, threshold: float):
        return f"RocAuc is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"RocAuc is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"RocAuc is close to RocAuc on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"RocAuc differs from RocAuc on reference: {actual_value} <> {reference_value}"


class TestLogLoss(SimpleClassificationTest):
    name = "Test Logarithmic Loss"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.log_loss

    def _success_description(self, actual_value: float, threshold: float):
        return f"LogLoss is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"LogLoss is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"LogLoss is close to LogLoss on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"LogLoss differs from LogLoss on reference: {actual_value} <> {reference_value}"


class TestTPR(SimpleClassificationTest):
    name = "Test TPR"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tp_total = sum([data["tp"] for label, data in result.confusion_by_classes.items()])
        fn_total = sum([data["fn"] for label, data in result.confusion_by_classes.items()])
        return tp_total / (tp_total + fn_total)

    def _success_description(self, actual_value: float, threshold: float):
        return f"TPR is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"TPR is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"TPR is close to TPR on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"TPR differs from TPR on reference: {actual_value} <> {reference_value}"


class TestTNR(SimpleClassificationTest):
    name = "Test TNR"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return tn_total / (tn_total + fp_total)

    def _success_description(self, actual_value: float, threshold: float):
        return f"TNR is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"TNR is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"TNR is close to TNR on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"TNR differs from TNR on reference: {actual_value} <> {reference_value}"


class TestFPR(SimpleClassificationTest):
    name = "Test FPR"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return fp_total / (tn_total + fp_total)

    def _success_description(self, actual_value: float, threshold: float):
        return f"FPR is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"FPR is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"FPR is close to FPR on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"FPR differs from FPR on reference: {actual_value} <> {reference_value}"


class TestFNR(SimpleClassificationTest):
    name = "Test FNR"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tp_total = sum([data["tp"] for label, data in result.confusion_by_classes.items()])
        fn_total = sum([data["fn"] for label, data in result.confusion_by_classes.items()])
        return fn_total / (tp_total + fn_total)

    def _success_description(self, actual_value: float, threshold: float):
        return f"FNR is {actual_value} > {threshold}"

    def _fail_description(self, actual_value: float, threshold: float):
        return f"FNR is lower than threshold: {actual_value} < {threshold}"

    def _success_description_reference(self, actual_value: float, reference_value: float):
        return f"FNR is close to FNR on reference: {actual_value} ~ {reference_value}"

    def _fail_description_reference(self, actual_value: float, reference_value: float):
        return f"FNR differs from FNR on reference: {actual_value} <> {reference_value}"
