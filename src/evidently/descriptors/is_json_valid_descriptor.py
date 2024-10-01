from evidently.features import is_json_valid_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class IsJSONValid(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:IsJSONValid"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_json_valid_feature.IsJSONValid(column_name, self.display_name)
