from abc import ABC
from abc import abstractmethod

import pandas as pd

from evidently.options.base import Options
from evidently.pydantic_utils import EvidentlyBaseModel

DatasetGeneratorResult = pd.DataFrame


class BaseDatasetGenerator(EvidentlyBaseModel, ABC):
    class Config:
        type_alias = "evidently:dataset_generator:BaseDatasetGenerator"
        is_base_type = True
        alias_required = False  # fixme

    options: Options

    @abstractmethod
    def generate(self) -> DatasetGeneratorResult:
        raise NotImplementedError
