import abc
import dataclasses
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import List
from typing import Optional

import deprecation
import pandas as pd
import uuid6

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.base_metric import DatasetType
from evidently.legacy.base_metric import TEngineDataType
from evidently.legacy.core import ColumnType
from evidently.legacy.options.base import Options
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.pydantic_utils import EvidentlyBaseModel


@dataclasses.dataclass
class FeatureResult(Generic[TEngineDataType]):
    current: TEngineDataType
    reference: Optional[TEngineDataType]


class GeneratedFeatures(EvidentlyBaseModel):
    class Config:
        is_base_type = True

    display_name: Optional[str] = None
    """
    Class for computation of additional features.
    """

    @abc.abstractmethod
    def get_type(self, subcolumn: Optional[str] = None) -> ColumnType:
        raise NotImplementedError

    @abc.abstractmethod
    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition, options: Options) -> pd.DataFrame:
        """
        generate DataFrame with new features from source data.

        Returns:
            DataFrame with new features. Columns should be unique across all features of same type.
        """
        raise NotImplementedError

    def generate_features_renamed(
        self, data: pd.DataFrame, data_definition: DataDefinition, options: Options
    ) -> pd.DataFrame:
        features = self.generate_features(data, data_definition, options)
        return features.rename(columns={col: self._create_column_name(col) for col in features.columns}).set_index(
            data.index
        )

    @abc.abstractmethod
    def list_columns(self) -> List["ColumnName"]:
        """
        get column names for given features and parameters.

        Returns:
            Special feature name for unique identification results of give feature.
        """
        raise NotImplementedError

    def as_column(self, subcolumn: Optional[str] = None) -> "ColumnName":
        columns = self.list_columns()
        if len(columns) == 1 and subcolumn is None:
            return columns[0]
        if len(columns) > 1 and subcolumn is None:
            raise ValueError(
                f"Please specify subcolumn for {self.__class__.__name__} feature, possible values: "
                + ", ".join(self._extract_subcolumn_name(c.name) for c in columns)
            )
        if len(columns) == 1 and subcolumn is not None and self._create_column_name(subcolumn) != columns[0].name:
            raise ValueError(f"{self.__class__.__name__} feature do not have subcolumns")
        try:
            fullname = self._create_column_name(subcolumn)
            return next(c for c in columns if c.name == fullname)
        except StopIteration:
            raise ValueError(
                f"Feature {self.__class__.__name__} do not have {subcolumn} subcolumn. Possible values: "
                + ", ".join(c.name for c in columns)
            )

    @deprecation.deprecated(deprecated_in="0.4.32", details="feature_name() is deprecated, please use as_column()")
    def feature_name(self, subcolumn: Optional[str] = None):
        return self.as_column(subcolumn)

    def _create_column_name(self, subcolumn: Optional[str]) -> str:
        subcolumn = f".{subcolumn}" if subcolumn is not None and len(subcolumn) > 0 else ""
        return f"{self.get_fingerprint()}{subcolumn}"

    def _extract_subcolumn_name(self, column_name: str) -> Optional[str]:
        fingerprint = self.get_fingerprint()
        if column_name == fingerprint:
            return None
        if fingerprint + "." in column_name:
            return column_name.split(fingerprint + ".")[-1]
        raise ValueError("Incorrectly formatted column name")

    def _create_column(
        self, subcolumn: str, *, display_name: Optional[str] = None, default_display_name: Optional[str] = None
    ) -> ColumnName:
        name = self._create_column_name(subcolumn)
        # todo: better display name logic
        return ColumnName(
            name=name,
            display_name=(display_name or self.display_name or default_display_name or name),
            dataset=DatasetType.ADDITIONAL,
            feature_class=self,
        )


class GeneratedFeature(GeneratedFeatures):
    __feature_type__: ClassVar[ColumnType]

    @abc.abstractmethod
    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        """
        generate DataFrame with new features from source data.

        Returns:
            DataFrame with new features. Columns should be unique across all features of same type.
        """
        raise NotImplementedError

    def generate_features(self, data: pd.DataFrame, data_definition: DataDefinition, options: Options) -> pd.DataFrame:
        feature = self.generate_feature(data, data_definition)
        assert len(feature.columns) == 1
        return feature

    def list_columns(self) -> List["ColumnName"]:
        return [self._as_column()]

    @abc.abstractmethod
    def _as_column(self) -> "ColumnName":
        raise NotImplementedError

    def get_type(self, subcolumn: Optional[str] = None):
        return self.__feature_type__


class FeatureTypeFieldMixin(BaseModel):
    feature_type: ColumnType

    def get_type(self, subcolumn: Optional[str] = None):
        return self.feature_type


class ApplyColumnGeneratedFeature(GeneratedFeature):
    display_name_template: ClassVar[str]
    column_name: str

    @abc.abstractmethod
    def apply(self, value: Any):
        raise NotImplementedError

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame({self._feature_column_name(): data[self.column_name].apply(self.apply)})

    def _as_column(self) -> ColumnName:
        return self._create_column(self._feature_column_name(), default_display_name=self._feature_display_name())

    def _feature_column_name(self):
        return self.column_name

    def _feature_display_name(self):
        return self.display_name_template.format(column_name=self.column_name)


class DataFeature(GeneratedFeature):
    display_name: str
    name: str = Field(default_factory=lambda: str(uuid6.uuid7()))

    @abc.abstractmethod
    def generate_data(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.Series:
        raise NotImplementedError()

    def generate_feature(self, data: pd.DataFrame, data_definition: DataDefinition) -> pd.DataFrame:
        return pd.DataFrame({self.name: self.generate_data(data, data_definition)})

    def _as_column(self) -> "ColumnName":
        return self._create_column(self.name)


class BaseDescriptor(EvidentlyBaseModel):
    class Config:
        type_alias = "evidently:descriptor:BaseDescriptor"
        is_base_type = True

    display_name: Optional[str] = None


class GeneralDescriptor(BaseDescriptor):
    class Config:
        is_base_type = True

    @abc.abstractmethod
    def feature(self) -> GeneratedFeatures:
        raise NotImplementedError()

    def as_column(self) -> "ColumnName":
        return self.feature().as_column()


class MultiColumnFeatureDescriptor(BaseDescriptor):
    class Config:
        type_alias = "evidently:descriptor:MultiColumnFeatureDescriptor"
        is_base_type = True

    def feature(self, columns: List[str]) -> GeneratedFeature:
        raise NotImplementedError()

    def for_columns(self, columns: List[str]) -> "ColumnName":
        return self.feature(columns).as_column()

    def on(self, columns: List[str]) -> "ColumnName":
        return self.feature(columns).as_column()


class FeatureDescriptor(BaseDescriptor):
    class Config:
        is_base_type = True

    @abc.abstractmethod
    def feature(self, column_name: str) -> GeneratedFeatures:
        raise NotImplementedError

    def for_column(self, column_name: str) -> "ColumnName":
        feature = self.feature(column_name)
        if not isinstance(feature, GeneratedFeature):
            raise NotImplementedError("Descriptors do not support multi-column features yet")
        return feature.as_column()

    def on(self, column_name: str) -> "ColumnName":
        return self.for_column(column_name)
