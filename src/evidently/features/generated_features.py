import abc

import pandas as pd

from evidently.utils.data_preprocessing import DataDefinition


class GeneratedFeature:
    """
    Class for computation of additional features.
    """
    @abc.abstractmethod
    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        """
        generate DataFrame with new features from source data.

        Returns:
            DataFrame with new features. Columns should be unique across all features of same type.
        """
        raise NotImplementedError()
