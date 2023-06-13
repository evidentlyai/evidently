import dataclasses

import numpy
import pytest

from evidently.base_metric import Metric
from evidently.metrics import ClassificationClassSeparationPlot
from evidently.report import Report
from tests.multitest.conftest import find_all_subclasses
from tests.multitest.datasets import TestDataset


@dataclasses.dataclass
class TestMetric:
    name: str
    metric: Metric


metric_fixtures = []


def metric(f):
    metric_fixtures.append(f())
    return f


@metric
def classification_class_separation_plot():
    return TestMetric("classification_class_separation_plot", ClassificationClassSeparationPlot())


def should_run_and_result(tmetric: TestMetric, tdataset: TestDataset):
    # todo: filter by tags or something, also
    return True, None


@pytest.mark.parametrize("raw_data", [True, False], ids=["raw_data", "agg_data"])
def test_metric(tmetric: TestMetric, tdataset: TestDataset, raw_data, tmp_path):
    should_run, exception = should_run_and_result(tmetric, tdataset)
    if not should_run:
        pytest.skip()

    report = Report(metrics=[tmetric.metric], options={"render": {"raw_data": raw_data}})

    if exception is not None:
        with pytest.raises(exception):
            report.run(reference_data=tdataset.reference, current_data=tdataset.current)
        return

    report.run(reference_data=tdataset.reference, current_data=tdataset.current)
    report._inner_suite.raise_for_error()
    assert report.show()
    assert report.json()

    path = str(tmp_path / "report.json")
    report._save(path)
    report2 = Report._load(path)
    numpy.testing.assert_equal(report2.as_dict(), report.as_dict())  # has nans
    report2.show()
    report2.save_html(str(tmp_path / "report.html"))


def test_all_metrics_tested():
    all_metric_classes = find_all_subclasses(Metric)
    missing = []
    for metric_class in all_metric_classes:
        if not any(m.metric.__class__ is metric_class for m in metric_fixtures):
            missing.append(metric_class)

    assert len(missing) == 0, f"Missing metric fixtures for {missing}"
