import re
from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.core import ColumnType
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class TriggerWordsPresent(GeneratedFeature):
    column_name: str
    words_list: List[str]
    lemmatize: bool = True
    _lem: WordNetLemmatizer

    def __init__(
        self,
        column_name: str,
        words_list: List[str],
        lemmatize: bool = True,
        display_name: Optional[str] = None,
    ):
        self.feature_type = ColumnType.Categorical
        self.column_name = column_name
        self.words_list = words_list
        self.lemmatize = lemmatize
        self.display_name = (
            display_name
            if display_name is not None
            else f"TriggerWordsPresent [words: {words_list}, lemmatize: {lemmatize}] for {column_name}"
        )
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if not hasattr(self, "_lem"):
            import nltk

            nltk.download("wordnet", quiet=True)
            self._lem = WordNetLemmatizer()

        def listed_words_present(s, words_list=(), lemmatize=True):
            if s is None or (isinstance(s, float) and np.isnan(s)):
                return 0
            words = re.sub("[^A-Za-z0-9 ]+", "", s).split()
            for word_ in words:
                word = word_.lower()
                if lemmatize:
                    word = self._lem.lemmatize(word)
                if word in words_list:
                    return 1
            return 0

        return data[self.column_name].apply(
            lambda x: listed_words_present(x, words_list=self.words_list, lemmatize=self.lemmatize),
        )

    def get_parameters(self):
        return self.column_name, tuple(self.words_list), self.lemmatize
