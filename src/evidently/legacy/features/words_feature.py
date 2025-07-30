import re
from typing import Any
from typing import ClassVar
from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature
from evidently.legacy.features.generated_features import GeneratedFeature
from evidently.legacy.utils.data_preprocessing import DataDefinition


def _listed_words_present(
    in_str: str,
    mode: str,
    lem: WordNetLemmatizer,
    words_list: List[str],
    lemmatize: bool,
) -> int:
    wl = set(words_list)
    result = False
    if in_str is None or (isinstance(in_str, float) and np.isnan(in_str)):
        return False
    words = re.sub("[^A-Za-z0-9 ]+", "", in_str).split()
    for word_ in words:
        word = word_.lower()
        if lemmatize:
            word = lem.lemmatize(word)
        if word in wl:
            if mode in ("includes_all", "excludes_any"):
                wl.remove(word)
            else:
                result = True
    if mode in ("includes_all", "excludes_any"):
        result = len(wl) == 0
    if mode.startswith("excludes"):
        return not result
    return result


class WordsPresence(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:WordsPresence"

    __feature_type__: ClassVar = ColumnType.Categorical
    column_name: str
    words_list: List[str]
    mode: str
    lemmatize: bool = True
    _lem: Optional[WordNetLemmatizer] = PrivateAttr(None)

    def __init__(
        self,
        column_name: str,
        words_list: List[str],
        mode: str = "includes_any",
        lemmatize: bool = True,
        display_name: Optional[str] = None,
    ):
        self.words_list = words_list
        if mode not in ["includes_any", "includes_all", "excludes_any", "excludes_all"]:
            raise ValueError("mode must be either 'includes_any', 'includes_all', 'excludes_any' or 'excludes_all'")
        self.mode = mode
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
        return _listed_words_present(value, self.mode, self.lem, self.words_list, self.lemmatize)


class IncludesWords(WordsPresence):
    class Config:
        type_alias = "evidently:feature:IncludesWords"

    def __init__(
        self,
        column_name: str,
        words_list: List[str],
        mode: str = "any",
        lemmatize: bool = True,
        display_name: Optional[str] = None,
    ):
        if mode.startswith("includes_"):
            mode = mode[len("includes_") :]
        super().__init__(column_name, words_list, "includes_" + mode, lemmatize, display_name)

    def _feature_column_name(self):
        return self.column_name + "_" + "_".join(self.words_list) + "_" + str(self.lemmatize) + "_" + str(self.mode)

    def _feature_display_name(self):
        return (
            f"Text Includes {self.mode} words [{self.words_list}],"
            f" lemmatize: {self.lemmatize}] for {self.column_name}"
        )


class ExcludesWords(WordsPresence):
    class Config:
        type_alias = "evidently:feature:ExcludesWords"

    def __init__(
        self,
        column_name: str,
        words_list: List[str],
        mode: str = "any",
        lemmatize: bool = True,
        display_name: Optional[str] = None,
    ):
        if mode.startswith("excludes_"):
            mode = mode[len("excludes_") :]
        super().__init__(column_name, words_list, "excludes_" + mode, lemmatize, display_name)

    def _feature_column_name(self):
        return self.column_name + "_" + "_".join(self.words_list) + "_" + str(self.lemmatize) + "_" + str(self.mode)

    def _feature_display_name(self):
        return (
            f"Text Excludes {self.mode} words [{self.words_list}],"
            f" lemmatize: {self.lemmatize}] for {self.column_name}"
        )


class RowWordPresence(GeneratedFeature):
    class Config:
        type_alias = "evidently:feature:RowWordPresence"

    __feature_type__: ClassVar = ColumnType.Categorical
    columns: List[str]
    mode: str = "any"
    lemmatize: bool = True
    _lem: Optional[WordNetLemmatizer] = PrivateAttr(None)

    def __init__(self, columns: List[str], mode: str, lemmatize: bool, display_name: Optional[str] = None):
        self.columns = columns
        self.mode = mode
        self.lemmatize = lemmatize
        self.display_name = display_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        generated_col = data[self.columns[0]].fillna("")
        expected_col = data[self.columns[1]].fillna("")

        return pd.DataFrame(
            {
                self._feature_name(): pd.Series(
                    [
                        _listed_words_present(
                            in_str=generated_str,
                            mode=self.mode,
                            lemmatize=self.lemmatize,
                            words_list=expected_words,
                            lem=self.lem,
                        )
                        for generated_str, expected_words in zip(generated_col, expected_col)
                    ],
                    index=data.index,
                )
            }
        )

    @property
    def lem(self):
        if self._lem is None:
            import nltk

            nltk.download("wordnet", quiet=True)
            self._lem = WordNetLemmatizer()
        return self._lem

    def _feature_name(self):
        return "_".join(["RowWordPresence", self.columns[0], self.columns[1], str(self.lemmatize), str(self.mode)])


class WordMatch(RowWordPresence):
    class Config:
        type_alias = "evidently:feature:WordMatch"

    def __init__(self, columns: List[str], mode: str, lemmatize: bool, display_name: Optional[str] = None):
        super().__init__(columns=columns, mode="includes_" + mode, lemmatize=lemmatize, display_name=display_name)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"Text contains {self.mode.split('_')[1]} defined words",
        )


class WordNoMatch(RowWordPresence):
    class Config:
        type_alias = "evidently:feature:WordNoMatch"

    def __init__(self, columns: List[str], mode: str, lemmatize: bool, display_name: Optional[str] = None):
        super().__init__(columns=columns, mode="excludes_" + mode, lemmatize=lemmatize, display_name=display_name)

    def _as_column(self) -> "ColumnName":
        return self._create_column(
            self._feature_name(),
            default_display_name=f"Text does not contain {self.mode.split('_')[1]} defined words",
        )
