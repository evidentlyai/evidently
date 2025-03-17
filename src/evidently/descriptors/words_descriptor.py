from typing import ClassVar
from typing import List

from evidently.features import words_feature
from evidently.features.generated_features import FeatureDescriptor
from evidently.features.generated_features import GeneratedFeature


class ExcludesWords(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:ExcludesWords"

    words_list: List[str]
    mode: str = "all"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.ExcludesWords(
            column_name,
            self.words_list,
            self.mode,
            self.lemmatize,
            self.display_name,
        )


class IncludesWords(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:IncludesWords"

    words_list: List[str]
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.IncludesWords(
            column_name,
            self.words_list,
            self.mode,
            self.lemmatize,
            self.display_name,
        )


class WordMatch(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:WordMatch"

    with_column: str
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.WordMatch(
            columns=[column_name, self.with_column],
            mode=self.mode,
            lemmatize=self.lemmatize,
            display_name=self.display_name,
        )


class WordNoMatch(FeatureDescriptor):
    __type_alias__: ClassVar = "evidently:descriptor:WordNoMatch"

    with_column: str
    mode: str = "any"
    lemmatize: bool = True

    def feature(self, column_name: str) -> GeneratedFeature:
        return words_feature.WordNoMatch(
            columns=[column_name, self.with_column],
            mode=self.mode,
            lemmatize=self.lemmatize,
            display_name=self.display_name,
        )
