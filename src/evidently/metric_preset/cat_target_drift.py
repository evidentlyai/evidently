from evidently.utils.data_operations import DatasetColumns
from evidently.metrics.base_metric import InputData
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.cat_target_drift_metrics import CatTargetDriftMetrics
from evidently.metrics.probability_distribution import ProbabilityDistributionMetric


class CatTargetDrift(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [CatTargetDriftMetrics(), ProbabilityDistributionMetric()]
