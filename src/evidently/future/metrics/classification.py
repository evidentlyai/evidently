import abc
from typing import Generic
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from evidently.future.metric_types import ByLabelCalculation
from evidently.future.metric_types import ByLabelMetric
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueCalculation
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.report import Context
from evidently.metric_results import Label
from evidently.metrics import ClassificationDummyMetric
from evidently.metrics import ClassificationQualityByClass as _ClassificationQualityByClass
from evidently.metrics.classification_performance.classification_dummy_metric import ClassificationDummyMetricResults
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetric
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetricResult
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClassResult
from evidently.model.widget import BaseWidgetInfo


class ClassificationQualityByLabel(ByLabelMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class ClassificationQuality(SingleValueMetric):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


TByLabelMetric = TypeVar("TByLabelMetric", bound=ClassificationQualityByLabel)
TSingleValueMetric = TypeVar("TSingleValueMetric", bound=ClassificationQuality)


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

    def _relabel(self, context: "Context", label: Label):
        classification = context.data_definition.get_classification("default")
        if classification is None:
            return label
        labels = classification.labels
        if labels is not None:
            return labels[label]
        return label


class F1ByLabel(ClassificationQualityByLabel):
    pass


class F1ByLabelCalculation(LegacyClassificationQualityByClass[F1ByLabel]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[ByLabelValue, Optional[ByLabelValue]]:
        return (
            ByLabelValue({self._relabel(context, k): v.f1 for k, v in legacy_result.current.metrics.items()}),
            None
            if legacy_result.reference is None
            else ByLabelValue({self._relabel(context, k): v.f1 for k, v in legacy_result.reference.metrics.items()}),
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
        return (
            ByLabelValue({self._relabel(context, k): v.precision for k, v in legacy_result.current.metrics.items()}),
            None
            if legacy_result.reference is None
            else ByLabelValue(
                {self._relabel(context, k): v.precision for k, v in legacy_result.reference.metrics.items()}
            ),
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
        return (
            ByLabelValue({self._relabel(context, k): v.recall for k, v in legacy_result.current.metrics.items()}),
            None
            if legacy_result.reference is None
            else ByLabelValue(
                {self._relabel(context, k): v.recall for k, v in legacy_result.reference.metrics.items()}
            ),
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
        value = ByLabelValue(
            {self._relabel(context, k): v.roc_auc for k, v in legacy_result.current.metrics.items()},
        )
        value.widget = render
        value.widget[0].params["counters"][0]["label"] = self.display_name()
        return (
            value,
            None
            if legacy_result.reference is None
            else ByLabelValue(
                {self._relabel(context, k): v.roc_auc for k, v in legacy_result.reference.metrics.items()}
            ),
        )

    def display_name(self) -> str:
        return "ROC AUC by Label metric"


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
    ) -> Union[SingleValue, Tuple[SingleValue, Optional[SingleValue]]]:
        raise NotImplementedError()


class F1Score(ClassificationQuality):
    pass


class F1ScoreCalculation(LegacyClassificationQuality[F1Score]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            SingleValue(legacy_result.current.f1),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.f1),
        )

    def display_name(self) -> str:
        return "F1 score metric"


class Accuracy(ClassificationQuality):
    pass


class AccuracyCalculation(LegacyClassificationQuality[Accuracy]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            SingleValue(legacy_result.current.accuracy),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.accuracy),
        )

    def display_name(self) -> str:
        return "Accuracy metric"


class Precision(ClassificationQuality):
    pass


class PrecisionCalculation(LegacyClassificationQuality[Precision]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            SingleValue(legacy_result.current.precision),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.precision),
        )

    def display_name(self) -> str:
        return "Precision metric"


class Recall(ClassificationQuality):
    pass


class RecallCalculation(LegacyClassificationQuality[Recall]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        return (
            SingleValue(legacy_result.current.recall),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.recall),
        )

    def display_name(self) -> str:
        return "Recall metric"


class TPR(ClassificationQuality):
    pass


class TPRCalculation(LegacyClassificationQuality[TPR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.tpr is None:
            raise ValueError("Failed to calculate TPR value")
        return (
            SingleValue(legacy_result.current.tpr),
            None
            if legacy_result.reference is None or legacy_result.reference.tpr is None
            else SingleValue(legacy_result.reference.tpr),
        )

    def display_name(self) -> str:
        return "TPR metric"


class TNR(ClassificationQuality):
    pass


class TNRCalculation(LegacyClassificationQuality[TNR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.tnr is None:
            raise ValueError("Failed to calculate TNR value")
        return (
            SingleValue(legacy_result.current.tnr),
            None
            if legacy_result.reference is None or legacy_result.reference.tnr is None
            else SingleValue(legacy_result.reference.tnr),
        )

    def display_name(self) -> str:
        return "TNR metric"


class FPR(ClassificationQuality):
    pass


class FPRCalculation(LegacyClassificationQuality[FPR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.fpr is None:
            raise ValueError("Failed to calculate FPR value")
        return (
            SingleValue(legacy_result.current.fpr),
            None
            if legacy_result.reference is None or legacy_result.reference.fpr is None
            else SingleValue(legacy_result.reference.fpr),
        )

    def display_name(self) -> str:
        return "FPR metric"


class FNR(ClassificationQuality):
    pass


class FNRCalculation(LegacyClassificationQuality[FNR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.fnr is None:
            raise ValueError("Failed to calculate FNR value")
        return (
            SingleValue(legacy_result.current.fnr),
            None
            if legacy_result.reference is None or legacy_result.reference.fnr is None
            else SingleValue(legacy_result.reference.fnr),
        )

    def display_name(self) -> str:
        return "FNR metric"


class RocAuc(ClassificationQuality):
    pass


class RocAucCalculation(LegacyClassificationQuality[RocAuc]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.roc_auc is None:
            raise ValueError("Failed to calculate RocAuc value")
        return (
            SingleValue(legacy_result.current.roc_auc),
            None
            if legacy_result.reference is None or legacy_result.reference.roc_auc is None
            else SingleValue(legacy_result.reference.roc_auc),
        )

    def display_name(self) -> str:
        return "RocAuc metric"


class LogLoss(ClassificationQuality):
    pass


class LogLossCalculation(LegacyClassificationQuality[LogLoss]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> Tuple[SingleValue, Optional[SingleValue]]:
        if legacy_result.current.log_loss is None:
            raise ValueError("Failed to calculate LogLoss value")
        return (
            SingleValue(legacy_result.current.log_loss),
            None
            if legacy_result.reference is None or legacy_result.reference.log_loss is None
            else SingleValue(legacy_result.reference.log_loss),
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
    Generic[TSingleValueMetric],
    abc.ABC,
):
    _legacy_metric = None

    def legacy_metric(self) -> ClassificationDummyMetric:
        if self._legacy_metric is None:
            self._legacy_metric = ClassificationDummyMetric(self.metric.probas_threshold, self.metric.k)
        return self._legacy_metric

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationDummyMetricResults,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        raise NotImplementedError()


class DummyPrecision(ClassificationQuality):
    pass


class DummyPrecisionCalculation(LegacyClassificationDummy[DummyPrecision]):
    def calculate_value(
        self, context: "Context", legacy_result: ClassificationDummyMetricResults, render: List[BaseWidgetInfo]
    ) -> SingleValue:
        return SingleValue(legacy_result.dummy.precision)

    def display_name(self) -> str:
        return "Dummy precision metric"


class DummyRecall(ClassificationQuality):
    pass


class DummyRecallCalculation(LegacyClassificationDummy[DummyRecall]):
    def calculate_value(
        self, context: "Context", legacy_result: ClassificationDummyMetricResults, render: List[BaseWidgetInfo]
    ) -> SingleValue:
        return SingleValue(legacy_result.dummy.recall)

    def display_name(self) -> str:
        return "Dummy recall metric"


class DummyF1Score(ClassificationQuality):
    pass


class DummyF1ScoreCalculation(LegacyClassificationDummy[DummyF1Score]):
    def calculate_value(
        self, context: "Context", legacy_result: ClassificationDummyMetricResults, render: List[BaseWidgetInfo]
    ) -> SingleValue:
        return SingleValue(legacy_result.dummy.f1)

    def display_name(self) -> str:
        return "Dummy F1 score metric"
