from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.test_preset.test_preset import AnyTest
from evidently.legacy.test_preset.test_preset import TestPreset
from evidently.legacy.tests import TestAllColumnsShareOfMissingValues
from evidently.legacy.tests import TestCatColumnsOutOfListValues
from evidently.legacy.tests import TestColumnsType
from evidently.legacy.tests import TestNumberOfColumns
from evidently.legacy.tests import TestNumberOfRows
from evidently.legacy.tests import TestNumColumnsMeanInNSigmas
from evidently.legacy.tests import TestNumColumnsOutOfRangeValues
from evidently.legacy.utils.data_preprocessing import DataDefinition


class DataStabilityTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:DataStabilityTestPreset"

    """
    Data Stability tests.

    Contains tests:
    - `TestNumberOfRows`
    - `TestNumberOfColumns`
    - `TestColumnsType`
    - `TestAllColumnsShareOfMissingValues`
    - `TestNumColumnsOutOfRangeValues`
    - `TestCatColumnsOutOfListValues`
    - `TestNumColumnsMeanInNSigmas`
    """

    columns: Optional[List[str]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
    ):
        self.columns = columns
        super().__init__()

    def generate_tests(
        self, data_definition: DataDefinition, additional_data: Optional[Dict[str, Any]]
    ) -> List[AnyTest]:
        return [
            TestNumberOfRows(),
            TestNumberOfColumns(),
            TestColumnsType(),
            TestAllColumnsShareOfMissingValues(columns=self.columns),
            TestNumColumnsOutOfRangeValues(columns=self.columns),
            TestCatColumnsOutOfListValues(columns=self.columns),
            TestNumColumnsMeanInNSigmas(columns=self.columns),
        ]
