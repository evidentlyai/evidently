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
from evidently.future.metrics.classification import _gen_classification_input_data
from evidently.future.report import Context
from evidently.metrics import ClassificationConfusionMatrix
from evidently.metrics import ClassificationDummyMetric
from evidently.metrics import ClassificationPRCurve
from evidently.metrics import ClassificationPRTable
from evidently.metrics import ClassificationQualityByClass
from evidently.metrics import ClassificationQualityMetric
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import link_metric


class ClassificationQuality(MetricContainer):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        conf_matrix: bool = False,
        pr_curve: bool = False,
        pr_table: bool = False,
    ):
        self._probas_threshold = probas_threshold
        self._conf_matrix = conf_matrix
        self._pr_curve = pr_curve
        self._pr_table = pr_table

    def generate_metrics(self, context: "Context") -> List[Metric]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationQuality without a classification data")

        metrics: List[Metric]

        if isinstance(classification, BinaryClassification):
            metrics = [
                Accuracy(probas_threshold=self._probas_threshold),
                Precision(probas_threshold=self._probas_threshold),
                Recall(probas_threshold=self._probas_threshold),
                F1Score(probas_threshold=self._probas_threshold),
            ]
            if classification.prediction_probas is not None:
                metrics.extend(
                    [
                        RocAuc(probas_threshold=self._probas_threshold),
                        LogLoss(probas_threshold=self._probas_threshold),
                    ]
                )
            metrics.extend(
                [
                    TPR(probas_threshold=self._probas_threshold),
                    TNR(probas_threshold=self._probas_threshold),
                    FPR(probas_threshold=self._probas_threshold),
                    FNR(probas_threshold=self._probas_threshold),
                ]
            )
        else:
            metrics = [
                Accuracy(probas_threshold=self._probas_threshold),
                Precision(probas_threshold=self._probas_threshold),
                Recall(probas_threshold=self._probas_threshold),
                F1Score(probas_threshold=self._probas_threshold),
            ]
            if classification.prediction_probas is not None:
                metrics.extend(
                    [
                        RocAuc(probas_threshold=self._probas_threshold),
                        LogLoss(probas_threshold=self._probas_threshold),
                    ]
                )
        return metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        _, render = context.get_legacy_metric(
            ClassificationQualityMetric(probas_threshold=self._probas_threshold),
            _gen_classification_input_data,
        )
        if self._conf_matrix:
            render += context.get_legacy_metric(
                ClassificationConfusionMatrix(probas_threshold=self._probas_threshold),
                _gen_classification_input_data,
            )[1]
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationQuality without a classification data")
        if self._pr_curve and classification.prediction_probas is not None:
            render += context.get_legacy_metric(
                ClassificationPRCurve(probas_threshold=self._probas_threshold),
                _gen_classification_input_data,
            )[1]
        if self._pr_table and classification.prediction_probas is not None:
            render += context.get_legacy_metric(
                ClassificationPRTable(probas_threshold=self._probas_threshold),
                _gen_classification_input_data,
            )[1]
        for metric in self.metrics(context):
            link_metric(render, metric)
        return render


class ClassificationQualityByLabel(MetricContainer):
    def __init__(self, probas_threshold: Optional[float] = None, k: Optional[int] = None):
        self._probas_threshold = probas_threshold
        self._k = k

    def generate_metrics(self, context: "Context") -> List[Metric]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        return [
            F1ByLabel(probas_threshold=self._probas_threshold, k=self._k),
            PrecisionByLabel(probas_threshold=self._probas_threshold, k=self._k),
            RecallByLabel(probas_threshold=self._probas_threshold, k=self._k),
        ] + (
            []
            if classification.prediction_probas is None
            else [
                RocAucByLabel(probas_threshold=self._probas_threshold, k=self._k),
            ]
        )

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]):
        render = context.get_legacy_metric(
            ClassificationQualityByClass(self._probas_threshold, self._k),
            _gen_classification_input_data,
        )[1]
        widget = render
        widget[0].params["counters"][0]["label"] = "Classification Quality by Label"
        for metric in self.metrics(context):
            link_metric(widget, metric)
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
        _, widgets = context.get_legacy_metric(
            ClassificationDummyMetric(self._probas_threshold, self._k),
            _gen_classification_input_data,
        )
        for metric in self.metrics(context):
            link_metric(widgets, metric)
        return widgets


class ClassificationPreset(MetricContainer):
    def __init__(self, probas_threshold: Optional[float] = None):
        self._probas_threshold = probas_threshold
        self._quality = ClassificationQuality(
            probas_threshold=probas_threshold,
            conf_matrix=True,
            pr_curve=True,
            pr_table=True,
        )
        self._quality_by_label = ClassificationQualityByLabel(probas_threshold=probas_threshold)
        self._roc_auc: Optional[RocAuc] = None

    def generate_metrics(self, context: "Context") -> List[Metric]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        if classification.prediction_probas is not None:
            self._roc_auc = RocAuc()
        return (
            self._quality.metrics(context)
            + self._quality_by_label.metrics(context)
            + ([] if self._roc_auc is None else [RocAuc(probas_threshold=self._probas_threshold)])
        )

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        return (
            self._quality.render(context, results)
            + self._quality_by_label.render(context, results)
            + ([] if self._roc_auc is None else context.get_metric_result(self._roc_auc).widget)
        )
