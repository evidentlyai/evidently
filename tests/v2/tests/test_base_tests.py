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
