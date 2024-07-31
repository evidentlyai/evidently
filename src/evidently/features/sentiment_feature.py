from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from evidently._pydantic_compat import PrivateAttr
from evidently.features.generated_features import ApplyColumnGeneratedFeature


class Sentiment(ApplyColumnGeneratedFeature):
    display_name_template: ClassVar = "Sentiment for {column_name}"
    column_name: str

    _sid: Optional[SentimentIntensityAnalyzer] = PrivateAttr(None)

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name
        super().__init__()

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
