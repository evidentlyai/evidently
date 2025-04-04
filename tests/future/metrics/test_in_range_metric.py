from evidently.metrics import InRangeValueCount


def test_in_range_metric():
    metric = InRangeValueCount(column="a", left=0.5, right=1)
    assert metric.left == 0.5
    assert metric.right == 1
