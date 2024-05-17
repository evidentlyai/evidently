import abc
import logging
import typing
import uuid
from typing import List
from typing import Optional

import pandas as pd
from pydantic import Field

from evidently.core import ColumnType
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition

if typing.TYPE_CHECKING:
    from evidently.base_metric import ColumnName


class GeneratedFeature(EvidentlyBaseModel):
    display_name: Optional[str] = None
    feature_type: ColumnType = ColumnType.Numerical
    feature_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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
    def feature_name(self) -> "ColumnName":
        """
        get feature name for given features and parameters.

        Returns:
            Special feature name for unique identification results of give feature.
        """
        raise NotImplementedError()

    def get_parameters(self) -> Optional[tuple]:
        attributes = []
        for field, value in sorted(self.__dict__.items(), key=lambda x: x[0]):
            if field in ("display_name", "feature_id"):
                continue
            if isinstance(value, list):
                attributes.append(tuple(value))
            elif isinstance(value, dict):
                attributes.append(tuple([(k, value[k]) for k in sorted(value.keys())]))
            else:
                attributes.append(value)
        params = tuple(attributes)
        try:
            hash(params)
        except TypeError:
            logging.warning(f"unhashable params for {type(self)}. Fallback to unique.")
            return None
        return params


class GeneralDescriptor(EvidentlyBaseModel):
    display_name: Optional[str] = None

    @abc.abstractmethod
    def feature(self) -> GeneratedFeature:
        raise NotImplementedError()

    def as_column(self):
        return self.feature().feature_name()


class MultiColumnFeatureDescriptor(EvidentlyBaseModel):
    display_name: Optional[str] = None

    def feature(self, columns: List[str]) -> GeneratedFeature:
        raise NotImplementedError()

    def for_columns(self, columns: List[str]) -> "ColumnName":
        return self.feature(columns).feature_name()

    def on(self, columns: List[str]) -> "ColumnName":
        return self.feature(columns).feature_name()


class FeatureDescriptor(EvidentlyBaseModel):
    display_name: Optional[str] = None

    def for_column(self, column_name: str):
        return self.feature(column_name).feature_name()

    def on(self, column_name: str):
        return self.feature(column_name).feature_name()

    @abc.abstractmethod
    def feature(self, column_name: str) -> GeneratedFeature:
        raise NotImplementedError()
