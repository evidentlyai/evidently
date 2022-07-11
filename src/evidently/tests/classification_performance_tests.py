import abc
from typing import Optional, List, Union, Any

from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetrics
from evidently.metrics.classification_performance_metrics import DatasetClassificationPerformanceMetrics
from evidently.tests.base_test import BaseCheckValueTest, TestValueCondition
from evidently.tests.utils import Numeric, approx


class SimpleClassificationTest(BaseCheckValueTest):
    group = "classification"
    name: str
    metric: ClassificationPerformanceMetrics

    def __init__(
            self,
            eq: Optional[Numeric] = None,
            gt: Optional[Numeric] = None,
            gte: Optional[Numeric] = None,
            is_in: Optional[List[Union[Numeric, str, bool]]] = None,
            lt: Optional[Numeric] = None,
            lte: Optional[Numeric] = None,
            not_eq: Optional[Numeric] = None,
            not_in: Optional[List[Union[Numeric, str, bool]]] = None,
            metric: Optional[ClassificationPerformanceMetrics] = None
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)
        if metric is None:
            metric = ClassificationPerformanceMetrics()
        self.metric = metric

    def calculate_value_for_test(self) -> Optional[Any]:
        return self.get_value(self.metric.get_result().current_metrics)

    def get_condition(self) -> TestValueCondition:
        if self.condition.is_set():
            return self.condition
        ref_metrics = self.metric.get_result().reference_metrics
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics)))
        return TestValueCondition(gt=self.get_value(self.metric.get_result().dummy_metrics))

    @abc.abstractmethod
    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        raise NotImplementedError()


class TestAccuracyScore(SimpleClassificationTest):
    name = "Accuracy Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.accuracy

    def get_description(self, value: Numeric) -> str:
        return f"Accuracy Score is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestPrecisionScore(SimpleClassificationTest):
    name = "Precision Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.precision

    def get_description(self, value: Numeric) -> str:
        return f"Precision Score is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestF1Score(SimpleClassificationTest):
    name = "F1 Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.f1

    def get_description(self, value: Numeric) -> str:
        return f"F1 Score is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestRecallScore(SimpleClassificationTest):
    name = "Recall Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.recall

    def get_description(self, value: Numeric) -> str:
        return f"Recall Score is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestRocAuc(SimpleClassificationTest):
    name = "ROC AUC Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.roc_auc

    def get_description(self, value: Numeric) -> str:
        return f"ROC AUC Score is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestLogLoss(SimpleClassificationTest):
    name = "Logarithmic Loss"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.log_loss

    def get_description(self, value: Numeric) -> str:
        return f" Logarithmic Loss is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestTPR(SimpleClassificationTest):
    name = "True Positive Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tp_total = sum([data["tp"] for label, data in result.confusion_by_classes.items()])
        fn_total = sum([data["fn"] for label, data in result.confusion_by_classes.items()])
        return tp_total / (tp_total + fn_total)

    def get_description(self, value: Numeric) -> str:
        return f"True Positive Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestTNR(SimpleClassificationTest):
    name = "True Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return tn_total / (tn_total + fp_total)

    def get_description(self, value: Numeric) -> str:
        return f"True Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestFPR(SimpleClassificationTest):
    name = "False Positive Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return fp_total / (tn_total + fp_total)

    def get_description(self, value: Numeric) -> str:
        return f"False Positive Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestFNR(SimpleClassificationTest):
    name = "False Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tp_total = sum([data["tp"] for label, data in result.confusion_by_classes.items()])
        fn_total = sum([data["fn"] for label, data in result.confusion_by_classes.items()])
        return fn_total / (tp_total + fn_total)

    def get_description(self, value: Numeric) -> str:
        return f"False Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestPrecisionByClass(SimpleClassificationTest):
    name: str = "Precision Score by Class"

    def __init__(self,
                 label: str,
                 threshold: Optional[float] = None,
                 metric: Optional[ClassificationPerformanceMetrics] = None):
        super().__init__(threshold, metric)
        self.label = label

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['precision']

    def get_description(self, value: Numeric) -> str:
        return f"Precision Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestRecallByClass(SimpleClassificationTest):
    name: str = "Recall Score by Class"

    def __init__(self,
                 label: str,
                 threshold: Optional[float] = None,
                 metric: Optional[ClassificationPerformanceMetrics] = None):
        super().__init__(threshold, metric)
        self.label = label

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['recall']

    def get_description(self, value: Numeric) -> str:
        return f"Recall Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestF1ByClass(SimpleClassificationTest):
    name: str = "F1 Score by Class"

    def __init__(self,
                 label: str,
                 threshold: Optional[float] = None,
                 metric: Optional[ClassificationPerformanceMetrics] = None):
        super().__init__(threshold, metric)
        self.label = label

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['f1-score']

    def get_description(self, value: Numeric) -> str:
        return f"F1 Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"
