from typing import Tuple

from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature
from evidently.features.OOV_words_percentage_feature import OOVWordsPercentage


class OOV(FeatureDescriptor):
    ignore_words: Tuple = ()

    def feature(self, column_name: str) -> GeneratedFeature:
        return OOVWordsPercentage(column_name, self.ignore_words)

    def for_column(self, column_name: str):
        return OOVWordsPercentage(column_name, self.ignore_words).feature_name()
