from typing import Dict
from typing import List
from typing import Optional

from evidently.future.container import MetricContainer
from evidently.future.datasets import BinaryClassification
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import FNR
from evidently.future.metrics import FPR
from evidently.future.metrics import TNR
from evidently.future.metrics import TPR
from evidently.future.metrics import Accuracy
from evidently.future.metrics import F1ByLabel
from evidently.future.metrics import F1Score
from evidently.future.metrics import LogLoss
from evidently.future.metrics import Precision
from evidently.future.metrics import PrecisionByLabel
from evidently.future.metrics import Recall
from evidently.future.metrics import RecallByLabel
from evidently.future.metrics import RocAuc
from evidently.future.metrics import RocAucByLabel
from evidently.future.metrics.classification import DummyF1Score
from evidently.future.metrics.classification import DummyPrecision
from evidently.future.metrics.classification import DummyRecall
from evidently.future.report import Context
from evidently.metrics import ClassificationDummyMetric
from evidently.metrics import ClassificationQualityByClass
from evidently.metrics import ClassificationQualityMetric
from evidently.model.widget import BaseWidgetInfo


class ClassificationQuality(MetricContainer):
    def generate_metrics(self, context: "Context") -> List[Metric]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationQuality without a classification data")

        metrics: List[Metric]

        if isinstance(classification, BinaryClassification):
            metrics = [
                Accuracy(),
                Precision(),
                Recall(),
                F1Score(),
            ]
            if classification.prediction_probas is not None:
                metrics.extend(
                    [
                        RocAuc(),
                        LogLoss(),
                    ]
                )
            metrics.extend(
                [
                    TPR(),
                    TNR(),
                    FPR(),
                    FNR(),
                ]
            )
        else:
            metrics = [
                Accuracy(),
                Precision(),
                Recall(),
                F1Score(),
            ]
            if classification.prediction_probas is not None:
                metrics.extend(
                    [
                        RocAuc(),
                        LogLoss(),
                    ]
                )
        return metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        _, render = context.get_legacy_metric(ClassificationQualityMetric())
        return render


class ClassificationQualityByLabel(MetricContainer):
    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        self._probas_threshold = probas_threshold
        self._k = k

    def generate_metrics(self, context: "Context") -> List[Metric]:
        return [
            F1ByLabel(probas_threshold=self._probas_threshold, k=self._k),
            PrecisionByLabel(probas_threshold=self._probas_threshold, k=self._k),
            RecallByLabel(probas_threshold=self._probas_threshold, k=self._k),
            RocAucByLabel(probas_threshold=self._probas_threshold, k=self._k),
        ]

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]):
        render = context.get_legacy_metric(ClassificationQualityByClass(self._probas_threshold, self._k))[1]
        widget = render
        widget[0].params["counters"][0]["label"] = "Classification Quality by Label"
        return widget


class ClassificationDummyQuality(MetricContainer):
    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        self._probas_threshold = probas_threshold
        self._k = k

    def generate_metrics(self, context: "Context") -> List[Metric]:
        return [
            DummyPrecision(),
            DummyRecall(),
            DummyF1Score(),
        ]

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        _, widgets = context.get_legacy_metric(ClassificationDummyMetric(self._probas_threshold, self._k))
        return widgets
