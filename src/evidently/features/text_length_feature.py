from typing import Optional

import numpy as np
import pandas as pd

from evidently.features.generated_features import GeneratedFeature
from evidently.utils.data_preprocessing import DataDefinition


class TextLength(GeneratedFeature):
    column_name: str

    def __init__(self, column_name: str, display_name: Optional[str] = None):
        self.column_name = column_name
        self.display_name = display_name or f"Text Length for {column_name}"
        super().__init__()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        def text_len(s):
            if s is None or (isinstance(s, float) and np.isnan(s)):
                return 0
            return len(s)

        return data[self.column_name].apply(text_len)
