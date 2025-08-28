import abc
import copy
import dataclasses
import io
import json
import os
import tarfile
from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.core.base_types import Label
from evidently.core.tests import GenericTest
from evidently.legacy.base_metric import DisplayName
from evidently.legacy.core import ColumnType
from evidently.legacy.features.generated_features import GeneratedFeatures
from evidently.legacy.options.base import AnyOptions
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import ColumnMapping
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.legacy.utils.types import Numeric
from evidently.pydantic_utils import AutoAliasMixin
from evidently.pydantic_utils import EvidentlyBaseModel

EVIDENTLY_DATASET_EXT = "evidently_dataset"

if TYPE_CHECKING:
    from evidently.core.container import MetricOrContainer


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
    name: str
    target: str
    prediction_labels: Optional[str]
    prediction_probas: Optional[str]
    pos_label: Label
    labels: Optional[Dict[Label, str]]

    def __init__(
        self,
        *,
        name: str = "default",
        target: Optional[str] = None,
        prediction_labels: Optional[str] = None,
        prediction_probas: Optional[str] = None,
        pos_label: Optional[str] = None,
        labels: Optional[Dict[Label, str]] = None,
    ):
        self.name = name
        if (
            target is None
            and prediction_labels is None
            and prediction_probas is None
            and pos_label is None
            and labels is None
        ):
            self.target = "target"
            self.prediction_labels = None
            self.prediction_probas = "prediction"
            self.pos_label = 1
            self.labels = None
            return
        if target is None or (prediction_labels is None and prediction_probas is None):
            raise ValueError(
                "Invalid BinaryClassification configuration:" " target and one of (labels or probas) should be set"
            )
        self.target = target
        self.prediction_labels = prediction_labels
        self.prediction_probas = prediction_probas
        self.pos_label = pos_label if pos_label is not None else 1
        self.labels = labels


@dataclasses.dataclass
class MulticlassClassification:
    name: str = "default"
    target: str = "target"
    prediction_labels: Optional[str] = "prediction"
    prediction_probas: Optional[List[str]] = None
    labels: Optional[Dict[Label, str]] = None

    def __init__(
        self,
        *,
        name: str = "default",
        target: Optional[str] = None,
        prediction_labels: Optional[str] = None,
        prediction_probas: Optional[List[str]] = None,
        labels: Optional[Dict[Label, str]] = None,
    ):
        self.name = name
        if target is None and prediction_labels is None and prediction_probas is None and labels is None:
            self.target = "target"
            self.prediction_labels = "prediction"
            self.prediction_probas = None
            self.labels = None
            return
        if target is None or (prediction_labels is None and prediction_probas is None):
            raise ValueError(
                "Invalid MulticlassClassification configuration:" " target and one of (labels or probas) should be set"
            )
        self.target = target
        self.prediction_labels = prediction_labels
        self.prediction_probas = prediction_probas
        self.labels = labels


Classification = Union[BinaryClassification, MulticlassClassification]


@dataclasses.dataclass
class Regression:
    name: str = "default"
    target: str = "target"
    prediction: str = "prediction"


@dataclasses.dataclass
class Recsys:
    name: str = "default"
    user_id: str = "user_id"
    item_id: str = "item_id"
    target: str = "target"
    prediction: str = "prediction"
    recommendations_type: str = "score"


@dataclasses.dataclass
class Completion:
    pass


@dataclasses.dataclass
class RAG:
    pass


@dataclasses.dataclass
class LLMClassification:
    input: str
    target: str
    predictions: Optional[str] = None
    reasoning: Optional[str] = None
    prediction_reasoning: Optional[str] = None
    name: str = "llm_default"


class SpecialColumnInfo(AutoAliasMixin, EvidentlyBaseModel):
    __alias_type__: ClassVar = "special_column_info"

    class Config:
        is_base_type = True

    def get_metrics(self) -> List["MetricOrContainer"]:
        return []

    def get_column_type(self, column_name: str) -> Optional[ColumnType]:
        return None


LLMDefinition = Union[Completion, RAG, LLMClassification]


DEFAULT_TRACE_LINK_COLUMN = "_evidently_trace_link"


