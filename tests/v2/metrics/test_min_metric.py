from evidently.v2.metrics import column_min


def test_min_metric():
    metric = column_min("")
    assert metric
