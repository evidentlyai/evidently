from typing import Optional

from evidently.pydantic_utils import autoregister
from evidently.v2.datasets import Dataset
from evidently.v2.metrics.base import Metric
from evidently.v2.report import Report


def simple_metric():
    @autoregister
    class TestSimpleMetric(Metric):
        class Config:
            type_alias = "evidently:metric_v2:TestSimpleMetric"

        def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]):
            pass

        def display_name(self) -> str:
            pass

    return TestSimpleMetric("")


def test_report():
    report = Report([simple_metric()])
    assert report
