from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently._pydantic_compat import PrivateAttr
from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.datasets import BinaryClassification
from evidently.core.metric_types import ByLabelMetricTests
from evidently.core.metric_types import GenericByLabelMetricTests
from evidently.core.metric_types import GenericSingleValueMetricTests
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import SingleValueMetricTests
from evidently.core.metric_types import convert_tests
from evidently.core.report import Context
from evidently.legacy.metrics import ClassificationConfusionMatrix
from evidently.legacy.metrics import ClassificationDummyMetric
from evidently.legacy.metrics import ClassificationPRCurve
from evidently.legacy.metrics import ClassificationPRTable
from evidently.legacy.metrics import ClassificationQualityByClass
from evidently.legacy.metrics import ClassificationQualityMetric
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import link_metric
from evidently.metrics import FNR
from evidently.metrics import FPR
from evidently.metrics import TNR
from evidently.metrics import TPR
from evidently.metrics import Accuracy
from evidently.metrics import F1ByLabel
from evidently.metrics import F1Score
from evidently.metrics import LogLoss
from evidently.metrics import Precision
from evidently.metrics import PrecisionByLabel
from evidently.metrics import Recall
from evidently.metrics import RecallByLabel
from evidently.metrics import RocAuc
from evidently.metrics import RocAucByLabel
from evidently.metrics.classification import DummyF1Score
from evidently.metrics.classification import DummyPrecision
from evidently.metrics.classification import DummyRecall
from evidently.metrics.classification import _gen_classification_input_data


class ClassificationQuality(MetricContainer):
    classification_name: str = "default"
    probas_threshold: Optional[float] = None
    conf_matrix: bool = False
    pr_curve: bool = False
    pr_table: bool = False
    accuracy_tests: SingleValueMetricTests = None
    precision_tests: SingleValueMetricTests = None
    recall_tests: SingleValueMetricTests = None
    f1score_tests: SingleValueMetricTests = None
    rocauc_tests: SingleValueMetricTests = None
    logloss_tests: SingleValueMetricTests = None
    tpr_tests: SingleValueMetricTests = None
    tnr_tests: SingleValueMetricTests = None
    fpr_tests: SingleValueMetricTests = None
    fnr_tests: SingleValueMetricTests = None

    def __init__(
        self,
        classification_name: str = "default",
        probas_threshold: Optional[float] = None,
        conf_matrix: bool = False,
        pr_curve: bool = False,
        pr_table: bool = False,
        accuracy_tests: GenericSingleValueMetricTests = None,
        precision_tests: GenericSingleValueMetricTests = None,
        recall_tests: GenericSingleValueMetricTests = None,
        f1score_tests: GenericSingleValueMetricTests = None,
        rocauc_tests: GenericSingleValueMetricTests = None,
        logloss_tests: GenericSingleValueMetricTests = None,
        tpr_tests: GenericSingleValueMetricTests = None,
        tnr_tests: GenericSingleValueMetricTests = None,
        fpr_tests: GenericSingleValueMetricTests = None,
        fnr_tests: GenericSingleValueMetricTests = None,
        include_tests: bool = True,
    ):
        self.classification_name = classification_name
        self.accuracy_tests = convert_tests(accuracy_tests)
        self.precision_tests = convert_tests(precision_tests)
        self.recall_tests = convert_tests(recall_tests)
        self.f1score_tests = convert_tests(f1score_tests)
        self.rocauc_tests = convert_tests(rocauc_tests)
        self.logloss_tests = convert_tests(logloss_tests)
        self.tpr_tests = convert_tests(tpr_tests)
        self.tnr_tests = convert_tests(tnr_tests)
        self.fpr_tests = convert_tests(fpr_tests)
        self.fnr_tests = convert_tests(fnr_tests)
        self.probas_threshold = probas_threshold
        self.conf_matrix = conf_matrix
        self.pr_curve = pr_curve
        self.pr_table = pr_table
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification(self.classification_name)
        if classification is None:
            raise ValueError("Classification with name '{}' not found".format(self.classification_name))

        metrics: List[Metric]

        metrics = [
            Accuracy(
                probas_threshold=self.probas_threshold,
                classification_name=self.classification_name,
                tests=self._get_tests(self.accuracy_tests),
            ),
            Precision(
                probas_threshold=self.probas_threshold,
                classification_name=self.classification_name,
                tests=self._get_tests(self.precision_tests),
            ),
            Recall(
                probas_threshold=self.probas_threshold,
                classification_name=self.classification_name,
                tests=self._get_tests(self.recall_tests),
            ),
            F1Score(
                probas_threshold=self.probas_threshold,
                classification_name=self.classification_name,
                tests=self._get_tests(self.f1score_tests),
            ),
        ]
        if classification.prediction_probas is not None:
            metrics.extend(
                [
                    RocAuc(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.rocauc_tests),
                    ),
                    LogLoss(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.logloss_tests),
                    ),
                ]
            )
        if isinstance(classification, BinaryClassification):
            metrics.extend(
                [
                    TPR(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.tpr_tests),
                    ),
                    TNR(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.tnr_tests),
                    ),
                    FPR(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.fpr_tests),
                    ),
                    FNR(
                        probas_threshold=self.probas_threshold,
                        classification_name=self.classification_name,
                        tests=self._get_tests(self.fnr_tests),
                    ),
                ]
            )
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        _, render = context.get_legacy_metric(
            ClassificationQualityMetric(probas_threshold=self.probas_threshold),
            _gen_classification_input_data,
            self.classification_name,
        )
        if self.conf_matrix:
            render += context.get_legacy_metric(
                ClassificationConfusionMatrix(probas_threshold=self.probas_threshold),
                _gen_classification_input_data,
                self.classification_name,
            )[1]
        classification = context.data_definition.get_classification(self.classification_name)
        if classification is None:
            raise ValueError("Cannot use ClassificationQuality without a classification data")
        if self.pr_curve and classification.prediction_probas is not None:
            render += context.get_legacy_metric(
                ClassificationPRCurve(probas_threshold=self.probas_threshold),
                _gen_classification_input_data,
                self.classification_name,
            )[1]
        if self.pr_table and classification.prediction_probas is not None:
            render += context.get_legacy_metric(
                ClassificationPRTable(probas_threshold=self.probas_threshold),
                _gen_classification_input_data,
                self.classification_name,
            )[1]
        for metric in self.list_metrics(context):
            link_metric(render, metric)
        return render


