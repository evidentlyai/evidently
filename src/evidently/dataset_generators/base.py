from abc import ABC

from evidently.pydantic_utils import EvidentlyBaseModel


class BaseDatasetGenerator(EvidentlyBaseModel, ABC):
    class Config:
        type_alias = "evidently:dataset_generator:BaseDatasetGenerator"
        is_base_type = True

    def generate(self):
        pass
