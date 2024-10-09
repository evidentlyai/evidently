import json

import pandas as pd

from evidently import ColumnType
from evidently.base_metric import ColumnName
from evidently.features.generated_features import FeatureTypeFieldMixin
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class JSONMatch(FeatureTypeFieldMixin, GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:JSONMatch"

    display_name: str
    # func: Callable[[pd.Series, pd.Series], pd.Series]
    name: str = "is_json_match"
    first_column: str
    second_column: str
    feature_type: ColumnType = ColumnType.Categorical

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def compare_json_objects(first_json_object: str, second_json_object: str) -> pd.Series:
            try:
                # Load both JSON strings into dictionaries
                first_json = json.loads(first_json_object)
                second_json = json.loads(second_json_object)

                # Compare dictionaries for equality, ignoring order of keys
                return first_json == second_json

            except (ValueError, TypeError):
                # Return False if either of the JSONs is invalid
                return False

        data[self.name] = data.apply(
            lambda x: compare_json_objects(x[self.first_column], x[self.second_column]), axis=1
        )
        return pd.DataFrame(data[self.name])

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)
