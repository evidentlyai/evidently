from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from evidently._pydantic_compat import PrivateAttr
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature


class Sentiment(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:Sentiment"

    __feature_type__: ClassVar = ColumnType.Numerical
    display_name_template: ClassVar = "Sentiment for {column_name}"
    column_name: str

    _sid: Optional[SentimentIntensityAnalyzer] = PrivateAttr(None)

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.display_name = display_name
        super().__init__(column_name=column_name)

    @property
    def sid(self):
        if self._sid is None:
            import nltk

            nltk.download("vader_lexicon", quiet=True)
            self._sid = SentimentIntensityAnalyzer()
        return self._sid

    def apply(self, value: Any):
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        return self.sid.polarity_scores(value)["compound"]
