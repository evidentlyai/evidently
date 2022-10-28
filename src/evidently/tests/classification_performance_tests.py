import abc
from abc import ABC
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from evidently.metrics.base_metric import Metric
from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetrics
from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetricsThreshold
from evidently.metrics.classification_performance_metrics import ClassificationPerformanceMetricsTopK
from evidently.metrics.classification_performance_metrics import ClassificationPerformanceResults
from evidently.metrics.classification_performance_metrics import DatasetClassificationPerformanceMetrics
from evidently.renderers.base_renderer import TestHtmlInfo
from evidently.renderers.base_renderer import TestRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import plotly_figure
from evidently.tests.base_test import BaseCheckValueTest
from evidently.tests.base_test import GroupData
from evidently.tests.base_test import GroupingTypes
from evidently.tests.base_test import TestValueCondition
from evidently.tests.utils import approx
from evidently.tests.utils import plot_boxes
from evidently.tests.utils import plot_conf_mtrx
from evidently.tests.utils import plot_rates
from evidently.tests.utils import plot_roc_auc
from evidently.utils.types import Numeric

CLASSIFICATION_GROUP = GroupData("classification", "Classification", "")
GroupingTypes.TestGroup.add_value(CLASSIFICATION_GROUP)


class SimpleClassificationTest(BaseCheckValueTest):
    group = CLASSIFICATION_GROUP.id
    name: str
    metric: Metric[ClassificationPerformanceResults]

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
        return self.get_value(self.metric.get_result().current)

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_metrics = self.metric.get_result().reference
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(self.metric.get_result().dummy) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        return TestValueCondition(gt=self.get_value(self.metric.get_result().dummy))

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
    ):
        super().__init__(
            eq=eq,
            gt=gt,
            gte=gte,
            is_in=is_in,
            lt=lt,
            lte=lte,
            not_eq=not_eq,
            not_in=not_in,
        )
        if k is not None and classification_threshold is not None:
            raise ValueError("Only one of classification_threshold or k should be given")
        if k is not None:
            self.metric = ClassificationPerformanceMetricsTopK(k)
        if classification_threshold is not None:
            self.metric = ClassificationPerformanceMetricsThreshold(classification_threshold)
        self.k = k
        self.threshold = classification_threshold

    def calculate_value_for_test(self) -> Optional[Any]:
        return self.get_value(self.metric.get_result().current)

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        result = self.metric.get_result()
        ref_metrics = result.reference
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy
        return TestValueCondition(gt=self.get_value(dummy_metrics))


class TestAccuracyScore(SimpleClassificationTestTopK):
    name = "Accuracy Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.accuracy

    def get_description(self, value: Numeric) -> str:
        return f"The Accuracy Score is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestAccuracyScore)
