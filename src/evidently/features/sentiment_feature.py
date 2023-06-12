import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class Sentiment(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str):
        self.column_name = column_name
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        sid = SentimentIntensityAnalyzer()

        def sentiment_f(s, sid=sid):
            if s is None:
                return 0
            return sid.polarity_scores(s)["compound"]

        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(sentiment_f))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name, f"Sentiment for {self.column_name}")


def sentiment(column_name: str) -> ColumnName:
    return additional_feature(Sentiment(column_name), f"{column_name}", f"Sentiment for {column_name}")
