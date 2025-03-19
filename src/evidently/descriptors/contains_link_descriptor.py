from typing import ClassVar

from evidently.features import contains_link_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class ContainsLink(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:ContainsLink"

    def feature(self, column_name: str) -> GeneratedFeature:
        return contains_link_feature.ContainsLink(column_name, self.display_name)
