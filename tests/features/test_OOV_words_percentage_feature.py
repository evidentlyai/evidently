import nltk
import pandas as pd

from evidently.legacy.features.OOV_words_percentage_feature import OOVWordsPercentage
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

nltk.download("words")
nltk.download("wordnet")
nltk.download("omw-1.4")


def test_oov_words_percentage():
    feature_generator = OOVWordsPercentage("column_1", ignore_words=("foobar",))
    data = pd.DataFrame(dict(column_1=["Who ate apples? Go iaehb!", "Who ate apples? Go foobar! ", "the"]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=[20.0, 0, 0])))
