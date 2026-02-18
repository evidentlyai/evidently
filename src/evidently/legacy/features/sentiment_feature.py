from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature


class Sentiment(ApplyColumnGeneratedFeature):
    __type_alias__: ClassVar[Optional[str]] = "evidently:feature:Sentiment"

    __feature_type__: ClassVar = ColumnType.Numerical
    display_name_template: ClassVar = "Sentiment for {column_name}"
    column_name: str

    __sid__: Optional[SentimentIntensityAnalyzer] = None

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.display_name = display_name
        super().__init__(column_name=column_name)

    @property
    def sid(self):
        if self.__sid__ is None:
            import nltk

            nltk.download("vader_lexicon", quiet=True)
            self.__sid__ = SentimentIntensityAnalyzer()
        return self.__sid__

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        return self.sid.polarity_scores(value)["compound"]
