import dataclasses
from importlib import import_module
from typing import Callable
from typing import List
from typing import Optional

from _pytest.python import Metafunc

from evidently.base_metric import Metric
from evidently.report import Report
from tests.multitest.datasets import DatasetTags
from tests.multitest.datasets import TestDataset
from tests.multitest.datasets import dataset_fixtures


@dataclasses.dataclass
class TestMetric:
    name: str
    metric: Metric

    include_tags: List[DatasetTags] = dataclasses.field(default_factory=list)
    """Only run on datasets with all tags"""
    exclude_tags: List[DatasetTags] = dataclasses.field(default_factory=list)
    """Exclude datasets with any of theese tags"""

    dataset_names: Optional[List[str]] = None
    """Only run on datasets with any theese names"""
    datasets: Optional[List[TestDataset]] = None
    """Only run on those datasets"""

    additional_check: Optional[Callable[[Report], None]] = None
    """Additional callable to call on report"""


metric_fixtures = []


def metric(f):
    metric_fixtures.append(f())
    return f


def generate_dataset_outcome(m: TestMetric):
    if m.datasets is not None:
        yield from ((m, d, None) for d in m.datasets)
        return
    if m.dataset_names is not None:
        yield from ((m, d, None) for d in dataset_fixtures if d.name in m.dataset_names)
        return

    for d in dataset_fixtures:
        is_included = m.include_tags == [] or all(t in d.tags for t in m.include_tags)
        is_excluded = any(t in m.exclude_tags for t in d.tags)
        if is_included and not is_excluded:
            yield m, d, None


def load_test_metrics():
    for module in ["classification", "data_integrity", "data_drift", "data_quality", "regression"]:
        import_module(f"tests.multitest.metrics.{module}")


def generate_metric_dataset_outcome():
    load_test_metrics()
    for m in metric_fixtures:
        yield from generate_dataset_outcome(m)


def pytest_generate_tests(metafunc: Metafunc):
    if metafunc.definition.name != "test_metric":
        return
    parameters = [([m, d, o], f"{m.name}_{d.name}_{o}") for m, d, o in generate_metric_dataset_outcome()]
    metafunc.parametrize("tmetric,tdataset,outcome", [p[0] for p in parameters], ids=[p[1] for p in parameters])
