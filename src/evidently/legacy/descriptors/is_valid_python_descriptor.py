from evidently.legacy.features import is_valid_python_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class IsValidPython(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:IsValidPython"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_python_feature.IsValidPython(column_name, self.display_name)
