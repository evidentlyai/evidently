from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.metric_types import MeanStdMetricTests
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import SingleValueMetricTests
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
        mean_error_tests: Optional[MeanStdMetricTests] = None,
        mape_tests: Optional[MeanStdMetricTests] = None,
        rmse_tests: SingleValueMetricTests = None,
        mae_tests: Optional[MeanStdMetricTests] = None,
        r2score_tests: SingleValueMetricTests = None,
        abs_max_error_tests: SingleValueMetricTests = None,
    ):
        self._pred_actual_plot = pred_actual_plot
        self._error_plot = error_plot
        self._error_distr = error_distr
        self._mean_error_tests = mean_error_tests or MeanStdMetricTests()
        self._mape_tests = mape_tests or MeanStdMetricTests()
        self._rmse_tests = rmse_tests
        self._mae_tests = mae_tests or MeanStdMetricTests()
        self._r2score_tests = r2score_tests
        self._abs_max_error_tests = abs_max_error_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            MeanError(mean_tests=self._mean_error_tests.mean, std_tests=self._mean_error_tests.std),
            MAPE(mean_tests=self._mape_tests.mean, std_tests=self._mape_tests.std),
            RMSE(tests=self._rmse_tests),
            MAE(mean_tests=self._mae_tests.mean, std_tests=self._mae_tests.std),
            R2Score(tests=self._r2score_tests),
            AbsMaxError(tests=self._abs_max_error_tests),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
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
        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionDummyQuality(MetricContainer):
    def __init__(
        self,
        mae_tests: SingleValueMetricTests = None,
        mape_tests: SingleValueMetricTests = None,
        rmse_tests: SingleValueMetricTests = None,
    ):
        self._mae_tests = mae_tests
        self._mape_tests = mape_tests
        self._rmse_tests = rmse_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            DummyMAE(tests=self._mae_tests),
            DummyMAPE(tests=self._mape_tests),
            DummyRMSE(tests=self._rmse_tests),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        widgets = context.get_legacy_metric(
            RegressionDummyMetric(),
            _gen_regression_input_data,
        )[1]

        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionPreset(MetricContainer):
    _quality: Optional[RegressionQuality] = None

    def __init__(
        self,
        mean_error_tests: Optional[MeanStdMetricTests] = None,
        mape_tests: Optional[MeanStdMetricTests] = None,
        rmse_tests: SingleValueMetricTests = None,
        mae_tests: Optional[MeanStdMetricTests] = None,
        r2score_tests: SingleValueMetricTests = None,
        abs_max_error_tests: SingleValueMetricTests = None,
    ):
        self._quality = None
        self._mean_error_tests = mean_error_tests or MeanStdMetricTests()
        self._mape_tests = mape_tests or MeanStdMetricTests()
        self._rmse_tests = rmse_tests
        self._mae_tests = mae_tests or MeanStdMetricTests()
        self._r2score_tests = r2score_tests
        self._abs_max_error_tests = abs_max_error_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        self._quality = RegressionQuality(
            True,
            True,
            True,
            self._mean_error_tests,
            self._mape_tests,
            self._rmse_tests,
            self._mae_tests,
            self._r2score_tests,
            self._abs_max_error_tests,
        )
        return self._quality.metrics(context) + [
            MAPE(mean_tests=self._mape_tests.mean, std_tests=self._mape_tests.std),
            AbsMaxError(tests=self._abs_max_error_tests),
            R2Score(tests=self._r2score_tests),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        if self._quality is None:
            raise ValueError("No _quality set in preset, something went wrong.")
        return (
            self._quality.render(context)
            + context.get_metric_result(
                MAPE(mean_tests=self._mape_tests.mean, std_tests=self._mape_tests.std),
            ).widget
            + context.get_metric_result(AbsMaxError(tests=self._abs_max_error_tests)).widget
            + context.get_metric_result(R2Score(tests=self._r2score_tests)).widget
        )
