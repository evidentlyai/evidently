from typing import Optional

from evidently.metrics import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClassRenderer
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import ByLabelValue
from evidently.v2.metrics import Metric
from evidently.v2.metrics.base import TResult
from evidently.v2.report import Context


class F1Metric(Metric[ByLabelValue]):
    class Config:
        type_alias = "evidently:metric_v2:F1Metric"

    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        super().__init__("f1")
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))
        return ByLabelValue(
            {k: v.f1 for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "F1 metric"


class PrecisionMetric(Metric[ByLabelValue]):
    class Config:
        type_alias = "evidently:metric_v2:PrecisionMetric"

    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        super().__init__("precision")
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))
        return ByLabelValue(
            {k: v.precision for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Precision metric"


class RecallMetric(Metric[ByLabelValue]):
    class Config:
        type_alias = "evidently:metric_v2:RecallMetric"

    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        super().__init__("recall")
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        result = context.get_legacy_metric(ClassificationQualityByClass(self.probas_threshold, self.k))

        return ByLabelValue(
            {k: v.recall for k, v in result.current.metrics.items()},
        )

    def display_name(self) -> str:
        return "Recall metric"


class RocAucMetric(Metric[ByLabelValue]):
    class Config:
        type_alias = "evidently:metric_v2:RocAucMetric"

    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        super().__init__("roc_auc")
        self.probas_threshold = probas_threshold
        self.k = k

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        raise ValueError()

    def _call(self, context: Context) -> ByLabelValue:
        metric = ClassificationQualityByClass(self.probas_threshold, self.k)
        result = context.get_legacy_metric(metric)

        object.__setattr__(metric, "get_result", lambda: result)

        value = ByLabelValue(
            {k: v.roc_auc for k, v in result.current.metrics.items()},
        )

        value.widget = [ClassificationQualityByClassRenderer().render_html(metric)[1]]
        value.widget[0].title = self.display_name()
        return value

    def display_name(self) -> str:
        return "ROC AUC metric"
