from typing import Any
from typing import Dict

import pandas as pd
import pytest

from evidently.legacy.features.json_schema_match_feature import JSONSchemaMatch


@pytest.mark.parametrize(
    ("column_value, expected_schema, validate_types, exact_match, expected_output"),
    [
        # Invalid JSON
        ('{"name": "Invalid json"]', {"name": str, "age": int}, False, False, False),
        # Exact Match
        ('{"name": "Jane", "age": 25}', {"name": str, "age": int}, True, True, True),
        ('{"name": "Jane", "age": 25}', {"name": str, "age": int, "city": str}, True, True, False),
        ('{"name": "Jane", "age": 25, "city": "New York"}', {"name": str, "age": int}, True, True, False),
        ('{"name": "Jane", "age": 25}', {"name": int, "age": int}, True, True, False),
        # Minimal Match without type validation
        ('{"name": "Jane", "age": 25}', {"name": str, "age": int}, False, False, True),
        ('{"name": "Jane", "age": 25, "city": "New York"}', {"name": str, "age": int}, False, False, True),
        ('{"name": "Jane", "age": null, "city": "New York"}', {"name": str, "age": int}, False, False, False),
        # Minimal Match with type validation
        ('{"name": "Jane", "age": 25}', {"name": str, "age": int}, True, False, True),
        (
            '{"name": "Jane", "age": "25"}',
            {"name": str, "age": int},
            True,
            False,
            False,
        ),  # Fail due to type mismatch (age as string)
    ],
)
def test_match_json_schema(
    column_value: str, expected_schema: Dict[str, type], validate_types: bool, exact_match: bool, expected_output: bool
):
    schema_match = JSONSchemaMatch(
        expected_schema=expected_schema,
        validate_types=validate_types,
        exact_match=exact_match,
        column_name="TestColumnName",
    )
    result = schema_match.match_json_schema(json_text=column_value)
    assert result == expected_output


@pytest.mark.parametrize(
    ("json_obj, expected_schema, validate_types, expected_output"),
    [
        # Minimal Match with type validation
        ({"name": "Jane", "age": 25}, {"name": str, "age": int}, True, True),
        ({"name": "Jane", "age": "25"}, {"name": str, "age": int}, True, False),
        ({"name": "Jane", "age": 25, "city": "New York"}, {"name": str, "age": int}, True, True),
        ({"name": "Jane", "age": 25, "city": "New York"}, {"name": str, "age": int, "region": str}, True, False),
        ({"name": "Jane", "age": None, "city": "New York"}, {"name": str, "age": int}, True, False),
        # Minimal Match without type validation
        ({"name": "Jane", "age": "25"}, {"name": str, "age": int}, False, True),
        ({"name": "Jane", "age": None, "city": "New York"}, {"name": str, "age": int}, False, False),
    ],
)
def test_minimal_match(
    json_obj: Dict[str, Any], expected_schema: Dict[str, type], validate_types: bool, expected_output: bool
):
    schema_match = JSONSchemaMatch(
        expected_schema=expected_schema, validate_types=validate_types, exact_match=False, column_name="TestColumnName"
    )
    result = schema_match._minimal_match(json_obj)
    assert result == expected_output


@pytest.mark.parametrize(
    ("json_obj, expected_schema, validate_types, expected_output"),
    [
        # Exact Match
        ({"name": "Jane", "age": 25}, {"name": str, "age": int}, True, True),
        ({"name": "Jane", "age": 25}, {"name": str, "age": int}, False, True),
        ({"name": "Jane", "age": "25"}, {"name": str, "age": int}, True, False),
        ({"name": "Jane", "age": 25, "city": "New York"}, {"name": str, "age": int}, True, False),
        ({"name": "Jane", "age": 25}, {"name": str, "age": int, "city": str}, True, False),
        (
            {"name": "Jane", "age": 25, "city": ["New York", "California"]},
            {"name": str, "age": int, "city": list},
            True,
            True,
        ),
        (
            {"name": "Jane", "age": 25, "city": ["New York", "California"]},
            {"name": str, "age": int, "city": dict},
            True,
            False,
        ),
    ],
)
def test_exact_match(
    json_obj: Dict[str, Any], expected_schema: Dict[str, type], validate_types: bool, expected_output: bool
):
    schema_match = JSONSchemaMatch(
        expected_schema=expected_schema, validate_types=validate_types, exact_match=False, column_name="TestColumnName"
    )
    result = schema_match._exact_match(json_obj)
    assert result == expected_output


test_data = pd.DataFrame(
    {
        "TestColumnName": [
            '{"name": "John", "age": 30, "city": "New York"}',
            '{"name": "Jane", "age": null, "city": "London"}',
            '{"name": "Mike", "age": 25, "city": "San Francisco"}',
            '{"name": "Invalid json"]',
            '{"name": "Anna", "age": "22", "country": "Canada"}',
        ]
    }
)


@pytest.mark.parametrize(
    ("expected_schema, validate_types, exact_match, expected_output"),
    [
        # Minimal Match without type validation
        ({"name": str, "age": int}, False, False, [True, False, True, False, True]),
        # Minimal Match with type validation
        ({"name": str, "age": int}, True, False, [True, False, True, False, False]),
        # Exact Match
        ({"name": str, "age": int, "city": str}, True, True, [True, False, True, False, False]),
    ],
)
def test_generate_feature(
    expected_schema: Dict[str, type], validate_types: bool, exact_match: bool, expected_output: list
):
    schema_match = JSONSchemaMatch(
        expected_schema=expected_schema,
        validate_types=validate_types,
        exact_match=exact_match,
        column_name="TestColumnName",
    )
    result = schema_match.generate_feature(test_data, None)
    assert result[schema_match._feature_column_name()].tolist() == expected_output


def test_generate_feature_column_name_dne():
    schema_match = JSONSchemaMatch(
        expected_schema={"test": str}, validate_types=False, exact_match=False, column_name="DNEColumn"
    )
    with pytest.raises(KeyError):
        schema_match.generate_feature(test_data, None)
