from typing import ClassVar
from typing import Optional

from evidently.legacy.features import contains_link_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class ContainsLink(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:ContainsLink"

    def feature(self, column_name: str) -> GeneratedFeature:
        return contains_link_feature.ContainsLink(column_name, self.display_name)
