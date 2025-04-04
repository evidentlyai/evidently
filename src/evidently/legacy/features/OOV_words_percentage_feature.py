import re
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Set
from typing import Tuple

import numpy as np
import pandas as pd
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer

from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


class OOVWordsPercentage(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:OOVWordsPercentage"

    __feature_type__: ClassVar = ColumnType.Numerical
    display_name_template: ClassVar = "OOV Words % for {column_name}"
    ignore_words: Tuple = ()
    _lem: WordNetLemmatizer
    _eng_words: Set

    def __init__(self, column_name: str, ignore_words=(), display_name: Optional[str] = None):
        self.ignore_words = ignore_words
        self.display_name = display_name
        super().__init__(column_name=column_name)

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        oov_num = 0
        words_ = re.sub("[^A-Za-z0-9 ]+", "", value).split()  # leave only letters, digits and spaces, split by spaces
        if len(words_) == 0:
            return 0
        for word in words_:
            if word.lower() not in self.ignore_words and self._lem.lemmatize(word.lower()) not in self._eng_words:
                oov_num += 1
        return 100 * oov_num / len(words_)

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        if not hasattr(self, "_lem"):
            import nltk

            nltk.download("wordnet", quiet=True)
            nltk.download("words", quiet=True)
            self._lem = WordNetLemmatizer()
            self._eng_words = set(words.words())

        return super().generate_feature(data, data_definition)
