import pandas as pd

from evidently import ColumnMapping
from evidently.features.trigger_words_present_feature import TriggerWordsPresent
from evidently.utils.data_preprocessing import create_data_definition


def test_trigger_words_present_feature():
    feature_generator = TriggerWordsPresent("column_1", words_list=("apple",))
    data = pd.DataFrame(
        dict(column_1=["Who are you and where are my apples?", "abc ", "a"])
    )
    result = feature_generator.generate_feature(
        data=data,
        data_definition=create_data_definition(None, data, ColumnMapping()),
    )
    assert result.equals(pd.DataFrame(dict(column_1=[1, 0, 0])))