class ServiceColumns(BaseModel):
    trace_link: Optional[str] = None


class DataDefinition(BaseModel):
    id_column: Optional[str] = None
    timestamp: Optional[str] = None
    service_columns: Optional[ServiceColumns] = None
    numerical_columns: Optional[List[str]] = None
    categorical_columns: Optional[List[str]] = None
    text_columns: Optional[List[str]] = None
    datetime_columns: Optional[List[str]] = None
    classification: Optional[List[Classification]] = None
    regression: Optional[List[Regression]] = None
    llm: Optional[LLMDefinition] = None
    numerical_descriptors: List[str] = []
    categorical_descriptors: List[str] = []
    test_descriptors: Optional[List[str]] = None
    ranking: Optional[List[Recsys]] = None
    special_columns: List[SpecialColumnInfo] = []

    def __init__(
        self,
        id_column: Optional[str] = None,
        timestamp: Optional[str] = None,
        numerical_columns: Optional[List[str]] = None,
        categorical_columns: Optional[List[str]] = None,
        text_columns: Optional[List[str]] = None,
        datetime_columns: Optional[List[str]] = None,
        classification: Optional[List[Classification]] = None,
        regression: Optional[List[Regression]] = None,
        llm: Optional[LLMDefinition] = None,
        numerical_descriptors: Optional[List[str]] = None,
        categorical_descriptors: Optional[List[str]] = None,
        test_descriptors: Optional[List[str]] = None,
        ranking: Optional[List[Recsys]] = None,
        service_columns: Optional[ServiceColumns] = None,
    ):
        super().__init__()
        self.id_column = id_column
        self.timestamp = timestamp
        self.numerical_columns = numerical_columns
        self.categorical_columns = categorical_columns
        self.text_columns = text_columns
        self.datetime_columns = datetime_columns
        self.classification = classification
        self.regression = regression
        self.llm = llm
        self.numerical_descriptors = numerical_descriptors if numerical_descriptors is not None else []
        self.categorical_descriptors = categorical_descriptors if categorical_descriptors is not None else []
        self.test_descriptors = test_descriptors
        self.ranking = ranking
        self.service_columns = service_columns

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
        if column_name == self.timestamp:
            return ColumnType.Date
        if column_name == self.id_column:
            return ColumnType.Id
        for special_column in self.special_columns:
            ct = special_column.get_column_type(column_name)
            if ct is not None:
                return ct
        return ColumnType.Unknown

    def get_classification(self, classification_id: str) -> Optional[Classification]:
        item_list = list(filter(lambda x: x.name == classification_id, self.classification or []))
        if len(item_list) == 0:
            return None
        if len(item_list) > 1:
            raise ValueError("More than one classification with id {}".format(classification_id))
        return item_list[0]

    def get_ranking(self, ranking_id: str) -> Optional[Recsys]:
        item_list = list(filter(lambda x: x.name == ranking_id, self.ranking or []))
        if len(item_list) == 0:
            return None
        if len(item_list) > 1:
            raise ValueError("More than one ranking with id {}".format(ranking_id))
        return item_list[0]

    def get_columns(self, types: List[ColumnType]) -> Generator[str, None, None]:
        if ColumnType.Numerical in types:
            yield from self.get_numerical_columns()
        if ColumnType.Categorical in types:
            yield from self.get_categorical_columns()
        if ColumnType.Text in types:
            yield from self.get_text_columns()
        if ColumnType.Datetime in types:
            yield from self.get_datetime_columns()

    def get_regression(self, regression_id: str) -> Optional[Regression]:
        item_list = list(filter(lambda x: x.name == regression_id, self.regression or []))
        if len(item_list) == 0:
            return None
        if len(item_list) > 1:
            raise ValueError("More than one regression with id {}".format(regression_id))
        return item_list[0]


class DatasetColumn:
    type: ColumnType
    data: pd.Series

    def __init__(self, type: Union[str, ColumnType], data: pd.Series) -> None:
        self.type = ColumnType(type)
        self.data = data


