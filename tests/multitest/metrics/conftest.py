import pytest

from tests.multitest.datasets import dataset_fixtures
from tests.multitest.metrics.test_all import metric_fixtures


def pytest_generate_tests(metafunc):
    if "tmetric" in metafunc.fixturenames:
        metafunc.parametrize("tmetric", [pytest.param(m, id=m.name) for m in metric_fixtures])
    if "tdataset" in metafunc.fixturenames:
        metafunc.parametrize("tdataset", [pytest.param(d, id=d.name) for d in dataset_fixtures])
