import pandas as pd

from evidently.legacy.features.custom_feature import CustomSingleColumnFeature
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition


def test_custom_feature():
    def add_two(data: pd.Series) -> pd.Series:
        return data + 2

    feature_generator = CustomSingleColumnFeature(column_name="column_1", display_name="cl", func=add_two, name="cf")
    data = pd.DataFrame(dict(column_1=[1, 2, 3]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )

    pd.testing.assert_frame_equal(result, pd.DataFrame(dict(cf=[3, 4, 5])))
    assert feature_generator.as_column().display_name == "cl"
