from typing import Optional

from evidently.metrics import ClassificationQualityByClass
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import ByLabelValue
from evidently.v2.metrics import Metric
from evidently.v2.metrics.base import TResult
from evidently.v2.report import Context


class F1Metric(Metric[ByLabelValue]):
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
