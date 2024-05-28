import re
from typing import Optional

import numpy as np
import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class WordCount(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name or f"Word Count for {column_name}"
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        def word_count_f(s):
            if s is None or (isinstance(s, float) and np.isnan(s)):
                return 0
            return len(re.sub(r"[^a-zA-Z ]+", "", s).split())

        return data[self.column_name].apply(word_count_f)
