import pandas as pd
import pytest

from evidently.features.is_valid_json_feature import IsValidJSON
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        ('{"test": "abc"}', True),
        ("not json", False),
    ],
)
def test_is_valid_json_feature(item: str, expected: bool):
    feature_generator = IsValidJSON("column_1")
    data = pd.DataFrame(dict(column_1=[item]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=[expected])))
