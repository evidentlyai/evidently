from typing import ClassVar
from typing import Optional

from evidently.legacy.features import text_length_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class TextLength(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:TextLength"

    def feature(self, column_name: str) -> GeneratedFeature:
        return text_length_feature.TextLength(column_name, self.display_name)
