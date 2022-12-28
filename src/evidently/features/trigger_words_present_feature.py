import re

import nltk
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition
from evidently.metrics.base_metric import ColumnName
from evidently.metrics.base_metric import additional_feature

nltk.download("words")
nltk.download("wordnet")
nltk.download("omw-1.4")

lem = WordNetLemmatizer()


class TriggerWordsPresent(GeneratedFeature):
    def __init__(self, column_name: str, words_list=(), lemmatisize=True):
        self.column_name = column_name
        self.words_list = words_list
        self.lemmatisize = lemmatisize

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def listed_words_present(s, words_list=(), lemmatisize=True):
            words = re.sub("[^A-Za-z0-9 ]+", "", s).split()
            for word_ in words:
                word = word_.lower()
                if lemmatisize:
                    word = lem.lemmatize(word)
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

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)