class ColumnCondition(AutoAliasMixin, EvidentlyBaseModel, abc.ABC):
    __alias_type__: ClassVar[str] = "column_condition"

    class Config:
        is_base_type = True

    @abstractmethod
    def check(self, value: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_default_alias(self, column: str) -> str:
        raise NotImplementedError


class DescriptorTest(BaseModel):
    condition: ColumnCondition
    column: Optional[str] = None
    alias: Optional[str] = None

    def __init__(
        self,
        condition: Union[ColumnCondition, GenericTest],
        column: Optional[str] = None,
        alias: Optional[str] = None,
        **data: Any,
    ) -> None:
        c: ColumnCondition = condition.for_descriptor().condition if isinstance(condition, GenericTest) else condition
        super().__init__(alias=alias, column=column, condition=c, **data)

    def to_descriptor(self, descriptor: Optional["Descriptor"] = None) -> "Descriptor":
        if self.column is None:
            if descriptor is None:
                raise ValueError("Parent descriptor is required for test without column")
            descriptor_columns = descriptor.list_output_columns()
            if len(descriptor_columns) == 1:
                column = descriptor_columns[0]
            else:
                raise ValueError(
                    f"Column is required for test with multiple columns in parent descriptor: [{', '.join(descriptor_columns)}]"
                )
        else:
            column = self.column
        return ColumnTest(column, self.condition, self.alias or self.condition.get_default_alias(column))


AnyDescriptorTest = Union["DescriptorTest", "GenericTest"]


class Descriptor(AutoAliasMixin, EvidentlyBaseModel, abc.ABC):
    class Config:
        is_base_type = True

    __alias_type__: ClassVar = "descriptor_v2"

    alias: str
    tests: List[DescriptorTest] = []

    def __init__(self, alias: str, tests: Optional[List[AnyDescriptorTest]] = None, **data: Any) -> None:
        self.alias = alias
        self.tests = [t.for_descriptor() if isinstance(t, GenericTest) else t for t in (tests or [])]
        super().__init__(**data)

    @abc.abstractmethod
    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        raise NotImplementedError()

    def validate_input(self, data_definition: DataDefinition) -> None:
        input_columns = self.list_input_columns()
        if input_columns is not None:
            all_columns = set(data_definition.get_columns(list(ColumnType)))
            for column in input_columns:
                if column not in all_columns:
                    raise ValueError(
                        f"Column {column} is not found in dataset. Available columns: [{', '.join(all_columns)}]"
                    )

    def list_output_columns(self) -> List[str]:  # todo: also types?
        return [self.alias]

    def list_input_columns(self) -> Optional[List[str]]:  # todo: make not optional
        return None

    def get_sub_descriptors(self) -> List["Descriptor"]:
        return [t.to_descriptor(self) for t in self.tests]

    def get_special_columns_info(self, rename: Dict[str, str]) -> List[SpecialColumnInfo]:
        return []

    def add_to_descriptors_list(self) -> bool:
        return True


class SingleInputDescriptor(Descriptor, abc.ABC):
    column: str

    def list_input_columns(self) -> List[str]:
        return [self.column]


class ColumnTest(SingleInputDescriptor):
    column: str
    condition: ColumnCondition

    def __init__(
        self, column: str, condition: Union[ColumnCondition, GenericTest], alias: Optional[str] = None, **data: Any
    ) -> None:
        self.column = column
        if isinstance(condition, dict):
            condition = parse_obj_as(ColumnCondition, condition)  # type: ignore[type-abstract]
        descriptor_condition: ColumnCondition = (
            condition if isinstance(condition, ColumnCondition) else condition.for_descriptor().condition
        )
        self.condition = descriptor_condition
        super().__init__(alias=alias or descriptor_condition.get_default_alias(column), **data)

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        data = dataset.column(self.column)
        res = data.data.apply(self.condition.check)
        return DatasetColumn(ColumnType.Categorical, res)


class TestSummaryInfo(SpecialColumnInfo):
    all_column: Optional[str] = None
    any_column: Optional[str] = None
    count_column: Optional[str] = None
    rate_column: Optional[str] = None
    score_column: Optional[str] = None
    score_weights: Optional[Dict[str, float]] = None

    @property
    def has_all(self):
        return self.any_column is not None

    @property
    def has_any(self):
        return self.any_column is not None

    @property
    def has_count(self):
        return self.count_column is not None

    @property
    def has_rate(self):
        return self.rate_column is not None

    @property
    def has_score(self):
        return self.score_column is not None

    def get_metrics(self) -> List["MetricOrContainer"]:
        from evidently.presets.special import TestSummaryInfoPreset

        return [TestSummaryInfoPreset(column_info=self)]

    def get_column_type(self, column_name: str) -> Optional[ColumnType]:
        if column_name in (self.all_column, self.any_column):
            return ColumnType.Categorical
        if column_name in (self.count_column, self.rate_column, self.score_column):
            return ColumnType.Numerical
        return None


class TestSummary(Descriptor):
    success_all: bool = True
    success_any: bool = False
    success_count: bool = False
    success_rate: bool = False
    score: bool = False
    score_weights: Optional[Dict[str, float]] = None
    normalize_scores: bool = True

    def __init__(
        self,
        success_all: bool = True,
        success_any: bool = False,
        success_count: bool = False,
        success_rate: bool = False,
        score: bool = False,
        score_weights: Optional[Dict[str, float]] = None,
        alias: Optional[str] = None,
        normalize_scores: bool = True,
        **data: Any,
    ):
        self.success_all = success_all
        self.success_any = success_any
        self.success_count = success_count
        self.success_rate = success_rate
        self.score = score
        self.score_weights = score_weights
        self.normalize_scores = normalize_scores
        super().__init__(alias=alias or "summary", **data)

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        tests = dataset.data_definition.test_descriptors or []
        if len(tests) == 0:
            raise ValueError("No tests specified")
        summary_columns = {}
        test_results = dataset.as_dataframe()[tests]
        if self.success_count:
            summary_columns["success_count"] = (ColumnType.Numerical, test_results.sum(axis=1))
        if self.success_rate:
            summary_columns["success_rate"] = (ColumnType.Numerical, test_results.sum(axis=1) / len(tests))
        if self.success_all:
            summary_columns["success_all"] = (ColumnType.Categorical, test_results.all(axis=1))
        if self.success_any:
            summary_columns["success_any"] = (ColumnType.Categorical, test_results.any(axis=1))
        if self.score:
            weights = self.score_weights or {t: 1 for t in tests}
            total_weight = sum(weights.values()) if self.normalize_scores else 1
            summary_columns["score"] = (  # type: ignore[assignment]
                ColumnType.Numerical,
                sum(test_results[col] * weight / total_weight for col, weight in weights.items()),
            )
        alias = self.alias or "summary"
        result = {f"{alias}_{key}": DatasetColumn(ct, value) for key, (ct, value) in summary_columns.items()}
        if len(tests) == 0:
            raise ValueError("No summary columns specified")
        if len(result) == 1:
            return {alias: list(result.values())[0]}
        return result

    def list_input_columns(self) -> Optional[List[str]]:
        if self.score and self.score_weights is not None:
            return list(self.score_weights.keys())
        return None

    def get_special_columns_info(self, rename: Dict[str, str]) -> List[SpecialColumnInfo]:
        alias = self.alias or "summary"
        if len(rename) == 1:
            return [
                TestSummaryInfo(
                    all_column=rename[alias] if self.success_all else None,
                    any_column=rename[alias] if self.success_any else None,
                    count_column=rename[alias] if self.success_count else None,
                    rate_column=rename[alias] if self.success_rate else None,
                    score_column=rename[alias] if self.score else None,
                )
            ]

        return [
            TestSummaryInfo(
                all_column=rename[f"{alias}_success_all"] if self.success_all else None,
                any_column=rename[f"{alias}_success_any"] if self.success_any else None,
                count_column=rename[f"{alias}_success_count"] if self.success_count else None,
                rate_column=rename[f"{alias}_success_rate"] if self.success_rate else None,
                score_column=rename[f"{alias}_score"] if self.score else None,
                score_weights=self.score_weights,
            )
        ]

    def add_to_descriptors_list(self) -> bool:
        return False


class FeatureDescriptor(Descriptor):
    feature: GeneratedFeatures

    def __init__(
        self, feature: GeneratedFeatures, alias: Optional[str] = None, tests: Optional[List[AnyDescriptorTest]] = None
    ):
        # this is needed because we try to access it before super call
        feature = feature if isinstance(feature, GeneratedFeatures) else parse_obj_as(GeneratedFeatures, feature)  # type: ignore[type-abstract]
        feature_columns = feature.list_columns()
        super().__init__(feature=feature, alias=alias or f"{feature_columns[0].display_name}", tests=tests)

    def get_dataset_column(self, column_name: str, values: pd.Series) -> DatasetColumn:
        column_type = self.feature.get_type(column_name)
        if column_type == ColumnType.Numerical:
            values = pd.to_numeric(values, errors="coerce")
        dataset_column = DatasetColumn(type=column_type, data=values)
        return dataset_column

    def generate_data(
        self, dataset: "Dataset", options: Options
    ) -> Union[DatasetColumn, Dict[DisplayName, DatasetColumn]]:
        feature = self.feature.generate_features_renamed(
            dataset.as_dataframe(),
            create_data_definition(None, dataset.as_dataframe(), ColumnMapping()),
            options,
        )
        return {
            col.display_name: self.get_dataset_column(col.name, feature[col.name])
            for col in self.feature.list_columns()
        }

    def list_output_columns(self) -> List[str]:
        return [c.display_name for c in self.feature.list_columns()]


def _determine_descriptor_column_name(alias: str, columns: List[str]):
    index = 1
    key = alias
    while key in columns:
        key = f"{alias}_{index}"
        index += 1
    return key


@dataclasses.dataclass
class StatCountValue:
    count: int
    share: float


@dataclasses.dataclass
class GeneralColumnStats:
    missing_values: StatCountValue


@dataclasses.dataclass
class NumericalColumnStats:
    max: Numeric
    min: Numeric
    mean: Numeric
    std: Numeric
    quantiles: Dict[str, Numeric]
    infinite: StatCountValue


@dataclasses.dataclass
class LabelStats:
    count: StatCountValue


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


PossibleDatasetTypes = Union["Dataset", pd.DataFrame]


class Dataset:
    _data_definition: DataDefinition
    _metadata: Dict[str, MetadataValueType]
    _tags: List[str]

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        descriptors: Optional[List[Descriptor]] = None,
        options: AnyOptions = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
    ) -> "Dataset":
        dataset = PandasDataset(data, data_definition, metadata=metadata, tags=tags)
        if descriptors is not None:
            dataset.add_descriptors(descriptors, options)
        return dataset

    @staticmethod
    def from_any(dataset: PossibleDatasetTypes) -> "Dataset":
        if isinstance(dataset, Dataset):
            return dataset
        if isinstance(dataset, pd.DataFrame):
            return Dataset.from_pandas(dataset)
        raise ValueError(f"Unsupported dataset type: {type(dataset)}")

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

    @property
    def metadata(self) -> Dict[str, MetadataValueType]:
        return self._metadata

    @property
    def tags(self) -> List[str]:
        return self._tags

    @abstractmethod
    def add_descriptor(self, descriptor: Descriptor, options: AnyOptions = None):
        raise NotImplementedError

    def add_descriptors(self, descriptors: List[Descriptor], options: AnyOptions = None):
        for descriptor in descriptors:
            self.add_descriptor(descriptor, options)

    @abstractmethod
    def save(self, uri: str):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _can_load(cls, uri: str) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _load(cls, uri: str) -> "Dataset":
        raise NotImplementedError

    @classmethod
    def load(cls, uri: str) -> "Dataset":
        for subclass in cls.__subclasses__():
            if subclass._can_load(uri):
                return subclass._load(uri)
        raise Exception(f"Dataset {uri} could not be loaded")


