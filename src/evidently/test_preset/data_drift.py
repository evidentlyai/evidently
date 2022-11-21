from typing import Optional

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllFeaturesValueDrift
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestShareOfDriftedColumns
from evidently.utils.data_operations import DatasetColumns


class DataDriftTestPreset(TestPreset):
    target_stattest: Optional[PossibleStatTestType]
    prediction_stattest: Optional[PossibleStatTestType]
    target_stattest_threshold: Optional[float]
    prediction_stattest_threshold: Optional[float]

    def __init__(
        self,
        target_stattest: Optional[PossibleStatTestType] = None,
        prediction_stattest: Optional[PossibleStatTestType] = None,
        target_stattest_threshold: Optional[float] = None,
        prediction_stattest_threshold: Optional[float] = None,
    ):
        super().__init__()
        self.target_stattest = target_stattest
        self.prediction_stattest = prediction_stattest
        self.target_stattest_threshold = target_stattest_threshold
        self.prediction_stattest_threshold = prediction_stattest_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: list = [TestShareOfDriftedColumns()]

        if columns.utility_columns.target is not None:
            preset_tests.append(
                TestColumnValueDrift(
                    column_name=columns.utility_columns.target,
                    stattest_threshold=self.target_stattest_threshold,
                    stattest=self.target_stattest,
                )
            )

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(
                TestColumnValueDrift(
                    column_name=columns.utility_columns.prediction,
                    stattest_threshold=self.prediction_stattest_threshold,
                    stattest=self.prediction_stattest,
                )
            )

        preset_tests.append(TestAllFeaturesValueDrift())

        return preset_tests
