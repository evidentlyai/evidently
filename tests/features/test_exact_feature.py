import pandas as pd
import pytest

from evidently.features.exact_match_feature import ExactMatchFeature
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        ("this is same", "this is same", True),
        ("this is same", "this is different", False),
    ],
)
def test_exact_match_feature(value1: str, value2: str, expected: bool):
    feature_generator = ExactMatchFeature(columns=["column_1", "column_2"])
    data = pd.DataFrame(dict(column_1=[value1], column_2=[value2]))
    result = feature_generator.generate_feature(
        data=data, data_definition=create_data_definition(None, data, ColumnMapping())
    )
    result_value = bool(result.iloc[0])
    assert result_value == expected
