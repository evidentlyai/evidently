import pytest

from evidently.v2.tests.utils import approx


@pytest.mark.parametrize(
    "value, test_value, expected_result",
    (
        (approx(1, relative=0.5), 1.3, True),
        (approx(1, relative=0.5), 0.5, True),
        (approx(1, relative=0.5), 1.51, False),
        (approx(1, relative=0.5), 0.49, False),
        (approx(10, absolute=0.5), 10.4, True),
        (approx(10, absolute=0.5), 10.5, True),
        (approx(10, absolute=0.5), 9.5, True),
        (approx(10, absolute=0.5), 10.51, False),
        (approx(10, absolute=0.5), 9.49, False),
    ),
)
def test_approx_equals(value, test_value, expected_result):
    assert (value == test_value) is expected_result


@pytest.mark.parametrize(
    "value, condition_value, expected_result",
    (
        (approx(1, relative=0.5), 1.51, True),
        (approx(1, relative=0.5), 1.5, False),
        (approx(1, absolute=0.2), 1.21, True),
        (approx(1, absolute=0.2), 1.2, False),
        (approx(10, relative=0.1, absolute=0.2), 12.1, True),
    ),
)
def test_approx_lt(value, condition_value, expected_result):
    assert (value < condition_value) is expected_result, value


@pytest.mark.parametrize(
    "value, condition_value, expected_result",
    (
        (approx(1, relative=0.5), 1.51, True),
        (approx(1, relative=0.5), 1.5, True),
        (approx(1, relative=0.5), 1.49, False),
        (approx(1, absolute=0.2), 1.21, True),
        (approx(1, absolute=0.2), 1.2, True),
        (approx(1, absolute=0.2), 1.19, False),
    ),
)
def test_approx_lte(value, condition_value, expected_result):
    assert (value <= condition_value) is expected_result


@pytest.mark.parametrize(
    "value, condition_value, expected_result",
    (
        (approx(1, relative=0.5), 0.49, True),
        (approx(1, relative=0.5), 0.5, False),
        (approx(1, relative=0.5), 0.51, False),
        (approx(1, absolute=0.2), 0.79, True),
        (approx(1, absolute=0.2), 0.8, False),
        (approx(1, absolute=0.2), 0.81, False),
    ),
)
def test_approx_gt(value, condition_value, expected_result):
    assert (value > condition_value) is expected_result


@pytest.mark.parametrize(
    "value, condition_value, expected_result",
    (
        (approx(1, relative=0.5), 0.49, True),
        (approx(1, relative=0.5), 0.5, True),
        (approx(1, relative=0.5), 0.51, False),
        (approx(1, absolute=0.2), 0.79, True),
        (approx(1, absolute=0.2), 0.8, True),
        (approx(1, absolute=0.2), 0.81, False),
    ),
)
def test_approx_gte(value, condition_value, expected_result):
    assert (value >= condition_value) is expected_result
