import re
from typing import Optional

import pandas as pd
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class OOVWordsPercentage(GeneratedFeature):
    def __init__(self, column_name: str, ignore_words=()):
        self.lem = WordNetLemmatizer()
        self.eng_words = set(words.words())
        self.column_name = column_name
        self.ignore_words = ignore_words

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def oov_share(s, ignore_words=()):
            if s is None:
                return 0
            oov_num = 0
            words_ = re.sub("[^A-Za-z0-9 ]+", "", s).split()  # leave only letters, digits and spaces, split by spaces
            for word in words_:
                if word.lower() not in ignore_words and self.lem.lemmatize(word.lower()) not in self.eng_words:
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

    def feature_name(self):
        return additional_feature(self, self.column_name, f"OOV Words % for {self.column_name}")

    def get_parameters(self) -> Optional[tuple]:
        return self.column_name, self.ignore_words