INTEGER_CARDINALITY_LIMIT = 10


def infer_column_type(column_data: pd.Series) -> ColumnType:
    if column_data.dtype.name.startswith("float"):
        return ColumnType.Numerical
    if column_data.dtype.name.startswith("int"):
        if column_data.nunique() <= INTEGER_CARDINALITY_LIMIT:
            return ColumnType.Categorical
        else:
            return ColumnType.Numerical
    if column_data.dtype.name in ["string"]:
        if column_data.nunique() > (column_data.count() * 0.5):
            return ColumnType.Text
        else:
            return ColumnType.Categorical
    if column_data.dtype.name == "object":
        without_na = column_data.dropna()
        if without_na.count() == 0:
            return ColumnType.Unknown
        if isinstance(without_na.iloc[0], str) and isinstance(without_na.iloc[-1], str):
            if column_data.nunique() > (column_data.count() * 0.5):
                return ColumnType.Text
            else:
                return ColumnType.Categorical
        elif isinstance(without_na.iloc[0], (list, tuple)) and isinstance(without_na.iloc[-1], (list, tuple)):
            return ColumnType.List
        return ColumnType.Unknown
    if column_data.dtype.name in ["bool", "category"]:
        return ColumnType.Categorical
    if column_data.dtype.name.startswith("datetime"):
        return ColumnType.Datetime
    return ColumnType.Unknown


