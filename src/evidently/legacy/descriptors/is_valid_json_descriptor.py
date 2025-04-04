from evidently.legacy.features import is_valid_json_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class IsValidJSON(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:IsValidJSON"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_json_feature.IsValidJSON(column_name, self.display_name)
