import abc
from typing import ClassVar
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar

from evidently.core.base_types import Label
from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import ByLabelCalculation
from evidently.core.metric_types import ByLabelMetric
from evidently.core.metric_types import ByLabelValue
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TMetricResult
from evidently.core.report import Context
from evidently.core.report import _default_input_data_generator
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.metrics import ClassificationConfusionMatrix
from evidently.legacy.metrics import ClassificationDummyMetric
from evidently.legacy.metrics import ClassificationLiftCurve
from evidently.legacy.metrics import ClassificationLiftTable
from evidently.legacy.metrics import ClassificationPRCurve
from evidently.legacy.metrics import ClassificationProbDistribution
from evidently.legacy.metrics import ClassificationPRTable
from evidently.legacy.metrics import ClassificationQualityByClass as _ClassificationQualityByClass
from evidently.legacy.metrics import ClassificationRocCurve
from evidently.legacy.metrics.classification_performance.classification_dummy_metric import (
    ClassificationDummyMetricResults,
)
from evidently.legacy.metrics.classification_performance.classification_quality_metric import (
    ClassificationQualityMetric,
)
from evidently.legacy.metrics.classification_performance.classification_quality_metric import (
    ClassificationQualityMetricResult,
)
from evidently.legacy.metrics.classification_performance.quality_by_class_metric import (
    ClassificationQualityByClassResult,
)
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.metrics._legacy import LegacyMetricCalculation
from evidently.tests import Reference
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import lt


class ClassificationQualityByLabel(ByLabelMetric):
    classification_name: str = "default"
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class ClassificationQualityBase(SingleValueMetric):
    classification_name: str = "default"
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class ClassificationQuality(ClassificationQualityBase):
    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.2)).bind_single(self.get_fingerprint())]

    def _get_dummy_value(
        self, context: Context, dummy_type: Type["DummyClassificationQuality"], **kwargs
    ) -> SingleValue:
        return context.calculate_metric(
            dummy_type(probas_threshold=self.probas_threshold, k=self.k, **kwargs).to_calculation()
        )


TByLabelMetric = TypeVar("TByLabelMetric", bound=ClassificationQualityByLabel)
TSingleValueMetric = TypeVar("TSingleValueMetric", bound=ClassificationQualityBase)


def _gen_classification_input_data(context: "Context", task_name: Optional[str]) -> InputData:
    default_input_data = _default_input_data_generator(context, task_name)
    return default_input_data


class LegacyClassificationQualityByClass(
    ByLabelCalculation[TByLabelMetric],
    LegacyMetricCalculation[
        ByLabelValue,
        TByLabelMetric,
        ClassificationQualityByClassResult,
        _ClassificationQualityByClass,
    ],
    Generic[TByLabelMetric],
    abc.ABC,
):
    _legacy_metric = None

    def task_name(self) -> str:
        return self.metric.classification_name

    def legacy_metric(self) -> _ClassificationQualityByClass:
        if self._legacy_metric is None:
            self._legacy_metric = _ClassificationQualityByClass(self.metric.probas_threshold, self.metric.k)
        return self._legacy_metric

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ):
        raise NotImplementedError()

    def _relabel(self, context: "Context", label: Label) -> Label:
        classification = context.data_definition.get_classification("default")
        if classification is None:
            return label
        actual_labels = context.get_labels(classification.target, classification.prediction_labels)
        _label = None
        for actual_label in actual_labels:
            if label == actual_label:
                _label = label
                break
            if label == str(actual_label):
                _label = actual_label
                break
        if _label is None:
            raise ValueError(f"Failed to relabel {label}")
        labels = classification.labels
        if labels is not None:
            return labels[_label]
        return _label

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, self._gen_input_data, self.task_name())
                result += widgets
        return result


class F1ByLabel(ClassificationQualityByLabel):
    pass


