from evidently.metrics import OutRangeValueCount


def test_out_range_metric():
    metric = OutRangeValueCount(column="a", left=0.5, right=1)
    assert metric.left == 0.5
    assert metric.right == 1
