import pandas as pd

from evidently.base_metric import ColumnName
from evidently.base_metric import additional_feature
from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class NonLetterCharacterPercentage(GeneratedFeature):
    def __init__(self, column_name: str):
        self.column_name = column_name

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:

        # counts share of characters that are not letters or spaces
        def non_letter_share(s):
            if s is None:
                return 0
            non_letters_num = 0
            for ch in s:
                if not ch.isalpha() and ch != " ":
                    non_letters_num += 1
            return 100 * non_letters_num / len(s)

        return pd.DataFrame(dict([(self.column_name, data[self.column_name].apply(non_letter_share))]))

    def feature_name(self) -> ColumnName:
        return additional_feature(self, self.column_name)
