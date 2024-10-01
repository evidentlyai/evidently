import pandas as pd

from evidently.features.is_json_valid_feature import IsJSONValid
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.utils.data_preprocessing import create_data_definition


def test_is_valid_json_feature():
    feature_generator = IsJSONValid("column_1")
    data = pd.DataFrame(dict(column_1=["{'test': 'abc'}", "abc"]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=[True, False])))
