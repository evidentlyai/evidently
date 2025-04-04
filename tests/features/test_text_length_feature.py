import pandas as pd

from evidently.legacy.features.text_length_feature import TextLength
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_text_length_feature():
    feature_generator = TextLength("column_1")
    data = pd.DataFrame(dict(column_1=["abcdefg", "abc", "a"]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=[7, 3, 1])))
