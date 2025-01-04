import abc
from typing import Dict
from typing import List
from typing import Optional

from typing_extensions import Generic

from evidently.future.datasets import Dataset
from evidently.future.metric_types import ByLabelMetric
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metric_types import TMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.preset_types import MetricPreset
from evidently.future.preset_types import PresetResult
from evidently.future.report import Context
from evidently.metrics import ClassificationQualityByClass as _ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClassResult
from evidently.model.widget import BaseWidgetInfo


class F1ByLabel(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class LegacyClassificationQualityByClass(
    LegacyMetricCalculation[ByLabelValue, TMetric, ClassificationQualityByClassResult, _ClassificationQualityByClass],
    Generic[TMetric],
    abc.ABC,
):
    _legacy_metric = None

    def legacy_metric(self) -> _ClassificationQualityByClass:
        if self._legacy_metric is None:
            self._legacy_metric = _ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k)
        return self._legacy_metric

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise NotImplementedError()

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        raise NotImplementedError()


class F1ByLabelCalculation(LegacyClassificationQualityByClass[F1ByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        return ByLabelValue({k: v.f1 for k, v in legacy_result.current.metrics.items()})

    def display_name(self) -> str:
        return "F1 by Label metric"


class PrecisionByLabel(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class PrecisionByLabelCalculation(LegacyClassificationQualityByClass[PrecisionByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        return ByLabelValue(
            {k: v.precision for k, v in legacy_result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Precision by Label metric"


class RecallByLabel(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RecallByLabelCalculation(LegacyClassificationQualityByClass[RecallByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        return ByLabelValue(
            {k: v.recall for k, v in legacy_result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Recall by Label metric"


class RocAucByLabel(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RocAucByLabelCalculation(LegacyClassificationQualityByClass[RocAucByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        value = ByLabelValue(
            {k: v.roc_auc for k, v in legacy_result.current.metrics.items()},
        )
        value.widget = render
        value.widget[0].params["counters"][0]["label"] = self.display_name()
        return value

    def display_name(self) -> str:
        return "ROC AUC by Label metric"


class ClassificationQualityByClass(MetricPreset):
    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        self._probas_threshold = probas_threshold
        self._k = k

    def metrics(self) -> List[Metric]:
        return [
            F1ByLabel(probas_threshold=self._probas_threshold, k=self._k),
            PrecisionByLabel(probas_threshold=self._probas_threshold, k=self._k),
            RecallByLabel(probas_threshold=self._probas_threshold, k=self._k),
            RocAucByLabel(probas_threshold=self._probas_threshold, k=self._k),
        ]

    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        metric = RocAucByLabel(probas_threshold=self._probas_threshold, k=self._k)
        return PresetResult(metric_results[metric.to_calculation().id].widget)