class ClassificationQualityByLabel(MetricContainer):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None
    f1score_tests: ByLabelMetricTests = None
    precision_tests: ByLabelMetricTests = None
    recall_tests: ByLabelMetricTests = None
    rocauc_tests: ByLabelMetricTests = None
    classification_name: str = "default"

    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        f1score_tests: GenericByLabelMetricTests = None,
        precision_tests: GenericByLabelMetricTests = None,
        recall_tests: GenericByLabelMetricTests = None,
        rocauc_tests: GenericByLabelMetricTests = None,
        classification_name: str = "default",
        include_tests: bool = True,
    ):
        self.probas_threshold = probas_threshold
        self.k = k
        self.f1score_tests = convert_tests(f1score_tests)
        self.precision_tests = convert_tests(precision_tests)
        self.recall_tests = convert_tests(recall_tests)
        self.rocauc_tests = convert_tests(rocauc_tests)
        self.classification_name = classification_name
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification(self.classification_name)
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        return [
            F1ByLabel(
                classification_name=self.classification_name,
                probas_threshold=self.probas_threshold,
                k=self.k,
                tests=self._get_tests(self.f1score_tests),
            ),
            PrecisionByLabel(
                classification_name=self.classification_name,
                probas_threshold=self.probas_threshold,
                k=self.k,
                tests=self._get_tests(self.precision_tests),
            ),
            RecallByLabel(
                classification_name=self.classification_name,
                probas_threshold=self.probas_threshold,
                k=self.k,
                tests=self._get_tests(self.recall_tests),
            ),
        ] + (
            []
            if classification.prediction_probas is None
            else [
                RocAucByLabel(
                    classification_name=self.classification_name,
                    probas_threshold=self.probas_threshold,
                    k=self.k,
                    tests=self._get_tests(self.rocauc_tests),
                ),
            ]
        )

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        render = context.get_legacy_metric(
            ClassificationQualityByClass(self.probas_threshold, self.k),
            _gen_classification_input_data,
            self.classification_name,
        )[1]
        widget = render
        widget[0].params["counters"][0]["label"] = "Classification Quality by Label"
        for metric in self.list_metrics(context):
            link_metric(widget, metric)
        return widget


