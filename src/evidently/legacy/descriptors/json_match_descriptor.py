from evidently.legacy.features import json_match_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class JSONMatch(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:JSONMatch"

    with_column: str

    def feature(self, column_name: str) -> GeneratedFeature:
        return json_match_feature.JSONMatch(first_column=column_name, second_column=self.with_column)