class TestAccuracyScoreRenderer(TestRenderer):
    def render_json(self, obj: TestAccuracyScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["accuracy"] = obj.value
        return base

    def render_html(self, obj: TestAccuracyScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("Accuracy Score", plotly_figure(figure=fig, title=""))
        return info


class TestPrecisionScore(SimpleClassificationTestTopK):
    name = "Precision Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.precision

    def get_description(self, value: Numeric) -> str:
        return f"The Precision Score is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestPrecisionScore)
class TestPrecisionScoreRenderer(TestRenderer):
    def render_json(self, obj: TestPrecisionScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["precision"] = obj.value
        return base

    def render_html(self, obj: TestPrecisionScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("Precision Score", plotly_figure(figure=fig, title=""))
        return info


class TestF1Score(SimpleClassificationTestTopK):
    name = "F1 Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.f1

    def get_description(self, value: Numeric) -> str:
        return f"The F1 Score is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestF1Score)
class TestF1ScoreRenderer(TestRenderer):
    def render_json(self, obj: TestF1Score) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["f1"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("F1 Score", plotly_figure(title="", figure=fig))
        return info


class TestRecallScore(SimpleClassificationTestTopK):
    name = "Recall Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.recall

    def get_description(self, value: Numeric) -> str:
        return f"The Recall Score is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestRecallScore)
class TestRecallScoreRenderer(TestRenderer):
    def render_json(self, obj: TestRecallScore) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["recall"] = obj.value
        return base

    def render_html(self, obj: TestRecallScore) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = curr_metrics.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("Recall Score", plotly_figure(title="", figure=fig))
        return info


class TestRocAuc(SimpleClassificationTest):
    name = "ROC AUC Score"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.roc_auc

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "Not enough data to calculate ROC AUC. Consider providing probabilities instead of labels."
        else:
            return f"The ROC AUC Score is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestRocAuc)
class TestRocAucRenderer(TestRenderer):
    def render_json(self, obj: TestRocAuc) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["roc_auc"] = obj.value
        return base

    def render_html(self, obj: TestRocAuc) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_roc_curve = curr_metrics.roc_curve
        ref_roc_curve = None
        if ref_metrics is not None:
            ref_roc_curve = ref_metrics.roc_curve
        if curr_roc_curve is not None:
            for title, plot in plot_roc_auc(
                curr_roc_curve=curr_roc_curve, ref_roc_curve=ref_roc_curve, color_options=self.color_options
            ):
                info.with_details(title, plot)
        return info


class TestLogLoss(SimpleClassificationTest):
    name = "Logarithmic Loss"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        ref_metrics = self.metric.get_result().reference
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(self.metric.get_result().dummy) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        return TestValueCondition(lt=self.get_value(self.metric.get_result().dummy))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.log_loss

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "Not enough data to calculate Logarithmic Loss. Consider providing probabilities instead of labels."
        else:
            return f"The Logarithmic Loss is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestLogLoss)
class TestLogLossRenderer(TestRenderer):
    def render_json(self, obj: TestLogLoss) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["log_loss"] = obj.value
        return base

    def render_html(self, obj: TestLogLoss) -> TestHtmlInfo:
        info = super().render_html(obj)
        result = obj.metric.get_result()

        curr_metrics = result.current.plot_data
        ref_metrics = None if result.reference is None else result.reference.plot_data

        if curr_metrics is not None:
            fig = plot_boxes(curr_for_plots=curr_metrics, ref_for_plots=ref_metrics, color_options=self.color_options)
            info.with_details("Logarithmic Loss", plotly_figure(title="", figure=fig))

        return info


class TestTPR(SimpleClassificationTestTopK):
    name = "True Positive Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.tpr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"The True Positive Rate is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestTPR)
class TestTPRRenderer(TestRenderer):
    def render_json(self, obj: TestTPR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["tpr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None

        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data

        if curr_rate_plots_data is not None:
            fig = plot_rates(
                curr_rate_plots_data=curr_rate_plots_data,
                ref_rate_plots_data=ref_rate_plots_data,
                color_options=self.color_options,
            )
            info.with_details("TPR", plotly_figure(title="", figure=fig))

        return info


class TestTNR(SimpleClassificationTestTopK):
    name = "True Negative Rate"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.tnr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"The True Negative Rate is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestTNR)
class TestTNRRenderer(TestRenderer):
    def render_json(self, obj: TestTNR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["tnr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(
                curr_rate_plots_data=curr_rate_plots_data,
                ref_rate_plots_data=ref_rate_plots_data,
                color_options=self.color_options,
            )
            info.with_details("TNR", plotly_figure(title="", figure=fig))
        return info


class TestFPR(SimpleClassificationTestTopK):
    name = "False Positive Rate"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        result = self.metric.get_result()
        ref_metrics = result.reference
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy
        return TestValueCondition(lt=self.get_value(dummy_metrics))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.fpr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"The False Positive Rate is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestFPR)
class TestFPRRenderer(TestRenderer):
    def render_json(self, obj: TestFPR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["fpr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(
                curr_rate_plots_data=curr_rate_plots_data,
                ref_rate_plots_data=ref_rate_plots_data,
                color_options=self.color_options,
            )
            info.with_details("FPR", plotly_figure(title="", figure=fig))
        return info


class TestFNR(SimpleClassificationTestTopK):
    name = "False Negative Rate"

    def get_condition(self) -> TestValueCondition:
        if self.condition.has_condition():
            return self.condition
        result = self.metric.get_result()
        ref_metrics = result.reference
        if ref_metrics is not None:
            return TestValueCondition(eq=approx(self.get_value(ref_metrics), relative=0.2))
        if self.get_value(result.dummy) is None:
            raise ValueError("Neither required test parameters nor reference data has been provided.")
        dummy_metrics = result.dummy
        return TestValueCondition(lt=self.get_value(dummy_metrics))

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.fnr

    def get_description(self, value: Numeric) -> str:
        if value is None:
            return "This test is applicable only for binary classification"

        return f"The False Negative Rate is {value:.3g}. The test threshold is {self.get_condition()}"


@default_renderer(wrap_type=TestFNR)
class TestFNRRenderer(TestRenderer):
    def render_json(self, obj: TestFNR) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["fnr"] = obj.value
        return base

    def render_html(self, obj: TestF1Score) -> TestHtmlInfo:
        info = super().render_html(obj)
        curr_metrics = obj.metric.get_result().current
        ref_metrics = obj.metric.get_result().reference
        curr_rate_plots_data = curr_metrics.rate_plots_data
        ref_rate_plots_data = None
        if ref_metrics is not None:
            ref_rate_plots_data = ref_metrics.rate_plots_data
        if curr_rate_plots_data is not None:
            fig = plot_rates(
                curr_rate_plots_data=curr_rate_plots_data,
                ref_rate_plots_data=ref_rate_plots_data,
                color_options=self.color_options,
            )
            info.with_details("FNR", plotly_figure(title="", figure=fig))
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
        return (
            f"The precision score of the label **{self.label}** is {value:.3g}. "
            f"The test threshold is {self.get_condition()}"
        )


@default_renderer(wrap_type=TestPrecisionByClass)
class TestPrecisionByClassRenderer(TestRenderer):
    def render_json(self, obj: TestPrecisionByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["precision"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestPrecisionByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = obj.metric.get_result().current.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("Precision by Class", plotly_figure(title="", figure=fig))
        return info


class TestRecallByClass(ByClassClassificationTest):
    name: str = "Recall Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]["recall"]

    def get_description(self, value: Numeric) -> str:
        return (
            f"The recall score of the label **{self.label}** is {value:.3g}. "
            f"The test threshold is {self.get_condition()}"
        )


@default_renderer(wrap_type=TestRecallByClass)
class TestRecallByClassRenderer(TestRenderer):
    def render_json(self, obj: TestRecallByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["recall"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestRecallByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = obj.metric.get_result().current.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("Recall by Class", plotly_figure(title="", figure=fig))
        return info


class TestF1ByClass(ByClassClassificationTest):
    name: str = "F1 Score by Class"

    def get_value(self, result: DatasetClassificationPerformanceMetrics):
        return result.metrics_matrix[self.label]["f1-score"]

    def get_description(self, value: Numeric) -> str:
        return (
            f"The F1 score of the label **{self.label}** is {value:.3g}. The test threshold is {self.get_condition()}"
        )


@default_renderer(wrap_type=TestF1ByClass)
class TestF1ByClassRenderer(TestRenderer):
    def render_json(self, obj: TestF1ByClass) -> dict:
        base = super().render_json(obj)
        base["parameters"]["condition"] = obj.get_condition().as_dict()
        base["parameters"]["f1"] = obj.value
        base["parameters"]["label"] = obj.label
        return base

    def render_html(self, obj: TestF1ByClass) -> TestHtmlInfo:
        info = super().render_html(obj)
        ref_metrics = obj.metric.get_result().reference
        curr_matrix = obj.metric.get_result().current.confusion_matrix
        ref_matrix = None
        if ref_metrics is not None:
            ref_matrix = ref_metrics.confusion_matrix
        fig = plot_conf_mtrx(curr_matrix, ref_matrix)
        info.with_details("F1 by Class", plotly_figure(title="", figure=fig))
        return info
