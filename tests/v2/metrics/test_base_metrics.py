import pytest

from evidently.v2.metrics.base_metric import NumberRange
from evidently.v2.metrics.base_metric import Metric


def test_base_metrics_class() -> None:
    with pytest.raises(TypeError):
        Metric()


@pytest.mark.parametrize("range_args,expected_range", [
    pytest.param(dict(exact=10), (10, 10), id="exact"),
    pytest.param(dict(left_side_threshold=10), (10, None), id="left_side_threshold"),
    pytest.param(dict(right_side_threshold=10), (None, 10), id="right_side_threshold"),
    pytest.param(dict(left_side_threshold=10, right_side_threshold=20), (10, 20), id="left_right_side_thresholds"),
    pytest.param(dict(is_in=(None, 10)), (None, 10), id="is_in(right)"),
    pytest.param(dict(is_in=(10, None)), (10, None), id="is_in(left)"),
    pytest.param(dict(is_in=(10, 20)), (10, 20), id="is_in(both)"),
])
def test_number_range(range_args, expected_range):
    num_range = NumberRange(**range_args)
    assert num_range.get_range() == expected_range


@pytest.mark.parametrize("range_args", [
    pytest.param(dict(exact=10, left_side_threshold=10), id="exact+l"),
    pytest.param(dict(exact=10, right_side_threshold=20), id="exact+r"),
    pytest.param(dict(exact=10, is_in=(10, 20)), id="exact+is_in"),
    pytest.param(dict(exact=10, left_side_threshold=10, right_side_threshold=20), id="exact+lr"),
    pytest.param(dict(exact=10, left_side_threshold=10, is_in=(10, 20)), id="exact+l+is_in"),
    pytest.param(dict(exact=10, right_side_threshold=20, is_in=(10, 20)), id="exact+r+is_in"),
    pytest.param(dict(exact=10, left_side_threshold=10, right_side_threshold=20, is_in=(10, 20)), id="all_args"),
    pytest.param(dict(left_side_threshold=10, is_in=(10, 20)), id="l+is_in"),
    pytest.param(dict(right_side_threshold=20, is_in=(10, 20)), id="r+is_in"),
    pytest.param(dict(left_side_threshold=10, right_side_threshold=20, is_in=(10, 20)), id="lr+is_in"),
    pytest.param(dict(is_in=(10,)), id="is_in(1 element)"),
    pytest.param(dict(is_in=()), id="is_in(0 elements)"),
    pytest.param(dict(is_in=(10, 20, 30)), id="is_in(3 elements)"),
])
def test_invalid_usage(range_args):
    with pytest.raises(ValueError):
        NumberRange(**range_args).get_range()
