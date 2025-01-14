import abc
import copy
import dataclasses
from abc import abstractmethod
from dataclasses import field
from enum import Enum
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently import ColumnType
from evidently.features.generated_features import GeneratedFeatures
from evidently.metric_results import Label
from evidently.options.base import Options
from evidently.utils.data_preprocessing import create_data_definition
from evidently.utils.types import Numeric


class ColumnRole(Enum):
    Unset = "Unset"
    Target = "target"
    Output = "output"
    Feature = "feature"
    Descriptor = "descriptor"
    UserId = "user_id"
    ItemId = "item_id"
    Input = "input"
    Context = "context"
    Example = "example"


@dataclasses.dataclass
class ColumnInfo:
    type: ColumnType
    role: ColumnRole = ColumnRole.Unset


@dataclasses.dataclass
class BinaryClassification:
    name: str = "default"
    target: str = "target"
    prediction_labels: Optional[str] = None
    prediction_probas: Optional[str] = "prediction"
    pos_label: Label = 1
    labels: Optional[Dict[Label, str]] = None


@dataclasses.dataclass
class MulticlassClassification:
    name: str = "default"
    target: str = "target"
    prediction_labels: str = "prediction"
    prediction_probas: Optional[List[str]] = None
    labels: Optional[Dict[Label, str]] = None


Classification = Union[BinaryClassification, MulticlassClassification]


@dataclasses.dataclass
class Regression:
    target: str = "target"
    prediction: str = "prediction"


@dataclasses.dataclass
class Completion:
    pass


@dataclasses.dataclass
class RAG:
    pass


LLMDefinition = Union[Completion, RAG]


@dataclasses.dataclass
class DataDefinition:
    id_column: Optional[str] = None
    timestamp: Optional[str] = None
    numerical_columns: Optional[List[str]] = None
    categorical_columns: Optional[List[str]] = None
    text_columns: Optional[List[str]] = None
    datetime_columns: Optional[List[str]] = None
    classification: Optional[List[Classification]] = None
    regression: Optional[List[Regression]] = None
    llm: Optional[LLMDefinition] = None
    numerical_descriptors: List[str] = field(default_factory=list)
    categorical_descriptors: List[str] = field(default_factory=list)

    def get_numerical_columns(self):
        return (self.numerical_columns or []) + (self.numerical_descriptors or [])

    def get_categorical_columns(self):
        return (self.categorical_columns or []) + (self.categorical_descriptors or [])

    def get_text_columns(self):
        return self.text_columns or []

    def get_datetime_columns(self):
        return self.datetime_columns or []

    def get_column_type(self, column_name: str) -> ColumnType:
        if column_name in self.get_numerical_columns():
            return ColumnType.Numerical
        if column_name in self.get_categorical_columns():
            return ColumnType.Categorical
        if column_name in self.get_text_columns():
            return ColumnType.Text
        if column_name in self.get_datetime_columns():
            return ColumnType.Datetime
        return ColumnType.Unknown

    def get_classification(self, classification_id: str) -> Optional[Classification]:
        item_list = list(filter(lambda x: x.name == classification_id, self.classification or []))
        if len(item_list) == 0:
            return None
        if len(item_list) > 1:
            raise ValueError("More than one classification with id {}".format(classification_id))
        return item_list[0]

    def get_columns(self, types: List[ColumnType]) -> Generator[str, None, None]:
        if ColumnType.Numerical in types:
            yield from self.get_numerical_columns()
        if ColumnType.Categorical in types:
            yield from self.get_categorical_columns()
        if ColumnType.Text in types:
            yield from self.get_text_columns()


class DatasetColumn:
    type: ColumnType
    data: pd.Series

    def __init__(self, type: ColumnType, data: pd.Series) -> None:
        self.type = type
        self.data = data


class Descriptor:
    def __init__(self, alias: str):
        self._alias = alias

    @abc.abstractmethod
    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        raise NotImplementedError()

    @property
    def alias(self) -> str:
        return self._alias


class FeatureDescriptor(Descriptor):
    def __init__(self, feature: GeneratedFeatures, alias: Optional[str] = None):
        feature_columns = feature.list_columns()
        super().__init__(alias or f"{feature_columns[0].display_name}")
        self._feature = feature

    def get_dataset_column(self, column_name: str, values: pd.Series) -> DatasetColumn:
        column_type = self._feature.get_type(f"{self._feature.get_fingerprint()}.{column_name}")
        if column_type == ColumnType.Numerical:
            values = pd.to_numeric(values, errors="coerce")
        dataset_column = DatasetColumn(type=column_type, data=values)
        return dataset_column

    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        feature = self._feature.generate_features(
            dataset.as_dataframe(),
            create_data_definition(None, dataset.as_dataframe(), ColumnMapping()),
            Options(),
        )
        if len(feature.columns) > 1:
            return {col: self.get_dataset_column(col, feature[col]) for col in feature.columns}
        col = feature.columns[0]
        return self.get_dataset_column(col, feature[col])


def _determine_desccriptor_column_name(alias: str, columns: List[str]):
    index = 1
    key = alias
    while key in columns:
        key = f"{alias}_{index}"
        index += 1
    return key


@dataclasses.dataclass
class CountValue:
    count: int
    share: float


