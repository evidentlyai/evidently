import pytest

from evidently.v2.metrics.base_metric import Metric


def test_base_metrics_class() -> None:
    with pytest.raises(TypeError):
        Metric()