class F1ByLabelCalculation(LegacyClassificationQualityByClass[F1ByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[ByLabelValue, Optional[ByLabelValue]]:
        return self.collect_by_label_result(
            context,
            lambda x: x.f1,
            legacy_result.current.metrics,
            None if legacy_result.reference is None else legacy_result.reference.metrics,
        )

    def display_name(self) -> str:
        return "F1 by Label metric"


class PrecisionByLabel(ClassificationQualityByLabel):
    pass


class PrecisionByLabelCalculation(LegacyClassificationQualityByClass[PrecisionByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[ByLabelValue, Optional[ByLabelValue]]:
        return self.collect_by_label_result(
            context,
            lambda x: x.precision,
            legacy_result.current.metrics,
            None if legacy_result.reference is None else legacy_result.reference.metrics,
        )

    def display_name(self) -> str:
        return "Precision by Label metric"


class RecallByLabel(ClassificationQualityByLabel):
    pass


class RecallByLabelCalculation(LegacyClassificationQualityByClass[RecallByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[ByLabelValue, Optional[ByLabelValue]]:
        return self.collect_by_label_result(
            context,
            lambda x: x.recall,
            legacy_result.current.metrics,
            None if legacy_result.reference is None else legacy_result.reference.metrics,
        )

    def display_name(self) -> str:
        return "Recall by Label metric"


class RocAucByLabel(ClassificationQualityByLabel):
    pass


class RocAucByLabelCalculation(LegacyClassificationQualityByClass[RocAucByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[ByLabelValue, Optional[ByLabelValue]]:
        return self.collect_by_label_result(
            context,
            lambda x: x.roc_auc if x.roc_auc is not None else 0.0,
            legacy_result.current.metrics,
            None if legacy_result.reference is None else legacy_result.reference.metrics,
        )

    def display_name(self) -> str:
        return "ROC AUC by Label metric"


ADDITIONAL_WIDGET_MAPPING: Dict[str, Metric] = {
    "prob_distribution": ClassificationProbDistribution(),
    "conf_matrix": ClassificationConfusionMatrix(),
    "pr_curve": ClassificationPRCurve(),
    "pr_table": ClassificationPRTable(),
    "roc_curve": ClassificationRocCurve(),
    "lift_curve": ClassificationLiftCurve(),
    "lift_table": ClassificationLiftTable(),
}


class LegacyClassificationQuality(
    SingleValueCalculation[TSingleValueMetric],
    LegacyMetricCalculation[
        SingleValue,
        TSingleValueMetric,
        ClassificationQualityMetricResult,
        ClassificationQualityMetric,
    ],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    _legacy_metric = None

    def legacy_metric(self) -> ClassificationQualityMetric:
        if self._legacy_metric is None:
            self._legacy_metric = ClassificationQualityMetric(self.metric.probas_threshold, self.metric.k)
        return self._legacy_metric

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        raise NotImplementedError()

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, self._gen_input_data, self.task_name())
                result += widgets
        return result


class F1Score(ClassificationQuality):
    conf_matrix: bool = True

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyF1Score)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class F1ScoreCalculation(LegacyClassificationQuality[F1Score]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            self.result(legacy_result.current.f1),
            None if legacy_result.reference is None else self.result(legacy_result.reference.f1),
        )

    def display_name(self) -> str:
        return "F1 score metric"


class Accuracy(ClassificationQuality):
    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyAccuracy)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class AccuracyCalculation(LegacyClassificationQuality[Accuracy]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            self.result(legacy_result.current.accuracy),
            None if legacy_result.reference is None else self.result(legacy_result.reference.accuracy),
        )

    def display_name(self) -> str:
        return "Accuracy metric"


class Precision(ClassificationQuality):
    conf_matrix: bool = True
    pr_curve: bool = False
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyPrecision)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class PrecisionCalculation(LegacyClassificationQuality[Precision]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            self.result(legacy_result.current.precision),
            None if legacy_result.reference is None else self.result(legacy_result.reference.precision),
        )

    def display_name(self) -> str:
        return "Precision metric"


class Recall(ClassificationQuality):
    conf_matrix: bool = True
    pr_curve: bool = False
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyRecall)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class RecallCalculation(LegacyClassificationQuality[Recall]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            self.result(legacy_result.current.recall),
            None if legacy_result.reference is None else self.result(legacy_result.reference.recall),
        )

    def display_name(self) -> str:
        return "Recall metric"


class TPR(ClassificationQuality):
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyTPR)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class TPRCalculation(LegacyClassificationQuality[TPR]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.tpr is None:
            raise ValueError(
                "Cannot compute TPR: current TPR value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.tpr),
            None
            if legacy_result.reference is None or legacy_result.reference.tpr is None
            else self.result(legacy_result.reference.tpr),
        )

    def display_name(self) -> str:
        return "TPR metric"


class TNR(ClassificationQuality):
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyTNR)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class TNRCalculation(LegacyClassificationQuality[TNR]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.tnr is None:
            raise ValueError(
                "Cannot compute TNR: current TNR value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.tnr),
            None
            if legacy_result.reference is None or legacy_result.reference.tnr is None
            else self.result(legacy_result.reference.tnr),
        )

    def display_name(self) -> str:
        return "TNR metric"


class FPR(ClassificationQuality):
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyFPR)
        return [lt(dummy_value.value).bind_single(self.get_fingerprint())]


class FPRCalculation(LegacyClassificationQuality[FPR]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.fpr is None:
            raise ValueError(
                "Cannot compute FPR: current FPR value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.fpr),
            None
            if legacy_result.reference is None or legacy_result.reference.fpr is None
            else self.result(legacy_result.reference.fpr),
        )

    def display_name(self) -> str:
        return "FPR metric"


class FNR(ClassificationQuality):
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyFNR)
        return [lt(dummy_value.value).bind_single(self.get_fingerprint())]


class FNRCalculation(LegacyClassificationQuality[FNR]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.fnr is None:
            raise ValueError(
                "Cannot compute FNR: current FNR value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.fnr),
            None
            if legacy_result.reference is None or legacy_result.reference.fnr is None
            else self.result(legacy_result.reference.fnr),
        )

    def display_name(self) -> str:
        return "FNR metric"


class RocAuc(ClassificationQuality):
    roc_curve: bool = True
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyRocAuc)
        return [gt(dummy_value.value).bind_single(self.get_fingerprint())]


class RocAucCalculation(LegacyClassificationQuality[RocAuc]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.roc_auc is None:
            raise ValueError(
                "Cannot compute RocAuc: current RocAuc value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.roc_auc),
            None
            if legacy_result.reference is None or legacy_result.reference.roc_auc is None
            else self.result(legacy_result.reference.roc_auc),
        )

    def display_name(self) -> str:
        return "RocAuc metric"


class LogLoss(ClassificationQuality):
    pr_table: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        dummy_value = self._get_dummy_value(context, DummyLogLoss)
        return [lt(dummy_value.value).bind_single(self.get_fingerprint())]


class LogLossCalculation(LegacyClassificationQuality[LogLoss]):
    def task_name(self) -> str:
        return self.metric.classification_name

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.log_loss is None:
            raise ValueError(
                "Cannot compute LogLoss: current LogLoss value is missing. "
                "Ensure prediction labels and probabilities are available. "
            )
        return (
            self.result(legacy_result.current.log_loss),
            None
            if legacy_result.reference is None or legacy_result.reference.log_loss is None
            else self.result(legacy_result.reference.log_loss),
        )

    def display_name(self) -> str:
        return "LogLoss metric"


class LegacyClassificationDummy(
    LegacyMetricCalculation[
        SingleValue,
        TSingleValueMetric,
        ClassificationDummyMetricResults,
        ClassificationDummyMetric,
    ],
    SingleValueCalculation[TSingleValueMetric],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    _legacy_metric = None
    __legacy_field_name__: ClassVar[str]

    def task_name(self) -> str:
        return self.metric.classification_name

    def legacy_metric(self) -> ClassificationDummyMetric:
        if self._legacy_metric is None:
            self._legacy_metric = ClassificationDummyMetric(self.metric.probas_threshold, self.metric.k)
        return self._legacy_metric

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationDummyMetricResults,
        render: List[BaseWidgetInfo],
    ) -> TMetricResult:
        current_value = getattr(legacy_result.dummy, self.__legacy_field_name__)
        if current_value is None:
            raise ValueError(f"Failed to calculate {self.display_name()}")
        if legacy_result.by_reference_dummy is None:
            return self.result(current_value)
        reference_value = getattr(legacy_result.by_reference_dummy, self.__legacy_field_name__)
        return self.result(current_value), self.result(reference_value)


class DummyClassificationQuality(ClassificationQualityBase):
    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return []

    def _default_tests(self, context: Context) -> List[BoundTest]:
        return []


class DummyPrecision(DummyClassificationQuality):
    pass


class DummyPrecisionCalculation(LegacyClassificationDummy[DummyPrecision]):
    def task_name(self) -> str:
        return self.metric.classification_name

    __legacy_field_name__ = "precision"

    def display_name(self) -> str:
        return "Dummy precision metric"


class DummyRecall(DummyClassificationQuality):
    pass


class DummyRecallCalculation(LegacyClassificationDummy[DummyRecall]):
    __legacy_field_name__ = "recall"

    def display_name(self) -> str:
        return "Dummy recall metric"


class DummyF1Score(DummyClassificationQuality):
    pass


class DummyF1ScoreCalculation(LegacyClassificationDummy[DummyF1Score]):
    __legacy_field_name__ = "f1"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy F1 score metric"


class DummyAccuracy(DummyClassificationQuality):
    pass


class DummyAccuracyCalculation(LegacyClassificationDummy[DummyAccuracy]):
    __legacy_field_name__ = "accuracy"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy accuracy metric"


class DummyTPR(DummyClassificationQuality):
    pass


class DummyTPRCalculation(LegacyClassificationDummy[DummyTPR]):
    __legacy_field_name__ = "tpr"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy TPR metric"


class DummyTNR(DummyClassificationQuality):
    pass


class DummyTNRCalculation(LegacyClassificationDummy[DummyTNR]):
    __legacy_field_name__ = "tnr"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy TNR metric"


class DummyFPR(DummyClassificationQuality):
    pass


class DummyFPRCalculation(LegacyClassificationDummy[DummyFPR]):
    __legacy_field_name__ = "fpr"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy FPR metric"


class DummyFNR(DummyClassificationQuality):
    pass


class DummyFNRCalculation(LegacyClassificationDummy[DummyFNR]):
    __legacy_field_name__ = "fnr"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy FNR metric"


class DummyLogLoss(DummyClassificationQuality):
    pass


class DummyLogLossCalculation(LegacyClassificationDummy[DummyLogLoss]):
    __legacy_field_name__ = "log_loss"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy LogLoss metric"


class DummyRocAuc(DummyClassificationQuality):
    pass


class DummyRocAucCalculation(LegacyClassificationDummy[DummyRocAuc]):
    __legacy_field_name__ = "roc_auc"

    def task_name(self) -> str:
        return self.metric.classification_name

    def display_name(self) -> str:
        return "Dummy RocAuc metric"
