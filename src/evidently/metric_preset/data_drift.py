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
    columns: Optional[List[str]]
    drift_share: float
    all_features_stattest: Optional[PossibleStatTestType]
    cat_features_stattest: Optional[PossibleStatTestType]
    num_features_stattest: Optional[PossibleStatTestType]
    per_feature_stattest: Optional[Dict[str, PossibleStatTestType]]
    all_features_threshold: Optional[float]
    cat_features_threshold: Optional[float]
    num_features_threshold: Optional[float]
    per_feature_threshold: Optional[Dict[str, float]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        drift_share: float = 0.5,
        all_features_stattest: Optional[PossibleStatTestType] = None,
        cat_features_stattest: Optional[PossibleStatTestType] = None,
        num_features_stattest: Optional[PossibleStatTestType] = None,
        per_feature_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        all_features_threshold: Optional[float] = None,
        cat_features_threshold: Optional[float] = None,
        num_features_threshold: Optional[float] = None,
        per_feature_threshold: Optional[Dict[str, float]] = None,
    ):
        super().__init__()
        self.columns = columns
        self.drift_share = drift_share
        self.all_features_stattest = all_features_stattest
        self.cat_features_stattest = cat_features_stattest
        self.num_features_stattest = num_features_stattest
        self.per_feature_stattest = per_feature_stattest
        self.all_features_threshold = all_features_threshold
        self.cat_features_threshold = cat_features_threshold
        self.num_features_threshold = num_features_threshold
        self.per_feature_threshold = per_feature_threshold

    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [
            DatasetDriftMetric(
                columns=self.columns,
                drift_share=self.drift_share,
                all_features_stattest=self.all_features_stattest,
                cat_features_stattest=self.cat_features_stattest,
                num_features_stattest=self.num_features_stattest,
                per_feature_stattest=self.per_feature_stattest,
                all_features_threshold=self.all_features_threshold,
                cat_features_threshold=self.cat_features_threshold,
                num_features_threshold=self.num_features_threshold,
                per_feature_threshold=self.per_feature_threshold,
            ),
            DataDriftTable(columns=self.columns),
        ]
