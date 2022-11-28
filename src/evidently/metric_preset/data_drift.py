from typing import Dict
from typing import List
from typing import Optional

from evidently.calculations.stattests import PossibleStatTestType
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import DataDriftTable
from evidently.metrics import DatasetDriftMetric
from evidently.metrics.base_metric import InputData
from evidently.utils.data_operations import DatasetColumns


class DataDriftPreset(MetricPreset):
    """Metric Preset for Data Drift analysis.

    Contains metrics:
    - DatasetDriftMetric
    - DataDriftTable
    """

    columns: Optional[List[str]]
    drift_share: float
    stattest: Optional[PossibleStatTestType]
    cat_stattest: Optional[PossibleStatTestType]
    num_stattest: Optional[PossibleStatTestType]
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]]
    stattest_threshold: Optional[float]
    cat_stattest_threshold: Optional[float]
    num_stattest_threshold: Optional[float]
    per_column_stattest_threshold: Optional[Dict[str, float]]

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
        self.num_stattest_threshold = num_stattest_threshold
        self.per_column_stattest_threshold = per_column_stattest_threshold

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            DatasetDriftMetric(
                columns=self.columns,
                drift_share=self.drift_share,
                stattest=self.stattest,
                cat_stattest=self.cat_stattest,
                num_stattest=self.num_stattest,
                per_column_stattest=self.per_column_stattest,
                stattest_threshold=self.stattest_threshold,
                cat_stattest_threshold=self.cat_stattest_threshold,
                num_stattest_threshold=self.num_stattest_threshold,
                per_column_stattest_threshold=self.per_column_stattest_threshold,
            ),
            DataDriftTable(
                columns=self.columns,
                stattest=self.stattest,
                cat_stattest=self.cat_stattest,
                num_stattest=self.num_stattest,
                per_column_stattest=self.per_column_stattest,
                stattest_threshold=self.stattest_threshold,
                cat_stattest_threshold=self.cat_stattest_threshold,
                num_stattest_threshold=self.num_stattest_threshold,
                per_column_stattest_threshold=self.per_column_stattest_threshold,
            ),
        ]
