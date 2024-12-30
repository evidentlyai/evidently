from typing import Dict
from typing import List
from typing import Optional

from evidently.future.datasets import Dataset
from evidently.future.metrics import ByLabelValue
from evidently.future.metrics import MetricPreset
from evidently.future.metrics import MetricResult
from evidently.future.metrics.base import ByLabelCalculation
from evidently.future.metrics.base import ByLabelMetric
from evidently.future.metrics.base import Metric
from evidently.future.metrics.base import MetricId
from evidently.future.metrics.presets import PresetResult
from evidently.future.report import Context
from evidently.metrics import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClassRenderer


class F1Metric(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class F1MetricCalculation(ByLabelCalculation[F1Metric]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k))
        return ByLabelValue(
            {k: v.f1 for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "F1 metric"


class PrecisionMetric(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class PrecisionMetricCalculation(ByLabelCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k))
        return ByLabelValue(
            {k: v.precision for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Precision metric"


class RecallMetric(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RecallMetricCalculation(ByLabelCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k))

        return ByLabelValue(
            {k: v.recall for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Recall metric"


class RocAucMetric(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RocAucCalculation(ByLabelCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        metric = ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k)
        result = context.get_legacy_metric(metric)

        object.__setattr__(metric, "get_result", lambda: result)

        value = ByLabelValue(
            {k: v.roc_auc for k, v in result.current.metrics.items()},
        )

        value.widget = ClassificationQualityByClassRenderer().render_html(metric)
        value.widget[0].params["counters"][0]["label"] = self.display_name()
        return value

    def display_name(self) -> str:
        return "ROC AUC metric"


class QualityByClassPreset(MetricPreset):
    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        self._probas_threshold = probas_threshold
        self._k = k

    def metrics(self) -> List[Metric]:
        return [
            F1Metric(probas_threshold=self._probas_threshold, k=self._k),
            PrecisionMetric(probas_threshold=self._probas_threshold, k=self._k),
            RecallMetric(probas_threshold=self._probas_threshold, k=self._k),
            RocAucMetric(probas_threshold=self._probas_threshold, k=self._k),
        ]

    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        metric = RocAucMetric(probas_threshold=self._probas_threshold, k=self._k)
        return PresetResult(metric_results[metric.to_calculation().id].widget)
