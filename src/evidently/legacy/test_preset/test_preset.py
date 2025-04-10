import abc
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from evidently.legacy.base_metric import BasePreset
from evidently.legacy.tests.base_test import Test
from evidently.legacy.utils.data_preprocessing import DataDefinition
from evidently.legacy.utils.generators import BaseGenerator

AnyTest = Union[Test, BaseGenerator[Test]]


class TestPreset(BasePreset):
    class Config:
        is_base_type = True

    @abc.abstractmethod
    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        raise NotImplementedError
