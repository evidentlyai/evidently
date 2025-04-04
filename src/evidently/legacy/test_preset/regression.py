from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.test_preset.test_preset import AnyTest
from evidently.legacy.test_preset.test_preset import TestPreset
from evidently.legacy.tests import TestValueMAE
from evidently.legacy.tests import TestValueMAPE
from evidently.legacy.tests import TestValueMeanError
from evidently.legacy.tests import TestValueRMSE
from evidently.legacy.utils.data_preprocessing import DataDefinition


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
