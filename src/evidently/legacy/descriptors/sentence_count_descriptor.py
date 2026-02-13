from typing import ClassVar
from typing import Optional

from evidently.legacy.features import sentence_count_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class SentenceCount(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:SentenceCount"

    def feature(self, column_name: str) -> GeneratedFeature:
        return sentence_count_feature.SentenceCount(column_name, self.display_name)
