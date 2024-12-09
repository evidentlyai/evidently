import abc
import dataclasses
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from evidently import ColumnType
from evidently.features.generated_features import GeneratedFeatures
from evidently.options.base import Options


@dataclasses.dataclass
class ColumnInfo:
    type: ColumnType


class DataDefinition:
    _columns: Dict[str, ColumnInfo]

    def __init__(self, columns: Dict[str, ColumnInfo]):
        self._columns = columns

    def get_column_type(self, column_name: str) -> ColumnType:
        # TODO: implement
        return ColumnType.Unknown


class DatasetColumn:
    type: ColumnType
    data: pd.Series

    def __init__(self, type: ColumnType, data: pd.Series) -> None:
        self.type = type
        self.data = data


class Scorer:
    def __init__(self, alias: str):
        self._alias = alias

    @abc.abstractmethod
    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        raise NotImplementedError()

    @property
    def alias(self) -> str:
        return self._alias


class FeatureScorer(Scorer):
    def __init__(self, feature: GeneratedFeatures, alias: Optional[str] = None):
        super().__init__(alias)
        self._feature = feature
        self._alias = alias

    def generate_data(self, dataset: "Dataset") -> Union[DatasetColumn, Dict[str, DatasetColumn]]:
        feature = self._feature.generate_features(dataset.as_dataframe(), None, Options())
        if len(feature.columns) > 1:
            return {
                col: DatasetColumn(
                    type=self._feature.get_type(f"{self._feature.get_fingerprint()}.{col}"), data=feature[col]
                )
                for col in feature.columns
            }
        return DatasetColumn(type=self._feature.get_type(), data=feature[feature.columns[0]])


class Dataset:
    _data_definition: DataDefinition

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        scorers: Optional[List[Scorer]] = None,
    ) -> "Dataset":
        dataset = PandasDataset(data, data_definition)
        for scorer in scorers or []:
            key = scorer.alias
            new_column = scorer.generate_data(dataset)
            if isinstance(new_column, DatasetColumn):
                data[key] = new_column.data
            elif len(new_column) > 1:
                for col, value in new_column.items():
                    data[f"{key}.{col}"] = value.data
            else:
                data[key] = list(new_column.values())[0].data
        return dataset

    def as_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError()

    def column(self, column_name: str) -> DatasetColumn:
        raise NotImplementedError()

    def subdataset(self, column_name: str, label: object) -> "Dataset":
        raise NotImplementedError()


class PandasDataset(Dataset):
    _data: pd.DataFrame
    _data_definition: DataDefinition

    def __init__(
        self,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
    ):
        self._data = data
        if data_definition is None:
            self._data_definition = self._generate_data_definition(data)
        else:
            self._data_definition = data_definition

    def as_dataframe(self) -> pd.DataFrame:
        return self._data

    def column(self, column_name: str) -> DatasetColumn:
        return DatasetColumn(self._data_definition.get_column_type(column_name), self._data[column_name])

    def subdataset(self, column_name: str, label: object):
        return PandasDataset(self._data[self._data[column_name] == label], self._data_definition)

    def _generate_data_definition(self, data: pd.DataFrame) -> DataDefinition:
        return DataDefinition(columns={column: ColumnInfo(ColumnType.Unknown) for column in data.columns})
