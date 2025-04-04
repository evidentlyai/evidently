import pandas as pd

from evidently.legacy.features.is_valid_sql_feature import IsValidSQL
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_is_valid_sql_feature():
    feature_generator = IsValidSQL("column_1")
    data = pd.DataFrame(
        dict(
            column_1=[
                "SELECT * FROM users",  # Valid SQL (simple query)
                "SELECT id, address FROM users; SELECT count(id) FROM users",  # Valid SQL (multiple SQL queries)
                "INSERT INTO table",  # Invalid SQL (incomplete query)
                "SLECT * FROM users",  # Invalid SQL (typo)
                "SLECT * FROM users; SELECT id, address FROM users",  # Invalid SQL (1 invalid sub-query)
            ]
        )
    )

    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )

    expected_result = pd.DataFrame(dict(column_1=[True, True, False, False, False]))

    assert result.equals(expected_result)
