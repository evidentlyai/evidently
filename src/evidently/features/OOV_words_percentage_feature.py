import re

import nltk
import pandas as pd
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.features.generated_features import GeneratedFeature
from evidently.metrics.base_metric import ColumnName
from evidently.metrics.base_metric import additional_feature
from evidently.utils.data_preprocessing import DataDefinition

nltk.download("words")
nltk.download("wordnet")
nltk.download("omw-1.4")

lem = WordNetLemmatizer()
eng_words = set(words.words())


class OOVWordsPercentage(GeneratedFeature):
    def __init__(self, column_name: str, ignore_words=()):
        self.column_name = column_name
        self.ignore_words = ignore_words

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def oov_share(s, ignore_words=()):
            oov_num = 0
            words_ = re.sub("[^A-Za-z0-9 ]+", "", s).split()  # leave only letters, digits and spaces, split by spaces
            for word in words_:
                if word.lower() not in ignore_words and lem.lemmatize(word.lower()) not in eng_words:
                    oov_num += 1
            return 100 * oov_num / len(words_)

        return pd.DataFrame(
            dict(
                [
                    (
                        self.column_name,
                        data[self.column_name].apply(lambda x: oov_share(x, ignore_words=self.ignore_words)),
                    )
                ]
            )
        )

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)
