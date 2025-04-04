from typing import Dict

from evidently.legacy.features import json_schema_match_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class JSONSchemaMatch(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:JSONSchemaMatch"

    expected_schema: Dict[str, type]
    validate_types: bool = False
    exact_match: bool = False

    def feature(self, column_name: str) -> GeneratedFeature:
        return json_schema_match_feature.JSONSchemaMatch(
            column_name=column_name,
            expected_schema=self.expected_schema,
            validate_types=self.validate_types,
            exact_match=self.exact_match,
            display_name=self.display_name,
        )
