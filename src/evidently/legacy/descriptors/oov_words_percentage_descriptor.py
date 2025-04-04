from typing import Tuple

from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.features.OOV_words_percentage_feature import OOVWordsPercentage


class OOV(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:OOV"

    ignore_words: Tuple = ()

    def feature(self, column_name: str) -> GeneratedFeature:
        return OOVWordsPercentage(column_name, self.ignore_words, self.display_name)
