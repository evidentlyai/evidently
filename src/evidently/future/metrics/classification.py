import abc
from typing import Dict
from typing import Generator
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.future.datasets import Dataset
from evidently.future.metric_types import ByLabelMetric
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.preset_types import MetricPreset
from evidently.future.preset_types import PresetResult
from evidently.future.report import Context
from evidently.metrics import ClassificationQualityByClass as _ClassificationQualityByClass
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

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        raise NotImplementedError()

    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityByClassResult,
        render: List[BaseWidgetInfo],
    ) -> ByLabelValue:
        raise NotImplementedError()

    def get_tests(self, value: ByLabelValue) -> Generator[MetricTestResult, None, None]:
        for label, tests in self.metric.tests.items():
            label_value = value.get_label_result(label)
            for test in tests:
                yield test.to_test()(self, label_value)


class F1ByLabel(ClassificationQualityByLabel):
    pass


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


class PrecisionByLabel(ClassificationQualityByLabel):
    pass


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


class RecallByLabel(ClassificationQualityByLabel):
    pass


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


class RocAucByLabel(ClassificationQualityByLabel):
    pass


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


class LegacyClassificationQuality(
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

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        raise NotImplementedError()

    def get_tests(self, value: SingleValue) -> Generator[MetricTestResult, None, None]:
        yield from (t.to_test()(self, value) for t in self.metric.tests)


class F1Score(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class F1ScoreCalculation(LegacyClassificationQuality[F1Score]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.f1)

    def display_name(self) -> str:
        return "F1 score metric"


class Accuracy(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class AccuracyCalculation(LegacyClassificationQuality[Accuracy]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.accuracy)

    def display_name(self) -> str:
        return "Accuracy metric"


class Precision(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class PrecisionCalculation(LegacyClassificationQuality[Precision]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.precision)

    def display_name(self) -> str:
        return "Precision metric"


class Recall(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RecallCalculation(LegacyClassificationQuality[Recall]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.recall)

    def display_name(self) -> str:
        return "Recall metric"


class TPR(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class TPRCalculation(LegacyClassificationQuality[TPR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.tpr)

    def display_name(self) -> str:
        return "TPR metric"


class TNR(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class TNRCalculation(LegacyClassificationQuality[TNR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.tnr)

    def display_name(self) -> str:
        return "TNR metric"


class FPR(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class FPRCalculation(LegacyClassificationQuality[FPR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.fpr)

    def display_name(self) -> str:
        return "FPR metric"


class FNR(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class FNRCalculation(LegacyClassificationQuality[FNR]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.fnr)

    def display_name(self) -> str:
        return "FNR metric"


class RocAuc(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class RocAucCalculation(LegacyClassificationQuality[RocAuc]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.roc_auc)

    def display_name(self) -> str:
        return "RocAuc metric"


class LogLoss(ClassificationQuality):
    probas_threshold: Optional[float] = None
    k: Optional[int] = None


class LogLossCalculation(LegacyClassificationQuality[LogLoss]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: ClassificationQualityMetricResult,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        return SingleValue(legacy_result.current.log_loss)

    def display_name(self) -> str:
        return "LogLoss metric"