MARKER_CONTENT = """{"version": "1.0"}"""
MARKER_FILENAME = ".evidently_dataset"
DATA_FILENAME = "data.parquet"
META_FILENAME = "dataset.json"


def _write_evidently_dataset(dataset: Dataset, uri: str):
    with tarfile.open(uri, "w") as tar:  # todo: use fsspec location
        # Add marker file
        marker_data = MARKER_CONTENT.encode("utf-8")
        marker_info = tarfile.TarInfo(MARKER_FILENAME)
        marker_info.size = len(marker_data)
        tar.addfile(marker_info, io.BytesIO(marker_data))

        # Add dataframe as parquet
        buffer = io.BytesIO()
        dataset.as_dataframe().to_parquet(buffer, index=False)
        buffer.seek(0)
        data_info = tarfile.TarInfo(DATA_FILENAME)
        data_info.size = len(buffer.getbuffer())
        tar.addfile(data_info, buffer)

        # Add metadata as JSON
        metadata = {
            "tags": dataset.tags,
            "metadata": dataset.metadata,
            "data_definition": dataset.data_definition.dict(),
        }
        meta_bytes = json.dumps(metadata, indent=2).encode("utf-8")
        meta_info = tarfile.TarInfo(META_FILENAME)
        meta_info.size = len(meta_bytes)
        tar.addfile(meta_info, io.BytesIO(meta_bytes))


