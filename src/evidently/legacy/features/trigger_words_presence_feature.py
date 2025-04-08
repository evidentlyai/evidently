import re
from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional

import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature


class TriggerWordsPresent(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:TriggerWordsPresent"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    words_list: List[str]
    lemmatize: bool = True
    _lem: Optional[WordNetLemmatizer] = PrivateAttr(None)

    def __init__(
        self,
        column_name: str,
        words_list: List[str],
        lemmatize: bool = True,
        display_name: Optional[str] = None,
    ):
        self.words_list = words_list
        self.lemmatize = lemmatize
        self.display_name = display_name
        super().__init__(column_name=column_name)

    @property
    def lem(self):
        if self._lem is None:
            import nltk

            nltk.download("wordnet", quiet=True)
            self._lem = WordNetLemmatizer()
        return self._lem

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        words = re.sub("[^A-Za-z0-9 ]+", "", value).split()
        for word_ in words:
            word = word_.lower()
            if self.lemmatize:
                word = self.lem.lemmatize(word)
            if word in self.words_list:
                return 1
        return 0

    def _feature_column_name(self):
        return self.column_name + "_" + "_".join(self.words_list) + "_" + str(self.lemmatize)

    def _feature_display_name(self):
        return f"TriggerWordsPresent [words: {self.words_list}, lemmatize: {self.lemmatize}] for {self.column_name}"
