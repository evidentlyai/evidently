import pytest

from evidently.v2.tests.base_test import TestValueCondition


@pytest.mark.parametrize(
    "condition_args, value, expected_result",
    (
        ({"gte": 10}, 5, False),
        ({"gte": 10}, 12, True),
        ({"gte": 10}, 10, True),
        ({"gt": 10}, 5, False),
        ({"gt": 10}, 12, True),
        ({"gt": 10}, 10, False),
        ({"eq": 10}, 8, False),
        ({"eq": 8}, 8, True),
        ({"not_eq": 10}, 8, True),
        ({"not_eq": 8}, 8, False),
        ({"lte": 10}, 5, True),
        ({"lte": 5}, 5, True),
        ({"lte": 5}, 6, False),
        ({"lt": 10}, 5, True),
        ({"lt": 5}, 5, False),
        ({"lt": 5}, 6, False),
        ({"is_in": [10, 20, 30]}, 5, False),
        ({"is_in": [10, 20, 30]}, 20, True),
        ({"not_in": [10, 20, 30]}, 5, True),
        ({"not_in": [10, 20, 30]}, 10, False),
    ),
)
def test_value_condition_class(condition_args, value, expected_result):
    conditions = TestValueCondition(**condition_args)
    assert conditions.check_value(value) == expected_result


@pytest.mark.parametrize("condition_args,expected", [
    ({}, False),
    ({"gte": 10}, True),
    ({"gt": 10}, True),
    ({"eq": 8}, True),
    ({"not_eq": 10}, True),
    ({"lte": 10}, True),
    ({"lt": 10}, True),
    ({"is_in": [10, 20, 30]}, True),
    ({"not_in": [10, 20, 30]}, True),
])
def test_value_condition_set(condition_args, expected):
    condition = TestValueCondition(**condition_args)
    assert condition.is_set() == expected


@pytest.mark.parametrize("condition_args,expected", [
    ({}, ""),
    ({"gte": 10}, "gte=10"),
    ({"gte": 10.5}, "gte=10.500"),
    ({"gt": 10}, "gt=10"),
    ({"gt": 10, "lt": 40}, "gt=10 and lt=40"),
    ({"eq": 8}, "eq=8"),
    ({"not_eq": 10}, "not_eq=10"),
    ({"lte": 10}, "lte=10"),
    ({"lt": 10}, "lt=10"),
    ({"is_in": [10, 20, 30]}, "is_in=[10, 20, 30]"),
    ({"not_in": [10, 20, 30]}, "not_in=[10, 20, 30]"),
])
def test_value_condition_str(condition_args, expected):
    condition = TestValueCondition(**condition_args)
    assert str(condition) == expected