class ClassificationDummyQuality(MetricContainer):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None
    classification_name: str = "default"

    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        k: Optional[int] = None,
        include_tests: bool = True,
        classification_name: str = "default",
    ):
        self.probas_threshold = probas_threshold
        self.k = k
        self.classification_name = classification_name
        super().__init__(include_tests=include_tests)

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
            ClassificationDummyMetric(self.probas_threshold, self.k),
            _gen_classification_input_data,
            self.classification_name,
        )
        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class ClassificationPreset(MetricContainer):
    probas_threshold: Optional[float] = None
    accuracy_tests: SingleValueMetricTests = None
    precision_tests: SingleValueMetricTests = None
    recall_tests: SingleValueMetricTests = None
    f1score_tests: SingleValueMetricTests = None
    rocauc_tests: SingleValueMetricTests = None
    logloss_tests: SingleValueMetricTests = None
    tpr_tests: SingleValueMetricTests = None
    tnr_tests: SingleValueMetricTests = None
    fpr_tests: SingleValueMetricTests = None
    fnr_tests: SingleValueMetricTests = None
    f1score_by_label_tests: ByLabelMetricTests = None
    precision_by_label_tests: ByLabelMetricTests = None
    recall_by_label_tests: ByLabelMetricTests = None
    rocauc_by_label_tests: ByLabelMetricTests = None
    classification_name: str = "default"

    _quality: ClassificationQuality = PrivateAttr()
    _quality_by_label: ClassificationQualityByLabel = PrivateAttr()
    _roc_auc: Optional[RocAuc] = PrivateAttr()

    def __init__(
        self,
        probas_threshold: Optional[float] = None,
        accuracy_tests: GenericSingleValueMetricTests = None,
        precision_tests: GenericSingleValueMetricTests = None,
        recall_tests: GenericSingleValueMetricTests = None,
        f1score_tests: GenericSingleValueMetricTests = None,
        rocauc_tests: GenericSingleValueMetricTests = None,
        logloss_tests: GenericSingleValueMetricTests = None,
        tpr_tests: GenericSingleValueMetricTests = None,
        tnr_tests: GenericSingleValueMetricTests = None,
        fpr_tests: GenericSingleValueMetricTests = None,
        fnr_tests: GenericSingleValueMetricTests = None,
        f1score_by_label_tests: GenericByLabelMetricTests = None,
        precision_by_label_tests: GenericByLabelMetricTests = None,
        recall_by_label_tests: GenericByLabelMetricTests = None,
        rocauc_by_label_tests: GenericByLabelMetricTests = None,
        include_tests: bool = True,
        classification_name: str = "default",
    ):
        super().__init__(
            include_tests=include_tests,
            probas_threshold=probas_threshold,
            accuracy_tests=convert_tests(accuracy_tests),
            precision_tests=convert_tests(precision_tests),
            recall_tests=convert_tests(recall_tests),
            f1score_tests=convert_tests(f1score_tests),
            rocauc_tests=convert_tests(rocauc_tests),
            logloss_tests=convert_tests(logloss_tests),
            tpr_tests=convert_tests(tpr_tests),
            tnr_tests=convert_tests(tnr_tests),
            fpr_tests=convert_tests(fpr_tests),
            fnr_tests=convert_tests(fnr_tests),
            f1score_by_label_tests=convert_tests(f1score_by_label_tests),
            precision_by_label_tests=convert_tests(precision_by_label_tests),
            recall_by_label_tests=convert_tests(recall_by_label_tests),
            rocauc_by_label_tests=convert_tests(rocauc_by_label_tests),
            classification_name=classification_name,
        )
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
            include_tests=include_tests,
            classification_name=classification_name,
        )
        self._quality_by_label = ClassificationQualityByLabel(
            probas_threshold=probas_threshold,
            f1score_tests=f1score_by_label_tests,
            precision_tests=precision_by_label_tests,
            recall_tests=recall_by_label_tests,
            rocauc_tests=rocauc_by_label_tests,
            include_tests=include_tests,
            classification_name=classification_name,
        )
        self._roc_auc = None

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        classification = context.data_definition.get_classification(self.classification_name)
        if classification is None:
            raise ValueError("Cannot use ClassificationPreset without a classification configration")
        quality_metrics = self._quality.metrics(context)
        self._roc_auc = next((m for m in quality_metrics if isinstance(m, RocAuc)), None)
        return quality_metrics + self._quality_by_label.metrics(context)

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return (
            self._quality.render(context)
            + self._quality_by_label.render(context)
            + ([] if self._roc_auc is None else context.get_metric_result(self._roc_auc).get_widgets())
        )
