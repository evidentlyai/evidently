import re

import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class TriggerWordsPresent(GeneratedFeature):
    def __init__(self, column_name: str, words_list=(), lemmatisize=True):
        self.lem = WordNetLemmatizer()
        self.column_name = column_name
        self.words_list = words_list
        self.lemmatisize = lemmatisize

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def listed_words_present(s, words_list=(), lemmatisize=True):
            if s is None:
                return 0
            words = re.sub("[^A-Za-z0-9 ]+", "", s).split()
            for word_ in words:
                word = word_.lower()
                if lemmatisize:
                    word = self.lem.lemmatize(word)
                if word in words_list:
                    return 1
            return 0

        return pd.DataFrame(
            dict(
                [
                    (
                        self.column_name,
                        data[self.column_name].apply(
                            lambda x: listed_words_present(
                                x,
                                words_list=self.words_list,
                                lemmatisize=self.lemmatisize,
                            )
                        ),
                    )
                ]
            )
        )
