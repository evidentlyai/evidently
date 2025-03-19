from typing import ClassVar

from evidently.features import text_part_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class BeginsWith(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:BeginsWith"

    prefix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.BeginsWith(
            column_name,
            self.prefix,
            self.case_sensitive,
            self.display_name,
        )


class EndsWith(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:EndsWith"

    suffix: str
    case_sensitive: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_part_feature.EndsWith(
            column_name,
            self.suffix,
            self.case_sensitive,
            self.display_name,
        )
