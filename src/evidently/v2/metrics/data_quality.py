from typing import Dict
from typing import List
from typing import Optional

from evidently.metric_results import Label
from evidently.metrics import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClassRenderer
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import ByLabelValue
from evidently.v2.metrics import Metric
from evidently.v2.metrics import MetricPreset
from evidently.v2.metrics import MetricResult
from evidently.v2.metrics.base import ByLabelMetric
from evidently.v2.metrics.base import MetricId
from evidently.v2.metrics.base import MetricTest
from evidently.v2.metrics.presets import PresetResult
from evidently.v2.report import Context


class F1Metric(ByLabelMetric):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        tests: Optional[Dict[Label, List[MetricTest]]] = None,
    ):
        super().__init__("f1")
        self.with_tests(tests)
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))
        return ByLabelValue(
            {k: v.f1 for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "F1 metric"


class PrecisionMetric(ByLabelMetric):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        tests: Optional[Dict[Label, List[MetricTest]]] = None,
    ):
        super().__init__("precision")
        self.with_tests(tests)
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))
        return ByLabelValue(
            {k: v.precision for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Precision metric"


class RecallMetric(ByLabelMetric):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        tests: Optional[Dict[Label, List[MetricTest]]] = None,
    ):
        super().__init__("recall")
        self.with_tests(tests)
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))

        return ByLabelValue(
            {k: v.recall for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Recall metric"


class RocAucMetric(ByLabelMetric):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        tests: Optional[Dict[Label, List[MetricTest]]] = None,
    ):
        super().__init__("roc_auc")
        self.with_tests(tests)
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        metric = ClassificationQualityByClass(self.probas_threshold, self.k)
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
            F1Metric(self._probas_threshold, self._k),
            PrecisionMetric(self._probas_threshold, self._k),
            RecallMetric(self._probas_threshold, self._k),
            RocAucMetric(self._probas_threshold, self._k),
        ]

    def calculate(self, metric_results: Dict[MetricId, MetricResult]) -> PresetResult:
        return PresetResult(metric_results[RocAucMetric(self._probas_threshold, self._k).id].widget)
