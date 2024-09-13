from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.test_preset.test_preset import AnyTest
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestValueMAE
from evidently.tests import TestValueMAPE
from evidently.tests import TestValueMeanError
from evidently.tests import TestValueRMSE
from evidently.utils.data_preprocessing import DataDefinition


class RegressionTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:RegressionTestPreset"

    """
    Regression performance tests.

    Contains tests:
    - `TestValueMeanError`
    - `TestValueMAE`
    - `TestValueRMSE`
    - `TestValueMAPE`
    """

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        return [
            TestValueMeanError(),
            TestValueMAE(),
            TestValueRMSE(),
            TestValueMAPE(),
        ]
