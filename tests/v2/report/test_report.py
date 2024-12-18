from evidently.v2.metrics.base import Metric
from evidently.v2.report import Report


def simple_metric():
    class SimpleMetric(Metric):
        pass

    return SimpleMetric()


def test_report():
    report = Report([simple_metric()])
    assert report
