from typing import List

from evidently.legacy.features import trigger_words_presence_feature
from evidently.legacy.features.generated_features import FeatureDescriptor
from evidently.legacy.features.generated_features import GeneratedFeature


class TriggerWordsPresence(FeatureDescriptor):
    class Config:
        type_alias = "evidently:descriptor:TriggerWordsPresence"

    words_list: List[str]
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return trigger_words_presence_feature.TriggerWordsPresent(
            column_name,
            self.words_list,
            self.lemmatize,
            self.display_name,
        )
