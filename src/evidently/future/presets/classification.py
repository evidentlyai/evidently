from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.datasets import BinaryClassification
from evidently.future.metric_types import ByLabelMetricTests
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import SingleValueMetricTests
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
        accuracy_tests: SingleValueMetricTests = None,
        precision_tests: SingleValueMetricTests = None,
        recall_tests: SingleValueMetricTests = None,
        f1score_tests: SingleValueMetricTests = None,
        rocauc_tests: SingleValueMetricTests = None,
        logloss_tests: SingleValueMetricTests = None,
        tpr_tests: SingleValueMetricTests = None,
        tnr_tests: SingleValueMetricTests = None,
        fpr_tests: SingleValueMetricTests = None,
        fnr_tests: SingleValueMetricTests = None,
    ):
        self._accuracy_tests = accuracy_tests
        self._precision_tests = precision_tests
        self._recall_tests = recall_tests
        self._f1score_tests = f1score_tests
        self._rocauc_test = rocauc_tests
        self._logloss_test = logloss_tests
        self._tpr_test = tpr_tests
        self._tnr_test = tnr_tests
        self._fpr_test = fpr_tests
        self._fnr_test = fnr_tests
        self._probas_threshold = probas_threshold
        self._conf_matrix = conf_matrix
        self._pr_curve = pr_curve
        self._pr_table = pr_table

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationQuality without a classification data")

        metrics: List[Metric]

        metrics = [
            Accuracy(probas_threshold=self._probas_threshold, tests=self._accuracy_tests),
            Precision(probas_threshold=self._probas_threshold, tests=self._precision_tests),
            Recall(probas_threshold=self._probas_threshold, tests=self._recall_tests),
            F1Score(probas_threshold=self._probas_threshold, tests=self._f1score_tests),
        ]
        if classification.prediction_probas is not None:
            metrics.extend(
                [
                    RocAuc(probas_threshold=self._probas_threshold, tests=self._rocauc_test),
                    LogLoss(probas_threshold=self._probas_threshold, tests=self._logloss_test),
                ]
            )
        if isinstance(classification, BinaryClassification):
            metrics.extend(
                [
                    TPR(probas_threshold=self._probas_threshold, tests=self._tpr_test),
                    TNR(probas_threshold=self._probas_threshold, tests=self._tnr_test),
                    FPR(probas_threshold=self._probas_threshold, tests=self._fpr_test),
                    FNR(probas_threshold=self._probas_threshold, tests=self._fnr_test),
                ]
            )
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
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
        for metric in self.list_metrics(context):
            link_metric(render, metric)
        return render


class ClassificationQualityByLabel(MetricContainer):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        f1score_tests: ByLabelMetricTests = None,
        precision_tests: ByLabelMetricTests = None,
        recall_tests: ByLabelMetricTests = None,
        rocauc_tests: ByLabelMetricTests = None,
    ):
        self._probas_threshold = probas_threshold
        self._k = k
        self._f1score_tests = f1score_tests
        self._precision_tests = precision_tests
        self._recall_tests = recall_tests
        self._rocauc_tests = rocauc_tests

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        return [
            F1ByLabel(probas_threshold=self._probas_threshold, k=self._k, tests=self._f1score_tests),
            PrecisionByLabel(probas_threshold=self._probas_threshold, k=self._k, tests=self._precision_tests),
            RecallByLabel(probas_threshold=self._probas_threshold, k=self._k, tests=self._recall_tests),
        ] + (
            []
            if classification.prediction_probas is None
            else [
                RocAucByLabel(probas_threshold=self._probas_threshold, k=self._k, tests=self._rocauc_tests),
            ]
        )

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        render = context.get_legacy_metric(
            ClassificationQualityByClass(self._probas_threshold, self._k),
            _gen_classification_input_data,
        )[1]
        widget = render
        widget[0].params["counters"][0]["label"] = "Classification Quality by Label"
        for metric in self.list_metrics(context):
            link_metric(widget, metric)
        return widget


class ClassificationDummyQuality(MetricContainer):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
    ):
        self._probas_threshold = probas_threshold
        self._k = k

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        return [
            DummyPrecision(),
            DummyRecall(),
            DummyF1Score(),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        _, widgets = context.get_legacy_metric(
            ClassificationDummyMetric(self._probas_threshold, self._k),
            _gen_classification_input_data,
        )
        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class ClassificationPreset(MetricContainer):
    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        accuracy_tests: SingleValueMetricTests = None,
        precision_tests: SingleValueMetricTests = None,
        recall_tests: SingleValueMetricTests = None,
        f1score_tests: SingleValueMetricTests = None,
        rocauc_tests: SingleValueMetricTests = None,
        logloss_tests: SingleValueMetricTests = None,
        tpr_tests: SingleValueMetricTests = None,
        tnr_tests: SingleValueMetricTests = None,
        fpr_tests: SingleValueMetricTests = None,
        fnr_tests: SingleValueMetricTests = None,
        f1score_by_label_tests: ByLabelMetricTests = None,
        precision_by_label_tests: ByLabelMetricTests = None,
        recall_by_label_tests: ByLabelMetricTests = None,
        rocauc_by_label_tests: ByLabelMetricTests = None,
    ):
        self._probas_threshold = probas_threshold
        self._quality = ClassificationQuality(
            probas_threshold=probas_threshold,
            conf_matrix=True,
            pr_curve=True,
            pr_table=True,
            accuracy_tests=accuracy_tests,
            precision_tests=precision_tests,
            recall_tests=recall_tests,
            f1score_tests=f1score_tests,
            rocauc_tests=rocauc_tests,
            logloss_tests=logloss_tests,
            tpr_tests=tpr_tests,
            tnr_tests=tnr_tests,
            fpr_tests=fpr_tests,
            fnr_tests=fnr_tests,
        )
        self._quality_by_label = ClassificationQualityByLabel(
            probas_threshold=probas_threshold,
            f1score_tests=f1score_by_label_tests,
            precision_tests=precision_by_label_tests,
            recall_tests=recall_by_label_tests,
            rocauc_tests=rocauc_by_label_tests,
        )
        self._roc_auc: Optional[RocAuc] = RocAuc(
            probas_threshold=probas_threshold,
            tests=rocauc_tests,
        )

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        if classification.prediction_probas is None:
            self._roc_auc = None
        return (
            self._quality.metrics(context)
            + self._quality_by_label.metrics(context)
            + ([] if self._roc_auc is None else [RocAuc(probas_threshold=self._probas_threshold)])
        )

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return (
            self._quality.render(context)
            + self._quality_by_label.render(context)
            + ([] if self._roc_auc is None else context.get_metric_result(self._roc_auc).widget)
        )
