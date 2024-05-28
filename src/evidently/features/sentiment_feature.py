from typing import Optional

import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class Sentiment(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name or f"Sentiment for {column_name}"
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        import nltk

        nltk.download("vader_lexicon", quiet=True)
        sid = SentimentIntensityAnalyzer()

        def sentiment_f(s, sid=sid):
            if s is None or (isinstance(s, float) and np.isnan(s)):
                return 0
            return sid.polarity_scores(s)["compound"]

        return data[self.column_name].apply(sentiment_f)
