from typing import Tuple

from evidently.features import trigger_words_presence_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class TriggerWordsPresence(FeatureDescriptor):
    words_list: Tuple
    lemmatisize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return trigger_words_presence_feature.TriggerWordsPresent(column_name, self.words_list, self.lemmatisize)

    def for_column(self, column_name: str):
        return trigger_words_presence_feature.TriggerWordsPresent(
            column_name,
            self.words_list,
            self.lemmatisize,
        ).feature_name()