def _read_evidently_dataset(uri: str) -> Dataset:
    with tarfile.open(uri, "r") as tar:
        names = tar.getnames()

        # Check marker
        if MARKER_FILENAME not in names:
            raise ValueError("Not a valid Evidently dataset: missing marker")
        marker_file = tar.extractfile(MARKER_FILENAME)
        if marker_file is None or marker_file.read().decode("utf-8") != MARKER_CONTENT:
            raise ValueError("Invalid Evidently dataset marker content")

        # Load dataframe
        if DATA_FILENAME not in names:
            raise ValueError("Missing data file in Evidently dataset")
        data_file = tar.extractfile(DATA_FILENAME)
        if data_file is None:
            raise ValueError("Missing data file in Evidently dataset")
        df = pd.read_parquet(data_file)

        # Load metadata
        if META_FILENAME not in names:
            raise ValueError("Missing metadata file in Evidently dataset")
        meta_file = tar.extractfile(META_FILENAME)
        if meta_file is None:
            raise ValueError("Missing metadata file in Evidently dataset")
        metadata = json.load(meta_file)

    return Dataset.from_pandas(
        df,
        data_definition=DataDefinition.parse_obj(metadata["data_definition"]),
        metadata=metadata["metadata"],
        tags=metadata["tags"],
    )


