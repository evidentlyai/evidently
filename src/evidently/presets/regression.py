from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently._pydantic_compat import PrivateAttr
from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.metric_types import GenericSingleValueMetricTests
from evidently.core.metric_types import MeanStdMetricsPossibleTests
from evidently.core.metric_types import MeanStdMetricTests
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import SingleValueMetricTests
from evidently.core.metric_types import convert_tests
from evidently.core.metric_types import convert_to_mean_tests
from evidently.core.report import Context
from evidently.legacy.metrics import RegressionDummyMetric
from evidently.legacy.metrics import RegressionErrorDistribution
from evidently.legacy.metrics import RegressionErrorPlot
from evidently.legacy.metrics import RegressionPredictedVsActualPlot
from evidently.legacy.metrics import RegressionQualityMetric
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import link_metric
from evidently.metrics import MAE
from evidently.metrics import MAPE
from evidently.metrics import RMSE
from evidently.metrics import AbsMaxError
from evidently.metrics import DummyMAE
from evidently.metrics import DummyMAPE
from evidently.metrics import DummyRMSE
from evidently.metrics import MeanError
from evidently.metrics import R2Score
from evidently.metrics.regression import _gen_regression_input_data


class RegressionQuality(MetricContainer):
    pred_actual_plot: bool = False
    error_plot: bool = False
    error_distr: bool = False
    mean_error_tests: MeanStdMetricTests
    mape_tests: MeanStdMetricTests
    rmse_tests: SingleValueMetricTests = None
    mae_tests: MeanStdMetricTests
    r2score_tests: SingleValueMetricTests = None
    abs_max_error_tests: SingleValueMetricTests = None
    regression_name: str = "default"

    def __init__(
        self,
        pred_actual_plot: bool = False,
        error_plot: bool = False,
        error_distr: bool = False,
        mean_error_tests: MeanStdMetricsPossibleTests = None,
        mape_tests: MeanStdMetricsPossibleTests = None,
        rmse_tests: GenericSingleValueMetricTests = None,
        mae_tests: MeanStdMetricsPossibleTests = None,
        r2score_tests: GenericSingleValueMetricTests = None,
        abs_max_error_tests: GenericSingleValueMetricTests = None,
        include_tests: bool = True,
        regression_name: str = "default",
    ):
        self.pred_actual_plot = pred_actual_plot
        self.error_plot = error_plot
        self.error_distr = error_distr
        self.mean_error_tests = convert_to_mean_tests(mean_error_tests) or MeanStdMetricTests()
        self.mape_tests = convert_to_mean_tests(mape_tests) or MeanStdMetricTests()
        self.rmse_tests = convert_tests(rmse_tests)
        self.mae_tests = convert_to_mean_tests(mae_tests) or MeanStdMetricTests()
        self.r2score_tests = convert_tests(r2score_tests)
        self.abs_max_error_tests = convert_tests(abs_max_error_tests)
        self.regression_name = regression_name
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            MeanError(
                regression_name=self.regression_name,
                mean_tests=self._get_tests(self.mean_error_tests.mean),
                std_tests=self._get_tests(self.mean_error_tests.std),
            ),
            MAPE(
                regression_name=self.regression_name,
                mean_tests=self._get_tests(self.mape_tests.mean),
                std_tests=self._get_tests(self.mape_tests.std),
            ),
            RMSE(regression_name=self.regression_name, tests=self._get_tests(self.rmse_tests)),
            MAE(
                regression_name=self.regression_name,
                mean_tests=self._get_tests(self.mae_tests.mean),
                std_tests=self._get_tests(self.mae_tests.std),
            ),
            R2Score(regression_name=self.regression_name, tests=self._get_tests(self.r2score_tests)),
            AbsMaxError(regression_name=self.regression_name, tests=self._get_tests(self.abs_max_error_tests)),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        widgets = context.get_legacy_metric(
            RegressionQualityMetric(),
            _gen_regression_input_data,
            self.regression_name,
        )[1]
        if self.pred_actual_plot:
            widgets += context.get_legacy_metric(
                RegressionPredictedVsActualPlot(),
                _gen_regression_input_data,
                self.regression_name,
            )[1]
        if self.error_plot:
            widgets += context.get_legacy_metric(
                RegressionErrorPlot(),
                _gen_regression_input_data,
                self.regression_name,
            )[1]
        if self.error_distr:
            widgets += context.get_legacy_metric(
                RegressionErrorDistribution(),
                _gen_regression_input_data,
                self.regression_name,
            )[1]
        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionDummyQuality(MetricContainer):
    mae_tests: SingleValueMetricTests = None
    mape_tests: SingleValueMetricTests = None
    rmse_tests: SingleValueMetricTests = None
    regression_name: str = "default"

    def __init__(
        self,
        mae_tests: GenericSingleValueMetricTests = None,
        mape_tests: GenericSingleValueMetricTests = None,
        rmse_tests: GenericSingleValueMetricTests = None,
        regression_name: str = "default",
        include_tests: bool = True,
    ):
        self.mae_tests = convert_tests(mae_tests)
        self.mape_tests = convert_tests(mape_tests)
        self.rmse_tests = convert_tests(rmse_tests)
        self.regression_name = regression_name
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            DummyMAE(regression_name=self.regression_name, tests=self._get_tests(self.mae_tests)),
            DummyMAPE(regression_name=self.regression_name, tests=self._get_tests(self.mape_tests)),
            DummyRMSE(regression_name=self.regression_name, tests=self._get_tests(self.rmse_tests)),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        widgets = context.get_legacy_metric(
            RegressionDummyMetric(),
            _gen_regression_input_data,
            self.regression_name,
        )[1]

        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets


