import pandas as pd
import pytest

from evidently.legacy.features.exact_match_feature import ExactMatchFeature
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


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
    expected_df = pd.DataFrame([[expected]], columns=["column_1|column_2"])
    pd.testing.assert_frame_equal(result, expected_df)
