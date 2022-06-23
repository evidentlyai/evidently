from typing import Optional

from evidently.v2.metrics import DataDriftMetrics
from evidently.v2.tests.base_test import Test, TestResult


class TestNumberOfDriftedFeatures(Test):
    data_drift_metrics: DataDriftMetrics

    def __init__(self,
                 less_than: Optional[int] = None,
                 data_drift_metrics: Optional[DataDriftMetrics] = None):
        self.data_drift_metrics = data_drift_metrics if data_drift_metrics is not None else DataDriftMetrics()
        self.less_than = less_than

    def check(self):
        less_than = self.less_than
        metrics = self.data_drift_metrics.get_result().metrics

        if less_than is None:
            less_than = metrics.n_features // 3 + 1

        if metrics.n_drifted_features < less_than:
            test_status = TestResult.SUCCESS
        else:
            test_status = TestResult.FAIL

        return TestResult("Test Number of drifted features",
                          f"Number of drifted features is {metrics.n_drifted_features} of {metrics.n_features}"
                          f" ( test threshold {less_than})",
                          test_status)
