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
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import Numeric, approx, plot_boxes, plot_conf_mtrx, plot_rates, plot_roc_auc


CLASSIFICATION_GROUP = GroupData("classification", "Classification", "")
GroupingTypes.TestGroup.add_value(CLASSIFICATION_GROUP)


class SimpleClassificationTest(BaseCheckValueTest):
    group = CLASSIFICATION_GROUP.id
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
        metric: Optional[ClassificationPerformanceMetrics] = None,
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
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
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
        metric: Optional[ClassificationPerformanceMetrics] = None,
    ):
        if metric is None:
            metric = ClassificationPerformanceMetrics()
        if k is not None and classification_threshold is not None:
            raise ValueError("Only one of classification_threshold or k should be given")
        if k is not None:
            metric = metric.with_k(k)
        if classification_threshold is not None:
            metric.with_threshold(classification_threshold)
        super().__init__(
            eq=eq,
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
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy_metrics
        if self.k is not None:
            dummy_metrics = result.dummy_by_k_metrics[self.k]
        if self.threshold is not None:
            dummy_metrics = result.dummy_by_threshold_metrics[self.threshold]
        return TestValueCondition(gt=self.get_value(dummy_metrics))


class TestAccuracyScore(SimpleClassificationTestTopK):
    name = "Accuracy Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.accuracy

    def get_description(self, value: Numeric) -> str:
        return f"Accuracy Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestAccuracyScore)
class TestAccuracyScoreRenderer(TestRenderer):
    def render_json(self, obj: TestAccuracyScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["accuracy"] = obj.value
        return base

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
    def render_json(self, obj: TestPrecisionScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["precision"] = obj.value
        return base

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
    def render_json(self, obj: TestF1Score) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["f1"] = obj.value
        return base

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
    def render_json(self, obj: TestRecallScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["recall"] = obj.value
        return base

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
        if value is None:
            return "Not enough data to calculate ROC AUC. Consider providing probabilities instead of labels."
        else:
            return f"ROC AUC Score is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestRocAuc)
class TestRocAucRenderer(TestRenderer):
    def render_json(self, obj: TestRocAuc) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["roc_auc"] = obj.value
        return base

    def render_html(self, obj: TestRocAuc) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current_metrics
        ref_metrics = obj.metric.get_result().reference_metrics
        curr_roc_curve = curr_metrics.roc_curve
        ref_roc_curve = None
        if ref_metrics is not None:
            ref_roc_curve = ref_metrics.roc_curve
        if curr_roc_curve is not None:
            info.details = plot_roc_auc(curr_roc_curve, ref_roc_curve)
        return info


class TestLogLoss(SimpleClassificationTest):
    name = "Logarithmic Loss"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_metrics = self.metric.get_result().reference_metrics
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(self.metric.get_result().dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        return TestValueCondition(lt=self.get_value(self.metric.get_result().dummy_metrics))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.log_loss

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "Not enough data to calculate Logarithmic Loss. Consider providing probabilities instead of labels."

        else:
            return f" Logarithmic Loss is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestLogLoss)
class TestLogLossRenderer(TestRenderer):
    def render_json(self, obj: TestLogLoss) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["log_loss"] = obj.value
        return base

    def render_html(self, obj: TestLogLoss) -> TestHtmlInfo:
        info = super().render_html(obj)
        data_for_plots = obj.metric.get_result().data_for_plots

        if data_for_plots is not None:
            curr_metrics = data_for_plots.current
            ref_metrics = data_for_plots.reference

        else:
            curr_metrics = None
            ref_metrics = None

        if curr_metrics is not None:
            fig = plot_boxes(curr_metrics, ref_metrics)
            fig_json = fig.to_plotly_json()
            info.details.append(
                DetailsInfo(
                    "TestLogLoss",
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


class TestTPR(SimpleClassificationTestTopK):
    name = "True Positive Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.tpr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"True Positive Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestTPR)
class TestTPRRenderer(TestRenderer):
    def render_json(self, obj: TestTPR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["tpr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(curr_rate_plots_data, ref_rate_plots_data)
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


class TestTNR(SimpleClassificationTestTopK):
    name = "True Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.tnr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"True Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestTNR)
class TestTNRRenderer(TestRenderer):
    def render_json(self, obj: TestTNR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["tnr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(curr_rate_plots_data, ref_rate_plots_data)
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


class TestFPR(SimpleClassificationTestTopK):
    name = "False Positive Rate"

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
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy_metrics
        if self.k is not None:
            dummy_metrics = result.dummy_by_k_metrics[self.k]
        if self.threshold is not None:
            dummy_metrics = result.dummy_by_threshold_metrics[self.threshold]
        return TestValueCondition(lt=self.get_value(dummy_metrics))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.fpr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"False Positive Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestFPR)
class TestFPRRenderer(TestRenderer):
    def render_json(self, obj: TestFPR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["fpr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(curr_rate_plots_data, ref_rate_plots_data)
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


class TestFNR(SimpleClassificationTestTopK):
    name = "False Negative Rate"

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
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy_metrics) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy_metrics
        if self.k is not None:
            dummy_metrics = result.dummy_by_k_metrics[self.k]
        if self.threshold is not None:
            dummy_metrics = result.dummy_by_threshold_metrics[self.threshold]
        return TestValueCondition(lt=self.get_value(dummy_metrics))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.fnr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"False Negative Rate is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestFNR)
class TestFNRRenderer(TestRenderer):
    def render_json(self, obj: TestFNR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["fnr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        k = obj.k
        threshold = obj.threshold
        is_ref = obj.metric.get_result().reference_metrics is not None
        curr_metrics, ref_metrics = _get_metric_result(k, threshold, is_ref, obj.metric.get_result())
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(curr_rate_plots_data, ref_rate_plots_data)
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


class ByClassClassificationTest(SimpleClassificationTest, ABC):
    def __init__(
        self,
        label: str,
        eq: Optional[Numeric] = None,
        gt: Optional[Numeric] = None,
        gte: Optional[Numeric] = None,
        is_in: Optional[List[Union[Numeric, str, bool]]] = None,
        lt: Optional[Numeric] = None,
        lte: Optional[Numeric] = None,
        not_eq: Optional[Numeric] = None,
        not_in: Optional[List[Union[Numeric, str, bool]]] = None,
        metric: Optional[ClassificationPerformanceMetrics] = None,
    ):
        super().__init__(
            eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in, metric=metric
        )
        self.label = label


class TestPrecisionByClass(ByClassClassificationTest):
    name: str = "Precision Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]["precision"]

    def get_description(self, value: Numeric) -> str:
        return f"Precision Score of **{self.label}** is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestPrecisionByClass)
class TestPrecisionByClassRenderer(TestRenderer):
    def render_json(self, obj: TestPrecisionByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["precision"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestPrecisionByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference_metrics
        curr_matrix = obj.metric.get_result().current_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "TestPrecisionByClass",
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


class TestRecallByClass(ByClassClassificationTest):
    name: str = "Recall Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]["recall"]

    def get_description(self, value: Numeric) -> str:
        return f"Recall Score of **{self.label}** is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestRecallByClass)
class TestRecallByClassRenderer(TestRenderer):
    def render_json(self, obj: TestRecallByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["recall"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestRecallByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference_metrics
        curr_matrix = obj.metric.get_result().current_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "TestRecallByClass",
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


class TestF1ByClass(ByClassClassificationTest):
    name: str = "F1 Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]["f1-score"]

    def get_description(self, value: Numeric) -> str:
        return f"F1 Score of **{self.label}** is {value:.3g}. Test Threshold is {self.get_condition()}"


@default_renderer(test_type=TestF1ByClass)
class TestF1ByClassRenderer(TestRenderer):
    def render_json(self, obj: TestF1ByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["f1"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestF1ByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference_metrics
        curr_matrix = obj.metric.get_result().current_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        fig_json = fig.to_plotly_json()
        info.details.append(
            DetailsInfo(
                "TestF1ByClass",
                "confusion matrix",
                BaseWidgetInfo(
                    title="",
                    size=2,
                    type="big_graph",
                    params={"data": fig_json["data"], "layout": fig_json["layout"]},
                ),
            )
        )
        return info


def _get_metric_result(
    k: Optional[Union[int, float]],
    threshold: Optional[float],
    is_ref: bool,
    result: ClassificationPerformanceMetricsResults,
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
