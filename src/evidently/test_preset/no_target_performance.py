from typing import Dict
from typing import List
from typing import Optional

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllColumnsShareOfMissingValues
from evidently.tests import TestCatColumnsOutOfListValues
from evidently.tests import TestColumnsType
from evidently.tests import TestColumnValueDrift
from evidently.tests import TestCustomFeaturesValueDrift
from evidently.tests import TestNumColumnsMeanInNSigmas
from evidently.tests import TestNumColumnsOutOfRangeValues
from evidently.tests import TestShareOfDriftedColumns
from evidently.utils.data_operations import DatasetColumns


class NoTargetPerformanceTestPreset(TestPreset):
    columns: Optional[List[str]]
    drift_share: float
    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None
    stattest_threshold: Optional[float] = None
    cat_stattest_threshold: Optional[float] = None
    num_stattest_threshold: Optional[float] = None
    per_column_stattest_threshold: Optional[Dict[str, float]] = None
    prediction_stattest: Optional[PossibleStatTestType]
    prediction_threshold: Optional[float]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        drift_share: float = 0.5,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
        prediction_stattest: Optional[PossibleStatTestType] = None,
        prediction_threshold: Optional[float] = None,
    ):
        super().__init__()
        self.columns = columns
        self.drift_share = drift_share
        self.stattest = stattest
        self.cat_stattest = cat_stattest
        self.num_stattest = num_stattest
        self.per_column_stattest = per_column_stattest
        self.stattest_threshold = stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.num_features_threshold = num_stattest_threshold
        self.per_feature_threshold = per_column_stattest_threshold
        self.prediction_stattest = prediction_stattest
        self.prediction_threshold = prediction_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        preset_tests: List = []

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            preset_tests.append(
                TestColumnValueDrift(
                    column_name=columns.utility_columns.prediction,
                    stattest=self.prediction_stattest,
                    stattest_threshold=self.prediction_threshold,
                )
            )

        preset_tests.append(
            TestShareOfDriftedColumns(
                lt=data.current_data.shape[1] // 3,
                stattest=self.stattest,
                cat_stattest=self.cat_stattest,
                num_stattest=self.num_stattest,
                per_column_stattest=self.per_column_stattest,
                stattest_threshold=self.stattest_threshold,
                cat_stattest_threshold=self.cat_stattest_threshold,
                num_stattest_threshold=self.num_features_threshold,
                per_column_stattest_threshold=self.per_feature_threshold,
            )
        )
        preset_tests.append(TestColumnsType())
        preset_tests.append(TestAllColumnsShareOfMissingValues(columns=self.columns))
        preset_tests.append(TestNumColumnsOutOfRangeValues(columns=self.columns))
        preset_tests.append(TestCatColumnsOutOfListValues(columns=self.columns))
        preset_tests.append(TestNumColumnsMeanInNSigmas(columns=self.columns))

        if self.columns:
            preset_tests.append(TestCustomFeaturesValueDrift(features=self.columns))

        return preset_tests
