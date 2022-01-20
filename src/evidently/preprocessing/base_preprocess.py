import abc

import pandas as pd


class Preprocess:
    """
    Base interface for preprocesses: preprocesses allowed mutating given data, adding or removing columns or rows.
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def process(self, reference_data: pd.DataFrame, current_data: pd.DataFrame):
        """
        perform data processing, and mutate given data.
        Args:
            reference_data (pd.DataFrame): reference dataset.
            current_data (pd.DataFrame): current dataset.

        Returns:
            None
        """
        raise NotImplementedError()
