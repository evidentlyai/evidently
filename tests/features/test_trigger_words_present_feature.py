import nltk
import pandas as pd

from evidently.legacy.features.trigger_words_presence_feature import TriggerWordsPresent
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.utils.data_preprocessing import create_data_definition

nltk.download("words")
nltk.download("wordnet")
nltk.download("omw-1.4")


def test_trigger_words_present_feature():
    feature_generator = TriggerWordsPresent("column_1", words_list=("apple",))
    data = pd.DataFrame(dict(column_1=["Who are you and where are my apples?", "abc ", "a"]))
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1_apple_True=[1, 0, 0])))
