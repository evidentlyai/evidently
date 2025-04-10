import json
from typing import List
from typing import Optional

import pandas as pd

from evidently._pydantic_compat import parse_obj_as
from evidently.core.datasets import Dataset
from evidently.core.datasets import Descriptor
from evidently.core.datasets import FeatureDescriptor
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import Options
from evidently.legacy.utils.data_preprocessing import DataDefinition


class MockGeneratedFeature(GeneratedFeatures):
    class Config:
        type_alias = "mock_generated_feature"

    column: str
    field: str

    def get_type(self, subcolumn: Optional[str] = None) -> ColumnType:
        return ColumnType.Text

    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition, options: Options) -> pd.DataFrame:
        return pd.DataFrame({self.column: data[self.column].apply(lambda x: x + self.field)})

    def list_columns(self) -> List["ColumnName"]:
        return [self._create_column(subcolumn=self.column)]


def test_deserialization():
    data = pd.DataFrame({"col": ["a", "b"]})
    d = FeatureDescriptor(feature=MockGeneratedFeature(column="col", field="c"), alias="col")

    res = d.generate_data(Dataset.from_pandas(data), Options())
    display_name = d.feature.list_columns()[0].display_name
    pd.testing.assert_series_equal(res[display_name].data, pd.DataFrame({display_name: ["ac", "bc"]})[display_name])

    payload = json.loads(d.json())
    d2 = parse_obj_as(Descriptor, payload)

    res2 = d2.generate_data(Dataset.from_pandas(data), Options())
    pd.testing.assert_series_equal(res2[display_name].data, pd.DataFrame({display_name: ["ac", "bc"]})[display_name])