class RegressionPreset(MetricContainer):
    mean_error_tests: MeanStdMetricTests
    mape_tests: MeanStdMetricTests
    rmse_tests: SingleValueMetricTests = None
    mae_tests: MeanStdMetricTests
    r2score_tests: SingleValueMetricTests = None
    abs_max_error_tests: SingleValueMetricTests = None

    _quality: Optional[RegressionQuality] = PrivateAttr(None)
    regression_name: str = "default"

    def __init__(
        self,
        mean_error_tests: MeanStdMetricsPossibleTests = None,
        mape_tests: MeanStdMetricsPossibleTests = None,
        rmse_tests: GenericSingleValueMetricTests = None,
        mae_tests: MeanStdMetricsPossibleTests = None,
        r2score_tests: GenericSingleValueMetricTests = None,
        abs_max_error_tests: GenericSingleValueMetricTests = None,
        regression_name: str = "default",
        include_tests: bool = True,
    ):
        self._quality = None
        self.mean_error_tests = convert_to_mean_tests(mean_error_tests) or MeanStdMetricTests()
        self.mape_tests = convert_to_mean_tests(mape_tests) or MeanStdMetricTests()
        self.rmse_tests = convert_tests(rmse_tests)
        self.mae_tests = convert_to_mean_tests(mae_tests) or MeanStdMetricTests()
        self.r2score_tests = convert_tests(r2score_tests)
        self.abs_max_error_tests = convert_tests(abs_max_error_tests)
        self.regression_name = regression_name
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        self._quality = RegressionQuality(
            True,
            True,
            True,
            self.mean_error_tests,
            self.mape_tests,
            self.rmse_tests,
            self.mae_tests,
            self.r2score_tests,
            self.abs_max_error_tests,
            include_tests=self.include_tests,
            regression_name=self.regression_name,
        )
        return (
            self._quality.metrics(context)
            + [
                # MAPE(mean_tests=self._get_tests(self.mape_tests.mean), std_tests=self._get_tests(self.mape_tests.std)),
                # AbsMaxError(tests=self._get_tests(self.abs_max_error_tests)),
                # R2Score(tests=self._get_tests(self.r2score_tests)),
            ]
        )

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
                MAPE(
                    regression_name=self.regression_name,
                    mean_tests=self.mape_tests.mean,
                    std_tests=self.mape_tests.std,
                ),
            ).get_widgets()
            + context.get_metric_result(
                AbsMaxError(
                    regression_name=self.regression_name,
                    tests=self.abs_max_error_tests,
                )
            ).get_widgets()
            + context.get_metric_result(
                R2Score(regression_name=self.regression_name, tests=self.r2score_tests)
            ).get_widgets()
        )
