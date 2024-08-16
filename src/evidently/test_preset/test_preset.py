import abc
from typing import Any
from typing import Dict
from typing import Optional

from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import DataDefinition


class TestPreset(EvidentlyBaseModel):
    class Config:
        is_base_type = True

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def generate_tests(self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]):
        raise NotImplementedError
