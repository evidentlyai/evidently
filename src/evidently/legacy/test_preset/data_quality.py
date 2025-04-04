from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from evidently.legacy.test_preset.test_preset import AnyTest
from evidently.legacy.test_preset.test_preset import TestPreset
from evidently.legacy.tests import TestAllColumnsMostCommonValueShare
from evidently.legacy.tests import TestAllColumnsShareOfMissingValues
from evidently.legacy.tests import TestNumberOfConstantColumns
from evidently.legacy.tests import TestNumberOfDuplicatedColumns
from evidently.legacy.tests import TestNumberOfDuplicatedRows
from evidently.legacy.utils.data_preprocessing import DataDefinition


class DataQualityTestPreset(TestPreset):
    class Config:
        type_alias = "evidently:test_preset:DataQualityTestPreset"

    """
    Data Quality tests.

    Contains tests:
    - `TestAllColumnsShareOfMissingValues`
    - `TestAllColumnsMostCommonValueShare`
    - `TestNumberOfConstantColumns`
    - `TestNumberOfDuplicatedColumns`
    - `TestNumberOfDuplicatedRows`
    - `TestHighlyCorrelatedColumns`
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
            TestAllColumnsShareOfMissingValues(columns=self.columns),
            TestAllColumnsMostCommonValueShare(columns=self.columns),
            TestNumberOfConstantColumns(),
            TestNumberOfDuplicatedColumns(),
            TestNumberOfDuplicatedRows(),
        ]
