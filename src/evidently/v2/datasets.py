from typing import Dict
from typing import Optional

import pandas as pd

from evidently import ColumnType
from evidently.features.generated_features import GeneratedFeature


class DataDefinition:
    pass


class DatasetColumn:
    type: ColumnType
    data: pd.Series

    def __init__(self, type: ColumnType, data: pd.Series) -> None:
        self.type = type
        self.data = data


class Scorer:
    def generate_data(self, dataset: "Dataset") -> DatasetColumn:
        raise NotImplementedError()


class FeatureScorer(Scorer):
    def __init__(self, feature: GeneratedFeature):
        self.feature = feature

    def generate_data(self, dataset: "Dataset") -> DatasetColumn:
        feature = self.feature.generate_feature(dataset.as_dataframe(), None)
        return DatasetColumn(type=self.feature.get_type(), data=feature[feature.columns[0]])


class Dataset:
    _data_definition: DataDefinition

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        scorers: Optional[Dict[str, Scorer]] = None,
    ) -> "Dataset":
        dataset = PandasDataset(data, data_definition)
        for key, scorer in scorers.items():
            new_column = scorer.generate_data(dataset)
            data[key] = new_column.data
        return dataset

    def as_dataframe(self) -> pd.DataFrame:
        raise NotImplementedError()

    def column(self, column_name: str) -> pd.Series:
        raise NotImplementedError()


class PandasDataset(Dataset):
    _data: pd.DataFrame

    def __init__(
        self,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
    ):
        self._data = data
        if data_definition is None:
            self._generate_data_definition()
        else:
            self._data_definition = data_definition

    def as_dataframe(self) -> pd.DataFrame:
        return self._data

    def column(self, column_name: str) -> pd.Series:
        return self._data[column_name]

    def _generate_data_definition(self):
        raise NotImplementedError()
