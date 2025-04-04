from typing import Any
from typing import ClassVar
from typing import Optional

import numpy as np

from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import ApplyColumnGeneratedFeature


class NonLetterCharacterPercentage(ApplyColumnGeneratedFeature):
    class Config:
        type_alias = "evidently:feature:NonLetterCharacterPercentage"

    __feature_type__: ClassVar = ColumnType.Numerical
    display_name_template: ClassVar = "Non Letter Character % for {column_name}"
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.display_name = display_name
        super().__init__(column_name=column_name)

    def apply(self, value: Any):
        """counts share of characters that are not letters or spaces"""
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0
        non_letters_num = 0
        for ch in value:
            if not ch.isalpha() and ch != " ":
                non_letters_num += 1
        return 100 * non_letters_num / len(value)
