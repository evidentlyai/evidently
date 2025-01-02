from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics.base import Metric
from evidently.future.report import Report


def simple_metric():
    class TestSimpleMetric(Metric):
        def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]):
            pass

        def display_name(self) -> str:
            pass

    return TestSimpleMetric("")


def test_report():
    report = Report([simple_metric()])
    assert report
