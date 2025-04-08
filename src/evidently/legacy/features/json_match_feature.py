import json

import pandas as pd

from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import FeatureTypeFieldMixin
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class JSONMatch(FeatureTypeFieldMixin, GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:JSONMatch"

    first_column: str
    second_column: str
    feature_type: ColumnType = ColumnType.Categorical

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def compare_json_objects(first_json_object: str, second_json_object: str) -> bool:
            try:
                # Load both JSON strings into dictionaries
                first_json = json.loads(first_json_object)
                second_json = json.loads(second_json_object)

                # Compare dictionaries for equality, ignoring order of keys
                return first_json == second_json

            except (ValueError, TypeError):
                # Return False if either of the JSONs is invalid
                return False

        data[self._feature_column_name()] = data.apply(
            lambda x: compare_json_objects(x[self.first_column], x[self.second_column]), axis=1
        )
        return pd.DataFrame(data[self._feature_column_name()])

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_column_name(),
            default_display_name=f"JSON match for columns {self.first_column} and {self.second_column}",
        )

    def _feature_column_name(self):
        return f"JSON match for {self.first_column} and {self.second_column}"
