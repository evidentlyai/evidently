from typing import Dict
from typing import Optional

import pandas as pd

from evidently import ColumnType


class DataDefinition:
    pass


class DatasetColumn:
    type: ColumnType
    data: pd.Series


class Scorer:
    def generate_data(self, dataset: "Dataset") -> DatasetColumn:
        raise NotImplementedError()


class Dataset:
    _data_definition: DataDefinition

    @classmethod
    def from_pandas(
        cls,
        data: pd.DataFrame,
        data_definition: Optional[DataDefinition] = None,
        scorers: Optional[Dict[str, Scorer]] = None,
    ) -> "Dataset":
        return PandasDataset(data, data_definition)

    def as_dataframe(self):
        pass

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

    def column(self, column_name: str) -> pd.Series:
        return self._data[column_name]

    def _generate_data_definition(self):
        raise NotImplementedError()
