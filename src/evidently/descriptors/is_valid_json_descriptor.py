from typing import ClassVar

from evidently.features import is_valid_json_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class IsValidJSON(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:IsValidJSON"

    def feature(self, column_name: str) -> GeneratedFeature:
        return is_valid_json_feature.IsValidJSON(column_name, self.display_name)
