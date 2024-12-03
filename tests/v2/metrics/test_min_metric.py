from evidently.v2.metrics.min import min_metric


def test_min_metric():
    metric = min_metric("")
    assert metric
