from typing import ClassVar
from typing import Optional

from evidently.legacy.features import non_letter_character_percentage_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class NonLetterCharacterPercentage(FeatureDescriptor):
    __type_alias__: ClassVar[Optional[str]] = "evidently:descriptor:NonLetterCharacterPercentage"

    def feature(self, column_name: str) -> GeneratedFeature:
        return non_letter_character_percentage_feature.NonLetterCharacterPercentage(column_name, self.display_name)