@dataclasses.dataclass
class GeneralColumnStats:
    missing_values: CountValue


@dataclasses.dataclass
class NumericalColumnStats:
    max: Numeric
    min: Numeric
    mean: Numeric
    std: Numeric
    quantiles: Dict[str, Numeric]
    infinite: CountValue


@dataclasses.dataclass
class LabelStats:
    count: CountValue


@dataclasses.dataclass
class CategoricalColumnStats:
    unique_count: int
    label_stats: Dict[Label, LabelStats]

    @property
    def most_common(self) -> Optional[Tuple[Label, LabelStats]]:
        most_common = None
        for key, value in self.label_stats.items():
            if most_common is None:
                most_common = key
                continue
            if self.label_stats[most_common].count < value.count:
                most_common = key
        if most_common is None:
            return None
        return most_common, self.label_stats[most_common]


@dataclasses.dataclass
class ColumnStats:
    general_stats: GeneralColumnStats
    numerical_stats: Optional[NumericalColumnStats]
    categorical_stats: Optional[CategoricalColumnStats]


@dataclasses.dataclass
class DatasetStats:
    row_count: int
    column_count: int
    column_stats: Dict[str, ColumnStats]


class Dataset:
    _data_definition: DataDefinition

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        descriptors: Optional[List[Descriptor]] = None,
    ) -> "Dataset":
        dataset = PandasDataset(data, data_definition)
        if descriptors is not None:
            dataset.add_descriptors(descriptors)
        return dataset

    @abstractmethod
    def as_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def column(self, column_name: str) -> DatasetColumn:
        raise NotImplementedError()

    @abstractmethod
    def subdataset(self, column_name: str, label: object) -> "Dataset":
        raise NotImplementedError()

    @abstractmethod
    def stats(self) -> DatasetStats:
        raise NotImplementedError()

    @property
    def data_definition(self) -> DataDefinition:
        return self._data_definition


class PandasDataset(Dataset):
    _data: pd.DataFrame
    _data_definition: DataDefinition
    _dataset_stats: DatasetStats

    def __init__(
        self,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
    ):
        self._data = data
        if data_definition is None:
            self._data_definition = self._generate_data_definition(data)
        else:
            self._data_definition = copy.deepcopy(data_definition)
        (rows, columns) = data.shape

        column_stats = {}
        for column in data.columns:
            column_stats[column] = self._collect_stats(self._data_definition.get_column_type(column), data[column])
        self._dataset_stats = DatasetStats(rows, columns, column_stats)

    def as_dataframe(self) -> pd.DataFrame:
        return self._data

    def column(self, column_name: str) -> DatasetColumn:
        return DatasetColumn(self._data_definition.get_column_type(column_name), self._data[column_name])

    def subdataset(self, column_name: str, label: object):
        return PandasDataset(self._data[self._data[column_name] == label], self._data_definition)

    def _generate_data_definition(self, data: pd.DataFrame) -> DataDefinition:
        raise NotImplementedError()

    def stats(self) -> DatasetStats:
        return self._dataset_stats

    def add_column(self, key: str, data: DatasetColumn):
        self._dataset_stats.column_count += 1
        self._dataset_stats.column_stats[key] = self._collect_stats(data.type, data.data)
        self._data[key] = data.data
        if data.type == ColumnType.Numerical:
            self._data_definition.numerical_descriptors.append(key)
        if data.type == ColumnType.Categorical:
            self._data_definition.categorical_descriptors.append(key)

    def add_descriptor(self, descriptor: Descriptor):
        key = _determine_desccriptor_column_name(descriptor.alias, self._data.columns.tolist())
        new_column = descriptor.generate_data(self)
        if isinstance(new_column, DatasetColumn):
            self.add_column(key, new_column)
        elif len(new_column) > 1:
            for col, value in new_column.items():
                self.add_column(f"{key}.{col}", value)
        else:
            self.add_column(key, list(new_column.values())[0])

    def add_descriptors(self, descriptors: List[Descriptor]):
        for descriptor in descriptors:
            self.add_descriptor(descriptor)

    def _collect_stats(self, column_type: ColumnType, data: pd.Series):
        numerical_stats = None
        if column_type == ColumnType.Numerical:
            numerical_stats = _collect_numerical_stats(data)

        categorical_stats = None
        if column_type == ColumnType.Categorical:
            categorical_stats = _collect_categorical_stats(data)

        return ColumnStats(
            general_stats=GeneralColumnStats(missing_values=CountValue(0, 0)),
            numerical_stats=numerical_stats,
            categorical_stats=categorical_stats,
        )


def _collect_numerical_stats(data: pd.Series):
    infinite_count = data.groupby(np.isinf(data)).count().get(True, 0)
    return NumericalColumnStats(
        max=data.max(),
        min=data.min(),
        mean=data.mean(),
        std=data.std(),
        quantiles={
            "p25": data.quantile(0.25),
            "p75": data.quantile(0.75),
        },
        infinite=CountValue(infinite_count, infinite_count / data.count()),
    )


def _collect_categorical_stats(data: pd.Series):
    total_count = data.count()
    return CategoricalColumnStats(
        unique_count=data.nunique(),
        label_stats={
            label: LabelStats(count=CountValue(count, count / total_count))
            for label, count in data.value_counts().items()
        },
    )