class PandasDataset(Dataset):
    SUPPORTED_FORMATS = {"csv": pd.read_csv, "parquet": pd.read_parquet, EVIDENTLY_DATASET_EXT: _read_evidently_dataset}
    _data: pd.DataFrame
    _data_definition: DataDefinition
    _dataset_stats: DatasetStats
    _metadata: Dict[str, MetadataValueType]
    _tags: List[str]

    def __init__(
        self,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        metadata: Dict[str, MetadataValueType] = None,
        tags: List[str] = None,
    ):
        self._data = data.copy()
        if (
            data_definition is None
            or data_definition.datetime_columns is None
            or data_definition.categorical_columns is None
            or data_definition.text_columns is None
            or data_definition.numerical_columns is None
        ):
            reserved_fields = []
            if data_definition is not None:
                if data_definition.service_columns is not None:
                    if data_definition.service_columns.trace_link is not None:
                        reserved_fields.append(data_definition.service_columns.trace_link)
                if data_definition.timestamp is not None:
                    reserved_fields.append(data_definition.timestamp)
                if data_definition.id_column is not None:
                    reserved_fields.append(data_definition.id_column)
                if data_definition.numerical_columns is not None:
                    reserved_fields.extend(data_definition.numerical_columns)
                if data_definition.categorical_columns is not None:
                    reserved_fields.extend(data_definition.categorical_columns)
                if data_definition.datetime_columns is not None:
                    reserved_fields.extend(data_definition.datetime_columns)
                if data_definition.text_columns is not None:
                    reserved_fields.extend(data_definition.text_columns)
                if data_definition.numerical_descriptors is not None:
                    reserved_fields.extend(data_definition.numerical_descriptors)
                if data_definition.categorical_descriptors is not None:
                    reserved_fields.extend(data_definition.categorical_descriptors)
            generated_data_definition = self._generate_data_definition(
                data,
                reserved_fields,
                data_definition.service_columns if data_definition is not None else None,
            )
            if data_definition is None:
                self._data_definition = generated_data_definition
            else:
                self._data_definition = copy.deepcopy(data_definition)
                if self._data_definition.datetime_columns is None:
                    if self._data_definition.timestamp is not None and generated_data_definition.timestamp is not None:
                        self._data_definition.datetime_columns = [generated_data_definition.timestamp]
                    else:
                        self._data_definition.datetime_columns = generated_data_definition.datetime_columns
                if self._data_definition.numerical_columns is None:
                    self._data_definition.numerical_columns = generated_data_definition.numerical_columns
                if self._data_definition.categorical_columns is None:
                    self._data_definition.categorical_columns = generated_data_definition.categorical_columns
                if self._data_definition.text_columns is None:
                    self._data_definition.text_columns = generated_data_definition.text_columns
                if self._data_definition.timestamp is None and generated_data_definition.timestamp is not None:
                    self._data_definition.timestamp = generated_data_definition.timestamp
                if (
                    self._data_definition.service_columns is None
                    and generated_data_definition.service_columns is not None
                ):
                    self._data_definition.service_columns = generated_data_definition.service_columns
        else:
            self._data_definition = copy.deepcopy(data_definition)
        (rows, columns) = data.shape

        column_stats = {}
        for column in data.columns:
            column_stats[column] = self._collect_stats(self._data_definition.get_column_type(column), data[column])
        self._dataset_stats = DatasetStats(rows, columns, column_stats)
        self._metadata = metadata or {}
        self._tags = tags or []

    def as_dataframe(self) -> pd.DataFrame:
        return self._data

    def column(self, column_name: str) -> DatasetColumn:
        return DatasetColumn(self._data_definition.get_column_type(column_name), self._data[column_name])

    def subdataset(self, column_name: str, label: object):
        return PandasDataset(self._data[self._data[column_name] == label], self._data_definition)

    def _generate_data_definition(
        self,
        data: pd.DataFrame,
        reserved_fields: List[str],
        service_columns: Optional[ServiceColumns] = None,
    ) -> DataDefinition:
        numerical = []
        categorical = []
        text = []
        datetime = []
        service = None
        for column in data.columns:
            if column in reserved_fields:
                continue
            if service_columns is None and column == DEFAULT_TRACE_LINK_COLUMN:
                if service is None:
                    service = ServiceColumns(trace_link=column)
                else:
                    service.trace_link = column
                continue
            column_type = infer_column_type(data[column])
            if column_type == ColumnType.Numerical:
                numerical.append(column)
            if column_type == ColumnType.Categorical:
                categorical.append(column)
            if column_type == ColumnType.Datetime:
                datetime.append(column)
            if column_type == ColumnType.Text:
                text.append(column)

        return DataDefinition(
            timestamp=datetime[0] if len(datetime) == 1 else None,
            service_columns=service,
            numerical_columns=numerical,
            categorical_columns=categorical,
            datetime_columns=datetime if len(datetime) != 1 else [],
            text_columns=text,
        )

    def stats(self) -> DatasetStats:
        return self._dataset_stats

    def add_column(self, key: str, data: DatasetColumn, add_to_descriptor_list: bool = True):
        self._dataset_stats.column_count += 1
        self._dataset_stats.column_stats[key] = self._collect_stats(data.type, data.data)
        self._data[key] = data.data
        if add_to_descriptor_list and data.type == ColumnType.Numerical:
            self._data_definition.numerical_descriptors.append(key)
        if add_to_descriptor_list and data.type == ColumnType.Categorical:
            self._data_definition.categorical_descriptors.append(key)

    def add_descriptor(self, descriptor: Descriptor, options: AnyOptions = None):
        descriptor.validate_input(self._data_definition)
        new_columns = descriptor.generate_data(self, Options.from_any_options(options))
        if isinstance(new_columns, DatasetColumn):
            new_columns = {descriptor.alias: new_columns}
        rename = {}
        for col, value in new_columns.items():
            name = _determine_descriptor_column_name(col, self._data.columns.tolist())
            rename[col] = name
            self.add_column(name, value, descriptor.add_to_descriptors_list())
            if isinstance(descriptor, ColumnTest):
                if self._data_definition.test_descriptors is None:
                    self._data_definition.test_descriptors = []
                self._data_definition.test_descriptors.append(name)
        self.data_definition.special_columns.extend(descriptor.get_special_columns_info(rename))
        for sub in descriptor.get_sub_descriptors():
            self.add_descriptor(sub, options)

    def _collect_stats(self, column_type: ColumnType, data: pd.Series):
        numerical_stats = None
        if column_type == ColumnType.Numerical:
            numerical_stats = _collect_numerical_stats(data)

        categorical_stats = None
        if column_type == ColumnType.Categorical:
            categorical_stats = _collect_categorical_stats(data)

        return ColumnStats(
            general_stats=GeneralColumnStats(missing_values=StatCountValue(0, 0)),
            numerical_stats=numerical_stats,
            categorical_stats=categorical_stats,
        )

    def save(self, uri: str):
        if not uri.endswith(f".{EVIDENTLY_DATASET_EXT}"):
            uri += f".{EVIDENTLY_DATASET_EXT}"
        _write_evidently_dataset(self, uri)

    @classmethod
    def _can_load(cls, uri: str) -> bool:
        split = uri.split(".")[-1]
        return split in cls.SUPPORTED_FORMATS or os.path.exists(f"{uri}.{EVIDENTLY_DATASET_EXT}")

    @classmethod
    def _load(cls, uri: str) -> "Dataset":
        ext = uri.split(".")[-1]
        if ext not in cls.SUPPORTED_FORMATS:
            if os.path.exists(f"{uri}.{EVIDENTLY_DATASET_EXT}"):
                ext = EVIDENTLY_DATASET_EXT
                uri = f"{uri}.{ext}"
            else:
                raise ValueError(f"Unsupported format: {ext}")
        # todo: load from fsspec stream instead
        data = cls.SUPPORTED_FORMATS[ext](uri)  # type: ignore[operator]
        if isinstance(data, Dataset):
            return data
        return Dataset.from_pandas(data)


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
        infinite=StatCountValue(infinite_count, infinite_count / data.count()),
    )


def _collect_categorical_stats(data: pd.Series):
    total_count = data.count()
    return CategoricalColumnStats(
        unique_count=data.nunique(),
        label_stats={
            label: LabelStats(count=StatCountValue(count, count / total_count))
            for label, count in data.value_counts().items()
        },
    )
