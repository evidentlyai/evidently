from typing import Optional

import numpy as np

from evidently.v2.metrics import ClassificationPerformanceMetrics
from evidently.v2.tests.base_test import Test, TestResult


class TestAccuracyScore(Test):
    name = "Test Accuracy Score"
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
            return self._compare(metrics.accuracy, self.threshold)
        if ref_metrics:
            return self._compare_with_reference(metrics.accuracy, ref_metrics.accuracy)
        return self._compare(metrics.accuracy, dummy_metrics.accuracy)

    def _compare(self, actual_value: float, threshold: float):
        if actual_value > threshold:
            return TestResult(name=self.name,
                              description=f"Accuracy Score is {actual_value} > {threshold}",
                              status=TestResult.SUCCESS)
        return TestResult(name=self.name,
                          description=f"Accuracy Score is lower than threshold: {actual_value} < {threshold}",
                          status=TestResult.FAIL)

    def _compare_with_reference(self, actual_value: float, reference_value: float):
        if np.isclose(actual_value, reference_value, atol=0.1):
            return TestResult(name=self.name,
                              description=f"Accuracy Score is close to Accuracy on reference:"
                                          f" {actual_value} ~ {reference_value}",
                              status=TestResult.SUCCESS)
        return TestResult(name=self.name,
                          description=f"Accuracy Score differs from Accuracy on reference:"
                                      f" {actual_value} <> {reference_value}",
                          status=TestResult.FAIL)
