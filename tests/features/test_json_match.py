import pandas as pd

from evidently.legacy.features.json_match_feature import JSONMatch
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_is_valid_sql_feature():
    feature_generator = JSONMatch(
        first_column="col_1", second_column="col_2", display_name="Json Match", feature_type="num", name="is_json_match"
    )

    # Define JSON strings for each scenario
    scenarios = [
        # Scenario 1 - Matching JSONs
        ('{"name": "Alice", "age": 25, "city": "London"}', '{"city": "London", "age": 25, "name": "Alice"}'),
        # Scenario 2 - Different whitespace (still matching)
        ('{ "name" : "Bob" , "age" : 22 , "city" : "Paris" }', '{"city": "Paris", "name": "Bob", "age": 22}'),
        # Scenario 3 - Invalid JSON in one column
        (
            '{"name": "Eve", "age": 28, "city": "Berlin"}',
            '{"city": "Berlin", "age": 28, "name": Eve}',
        ),  # Missing quotes around "Eve"
        # Scenario 4 - Keys mismatch
        (
            '{"name": "Charlie", "age": 30, "country": "USA"}',
            '{"name": "Charlie", "age": 30, "city": "USA"}',
        ),  # 'country' vs 'city'
        # Scenario 5 - Values mismatch
        (
            '{"name": "David", "age": 35, "city": "Tokyo"}',
            '{"city": "Tokyo", "age": 35, "name": "Daniel"}',
        ),  # 'David' vs 'Daniel'
    ]

    # Create DataFrame
    data = pd.DataFrame(scenarios, columns=["col_1", "col_2"])

    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )

    expected_result = pd.DataFrame(dict(is_json_match=[True, True, False, False, False]))

    print(result)

    print(expected_result)

    try:
        assert result.equals(expected_result)
        return True
    except AssertionError:
        return False


print(test_is_valid_sql_feature())
