import pandas as pd
import pytest

from evidently.legacy.features.BERTScore_feature import BERTScoreFeature
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

test_data = [
    ("The quick brown fox jumps over the lazy dog", "A fast brown fox leaps over a lazy dog"),
    ("Hello world", "Hi universe"),
    ("Machine learning is fascinating", "Artificial intelligence is intriguing"),
    ("I love apples", "I adore oranges"),
    ("Python is a great programming language", "Python is an excellent coding language"),
]


@pytest.mark.parametrize(
    (
        "column_1",
        "column_2",
        "expected",
    ),  # expected values obtained from the BERTScore library https://github.com/Tiiiger/bert_score
    [
        ("The quick brown fox jumps over the lazy dog", "A fast brown fox leaps over a lazy dog", 0.8917),
        ("Hello world", "Hi universe", 0.7707),
        ("Machine learning is fascinating", "Artificial intelligence is intriguing", 0.8238),
        ("I love apples", "I adore oranges", 0.7017),
        ("Python is a great programming language", "Python is an excellent coding language", 0.8689),
    ],
)
def test_bert_score_feature(column_1: str, column_2: str, expected: float):
    feature_generator = BERTScoreFeature(columns=["column_1", "column_2"], tfidf_weighted=False)
    data = pd.DataFrame(dict(column_1=[column_1], column_2=[column_2]))

    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    column_expected = feature_generator._feature_name()
    assert result[column_expected].iloc[0] == pytest.approx(expected, rel=0.1)
