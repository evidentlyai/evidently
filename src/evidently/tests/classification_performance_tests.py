import abc
from abc import ABC
from typing import Optional, List, Union, Any, Tuple

from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetrics
from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetricsResults
from evidently.metrics.classification_performance_metrics import DatasetClassificationPerformanceMetrics
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import DetailsInfo
from evidently.tests.base_test import BaseCheckValueTest, TestValueCondition
from evidently.tests.utils import Numeric, approx, plot_conf_mtrx, plot_roc_auc


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
        if self.condition.has_condition():
            return self.condition
        ref_metrics = self.metric.get_result().reference_metrics
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics),relative=0.1))
        if self.get_value(self.metric.get_result().dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        return TestValueCondition(gt=self.get_value(self.metric.get_result().dummy_metrics))

    @abc.abstractmethod
    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        raise NotImplementedError()


class SimpleClassificationTestTopK(SimpleClassificationTest, ABC):
    def __init__(
            self,
            classification_threshold: Optional[float] = None,
            k: Optional[Union[float, int]] = None,
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
        if metric is None:
            metric = ClassificationPerformanceMetrics()
        if k is not None and classification_threshold is not None:
            raise ValueError("Only one of classification_threshold or k should be given")
        if k is not None:
            metric = metric.with_k(k)
        if classification_threshold is not None:
            metric.with_threshold(classification_threshold)
        super().__init__(eq=eq,
                         gt=gt,
                         gte=gte,
                         is_in=is_in,
                         lt=lt,
                         lte=lte,
                         not_eq=not_eq,
                         not_in=not_in,
                         metric=metric,
                         )
        self.k = k
        self.threshold = classification_threshold

    def calculate_value_for_test(self) -> Optional[Any]:
        if self.k is not None:
            return self.get_value(self.metric.get_result().current_by_k_metrics[self.k])
        if self.threshold is not None:
            return self.get_value(self.metric.get_result().current_by_threshold_metrics[self.threshold])
        return self.get_value(self.metric.get_result().current_metrics)

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        result = self.metric.get_result()
        ref_metrics = result.reference_metrics
        if ref_metrics is not None:
            if self.k is not None:
                if result.reference_by_k_metrics is None:
                    raise ValueError("Reference by K isn't set but expected by test")
                ref_metrics = result.reference_by_k_metrics[self.k]
            if self.threshold is not None:
                if result.reference_by_threshold_metrics is None:
                    raise ValueError("Reference by Threshold isn't set but expected by test")
                ref_metrics = result.reference_by_threshold_metrics[self.threshold]
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.1))
        if self.get_value(result.dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        return TestValueCondition(gt=self.get_value(result.dummy_metrics))


class TestAccuracyScore(SimpleClassificationTestTopK):
    name = "Accuracy Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.accuracy

    def get_description(self, value: Numeric) -> str:
        return f"Accuracy Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestAccuracyScore)
class TestAccuracyScoreRenderer(TestRenderer):
    def render_html(self, obj: TestAccuracyScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "AccuracyScore",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestPrecisionScore(SimpleClassificationTestTopK):
    name = "Precision Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.precision

    def get_description(self, value: Numeric) -> str:
        return f"Precision Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestPrecisionScore)
class TestPrecisionScoreRenderer(TestRenderer):
    def render_html(self, obj: TestPrecisionScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "PrecisionScore",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestF1Score(SimpleClassificationTestTopK):
    name = "F1 Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.f1

    def get_description(self, value: Numeric) -> str:
        return f"F1 Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestF1Score)
class TestF1ScoreRenderer(TestRenderer):
    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "F1Score",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestRecallScore(SimpleClassificationTestTopK):
    name = "Recall Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.recall

    def get_description(self, value: Numeric) -> str:
        return f"Recall Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestRecallScore)
class TestRecallScoreRenderer(TestRenderer):
    def render_html(self, obj: TestRecallScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "RecallScore",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestRocAuc(SimpleClassificationTest):
    name = "ROC AUC Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.roc_auc

    def get_description(self, value: Numeric) -> str:
        return f"ROC AUC Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestRocAuc)
class TestRocAucRenderer(TestRenderer):
    def render_html(self, obj: TestRocAuc) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current_metrics 
        ref_metrics = obj.metric.get_result().reference_metrics 
        curr_roc_curve = curr_metrics.roc_curve
        ref_roc_curve = None
        if ref_metrics is not None:
            ref_roc_curve = ref_metrics.roc_curve
        info.details = plot_roc_auc(curr_roc_curve, ref_roc_curve)
        return info


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

@default_renderer(test_type=TestTPR)
class TestTPRRenderer(TestRenderer):
    def render_html(self, obj: TestTPR) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "TPR",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info

class TestTNR(SimpleClassificationTest):
    name = "True Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return tn_total / (tn_total + fp_total)

    def get_description(self, value: Numeric) -> str:
        return f"True Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestTNR)
class TestTNRRenderer(TestRenderer):
    def render_html(self, obj: TestTNR) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "TNR",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestFPR(SimpleClassificationTest):
    name = "False Positive Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tn_total = sum([data["tn"] for label, data in result.confusion_by_classes.items()])
        fp_total = sum([data["fp"] for label, data in result.confusion_by_classes.items()])
        return fp_total / (tn_total + fp_total)

    def get_description(self, value: Numeric) -> str:
        return f"False Positive Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestFPR)
class TestFPRRenderer(TestRenderer):
    def render_html(self, obj: TestFPR) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "FPR",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class TestFNR(SimpleClassificationTest):
    name = "False Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        tp_total = sum([data["tp"] for label, data in result.confusion_by_classes.items()])
        fn_total = sum([data["fn"] for label, data in result.confusion_by_classes.items()])
        return fn_total / (tp_total + fn_total)

    def get_description(self, value: Numeric) -> str:
        return f"False Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestFNR)
class TestFNRRenderer(TestRenderer):
    def render_html(self, obj: TestFNR) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "FNR",
                "",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


class ByClassClassificationTest(SimpleClassificationTest):
    def __init__(self,
                 label: str,
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
        super().__init__(eq=eq,
                         gt=gt,
                         gte=gte,
                         is_in=is_in,
                         lt=lt,
                         lte=lte,
                         not_eq=not_eq,
                         not_in=not_in,
                         metric=metric)
        self.label = label


class TestPrecisionByClass(ByClassClassificationTest):
    name: str = "Precision Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['precision']

    def get_description(self, value: Numeric) -> str:
        return f"Precision Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestRecallByClass(ByClassClassificationTest):
    name: str = "Recall Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['recall']

    def get_description(self, value: Numeric) -> str:
        return f"Recall Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"


class TestF1ByClass(ByClassClassificationTest):
    name: str = "F1 Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]['f1-score']

    def get_description(self, value: Numeric) -> str:
        return f"F1 Score of {self.label} is {value:.3g}. Test Threshold is {self.get_condition()}"

def _get_metric_result(
    k: Optional[Union[int, float]],
    threshold: Optional[float],
    is_ref: bool,
    result: ClassificationPerformanceMetricsResults
) -> Tuple[DatasetClassificationPerformanceMetrics, Optional[DatasetClassificationPerformanceMetrics]]:
    ref_metrics = None
    if k:
        curr_metrics = result.current_by_k_metrics[k]
        if result.reference_by_k_metrics is not None:
            ref_metrics = result.reference_by_k_metrics[k]
    elif threshold:
        curr_metrics = result.current_by_threshold_metrics[threshold]
        if result.reference_by_threshold_metrics is not None:
            ref_metrics = result.reference_by_threshold_metrics[threshold]
    else:
        curr_metrics = result.current_metrics
        if is_ref:
            ref_metrics = result.reference_metrics
    
    return curr_metrics, ref_metrics