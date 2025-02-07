from typing import Dict
from typing import List

from evidently.future.container import MetricContainer
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import MAE
from evidently.future.metrics import MAPE
from evidently.future.metrics import RMSE
from evidently.future.metrics import AbsMaxError
from evidently.future.metrics import DummyMAE
from evidently.future.metrics import DummyMAPE
from evidently.future.metrics import DummyRMSE
from evidently.future.metrics import MeanError
from evidently.future.metrics import R2Score
from evidently.future.metrics.regression import _gen_regression_input_data
from evidently.future.report import Context
from evidently.metrics import RegressionDummyMetric
from evidently.metrics import RegressionErrorDistribution
from evidently.metrics import RegressionErrorPlot
from evidently.metrics import RegressionPredictedVsActualPlot
from evidently.metrics import RegressionQualityMetric
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import link_metric


class RegressionQuality(MetricContainer):
    def __init__(
        self,
        pred_actual_plot: bool = False,
        error_plot: bool = False,
        error_distr: bool = False,
    ):
        self._pred_actual_plot = pred_actual_plot
        self._error_plot = error_plot
        self._error_distr = error_distr

    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            MeanError(),
            MAPE(),
            RMSE(),
            MAE(),
            R2Score(),
            AbsMaxError(),
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        widgets = context.get_legacy_metric(
            RegressionQualityMetric(),
            _gen_regression_input_data,
        )[1]
        if self._pred_actual_plot:
            widgets += context.get_legacy_metric(
                RegressionPredictedVsActualPlot(),
                _gen_regression_input_data,
            )[1]
        if self._error_plot:
            widgets += context.get_legacy_metric(
                RegressionErrorPlot(),
                _gen_regression_input_data,
            )[1]
        if self._error_distr:
            widgets += context.get_legacy_metric(
                RegressionErrorDistribution(),
                _gen_regression_input_data,
            )[1]
        for metric in self.metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionDummyQuality(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            DummyMAE(),
            DummyMAPE(),
            DummyRMSE(),
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        widgets = context.get_legacy_metric(
            RegressionDummyMetric(),
            _gen_regression_input_data,
        )[1]

        for metric in self.metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionPreset(MetricContainer):
    def __init__(self):
        self._quality = None

    def generate_metrics(self, context: Context) -> List[Metric]:
        self._quality = RegressionQuality(True, True, True)
        return self._quality.metrics(context) + [
            MAPE(),
            AbsMaxError(),
            R2Score(),
        ]

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        return (
            self._quality.render(context, results)
            + context.get_metric_result(MAPE()).widget
            + context.get_metric_result(AbsMaxError()).widget
            + context.get_metric_result(R2Score()).widget
        )
