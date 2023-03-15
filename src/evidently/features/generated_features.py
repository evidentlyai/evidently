import abc
import logging
from typing import Optional

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

    @abc.abstractmethod
    def feature_name(self):
        """
        get feature name for given features and parameters.

        Returns:
            Special feature name for unique identification results of give feature.
        """
        raise NotImplementedError()

    def get_parameters(self) -> Optional[tuple]:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if isinstance(value, list):
                attributes.append(tuple(value))
            elif isinstance(value, dict):
                attributes.append(tuple([(k, value[k]) for k in sorted(value.items())]))
            else:
                attributes.append(value)
        params = tuple(attributes)
        try:
            hash(params)
        except TypeError:
            logging.warning(f"unhashable params for {type(self)}. Fallback to unique.")
            return None
        return params


class FeatureDescriptor:
    @abc.abstractmethod
    def for_column(self, column_name: str):
        raise NotImplementedError()

    @abc.abstractmethod
    def feature(self, column_name: str) -> GeneratedFeature:
        raise NotImplementedError()
