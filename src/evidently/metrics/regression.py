import abc
from typing import Dict
from typing import Generic
from typing import List

from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import MeanStdCalculation
from evidently.core.metric_types import MeanStdMetric
from evidently.core.metric_types import MeanStdValue
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
from evidently.core.metric_types import TMeanStdMetric
from evidently.core.metric_types import TSingleValueMetric
from evidently.core.report import Context
from evidently.core.report import _default_input_data_generator
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.metrics import RegressionAbsPercentageErrorPlot
from evidently.legacy.metrics import RegressionDummyMetric
from evidently.legacy.metrics import RegressionErrorDistribution
from evidently.legacy.metrics import RegressionErrorNormality
from evidently.legacy.metrics import RegressionErrorPlot
from evidently.legacy.metrics import RegressionPredictedVsActualPlot
from evidently.legacy.metrics.regression_performance.regression_dummy_metric import RegressionDummyMetricResults
from evidently.legacy.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.legacy.metrics.regression_performance.regression_quality import RegressionQualityMetricResults
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.utils.data_preprocessing import create_data_definition
from evidently.metrics._legacy import LegacyMetricCalculation
from evidently.tests import Reference
from evidently.tests import eq
from evidently.tests import gt
from evidently.tests import lt

ADDITIONAL_WIDGET_MAPPING: Dict[str, Metric] = {
    "error_plot": RegressionErrorPlot(),
    "error_distr": RegressionErrorDistribution(),
    "error_normality": RegressionErrorNormality(),
    "perc_error_plot": RegressionAbsPercentageErrorPlot(),
    "pred_actual_plot": RegressionPredictedVsActualPlot(),
}


def _gen_regression_input_data(context: "Context") -> InputData:
    default_data = _default_input_data_generator(context)
    regression = context.data_definition.get_regression("default")
    if regression is None:
        raise ValueError("No default regression in data definition")
    default_data.column_mapping.target = regression.target
    default_data.column_mapping.prediction = regression.prediction

    definition = create_data_definition(
        default_data.reference_data,
        default_data.current_data,
        default_data.column_mapping,
    )
    default_data.data_definition = definition
    return default_data


class LegacyRegressionMeanStdMetric(
    MeanStdCalculation[TMeanStdMetric],
    LegacyMetricCalculation[MeanStdValue, TMeanStdMetric, RegressionQualityMetricResults, RegressionQualityMetric],
    Generic[TMeanStdMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, _gen_regression_input_data)
                result += widgets
        return result

    def _gen_input_data(self, context: "Context") -> InputData:
        return _gen_regression_input_data(context)


class LegacyRegressionSingleValueMetric(
    SingleValueCalculation[TSingleValueMetric],
    LegacyMetricCalculation[SingleValue, TSingleValueMetric, RegressionQualityMetricResults, RegressionQualityMetric],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, _gen_regression_input_data)
                result += widgets
        return result

    def _gen_input_data(self, context: "Context") -> InputData:
        return _gen_regression_input_data(context)


class MeanError(MeanStdMetric):
    error_plot: bool = True
    error_distr: bool = False
    error_normality: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_mean_std(self.get_fingerprint())]


class MeanErrorCalculation(LegacyRegressionMeanStdMetric[MeanError]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(
                legacy_result.current.mean_error,
                legacy_result.current.error_std,
            ),
            None
            if legacy_result.reference is None
            else self.result(
                legacy_result.reference.mean_error,
                legacy_result.reference.error_std,
            ),
        )

    def display_name(self) -> str:
        return "Mean Error"


class MAE(MeanStdMetric):
    error_plot: bool = False
    error_distr: bool = True
    error_normality: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_mean_std(self.get_fingerprint(), True)]

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        dv: SingleValue = context.calculate_metric(DummyMAE().to_calculation())
        return [lt(dv.value).bind_mean_std(self.get_fingerprint())]


class MAECalculation(LegacyRegressionMeanStdMetric[MAE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(
                legacy_result.current.mean_abs_error,
                legacy_result.current.abs_error_std,
            ),
            None
            if legacy_result.reference is None
            else self.result(
                legacy_result.reference.mean_abs_error,
                legacy_result.reference.abs_error_std,
            ),
        )

    def display_name(self) -> str:
        return "Mean Absolute Error"


class RMSE(SingleValueMetric):
    error_plot: bool = False
    error_distr: bool = True
    error_normality: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_single(self.get_fingerprint())]

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        dv: SingleValue = context.calculate_metric(DummyRMSE().to_calculation())
        return [lt(dv.value).bind_single(self.get_fingerprint())]


class RMSECalculation(LegacyRegressionSingleValueMetric[RMSE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(legacy_result.current.rmse),
            None if legacy_result.reference is None else self.result(legacy_result.reference.rmse),
        )

    def display_name(self) -> str:
        return "RMSE"


class MAPE(MeanStdMetric):
    perc_error_plot: bool = True
    error_distr: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_mean_std(self.get_fingerprint())]

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        dv: SingleValue = context.calculate_metric(DummyMAPE().to_calculation())
        return [lt(dv.value).bind_mean_std(self.get_fingerprint())]


class MAPECalculation(LegacyRegressionMeanStdMetric[MAPE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(legacy_result.current.mean_abs_perc_error, legacy_result.current.abs_perc_error_std),
            None
            if legacy_result.reference is None
            else self.result(legacy_result.reference.mean_abs_perc_error, legacy_result.reference.abs_perc_error_std),
        )

    def display_name(self) -> str:
        return "Mean Absolute Percentage Error"


class R2Score(SingleValueMetric):
    error_distr: bool = False
    error_normality: bool = False

    def _default_tests(self, context: Context) -> List[BoundTest]:
        return [gt(0).bind_single(self.get_fingerprint())]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_single(self.get_fingerprint())]


class R2ScoreCalculation(LegacyRegressionSingleValueMetric[R2Score]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(legacy_result.current.r2_score),
            None if legacy_result.reference is None else self.result(legacy_result.reference.r2_score),
        )

    def display_name(self) -> str:
        return "R2 Score"


class AbsMaxError(SingleValueMetric):
    error_distr: bool = False
    error_normality: bool = False

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_single(self.get_fingerprint())]


class AbsMaxErrorCalculation(LegacyRegressionSingleValueMetric[AbsMaxError]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(legacy_result.current.abs_error_max),
            None if legacy_result.reference is None else self.result(legacy_result.reference.abs_error_max),
        )

    def display_name(self) -> str:
        return "Absolute Max Error"


class LegacyRegressionDummyMeanStdMetric(
    MeanStdCalculation[TMeanStdMetric],
    LegacyMetricCalculation[MeanStdValue, TMeanStdMetric, RegressionDummyMetricResults, RegressionDummyMetric],
    Generic[TMeanStdMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        return _gen_regression_input_data(context)


class LegacyRegressionDummyValueMetric(
    SingleValueCalculation[TSingleValueMetric],
    LegacyMetricCalculation[SingleValue, TSingleValueMetric, RegressionDummyMetricResults, RegressionDummyMetric],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        return _gen_regression_input_data(context)


class DummyMAE(SingleValueMetric):
    pass


class DummyMAECalculation(LegacyRegressionDummyValueMetric[DummyMAE]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: RegressionDummyMetricResults,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        if legacy_result.mean_abs_error is None:
            raise ValueError("No mean absolute error was calculated")
        return self.result(legacy_result.mean_abs_error)

    def display_name(self) -> str:
        return "Dummy Mean Absolute Error"


class DummyMAPE(SingleValueMetric):
    pass


class DummyMAPECalculation(LegacyRegressionDummyValueMetric[DummyMAPE]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: RegressionDummyMetricResults,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        if legacy_result.mean_abs_perc_error is None:
            raise ValueError("No mean absolute percentage error was calculated")
        return self.result(legacy_result.mean_abs_perc_error)

    def display_name(self) -> str:
        return "Dummy Mean Absolute Percentage Error"


class DummyRMSE(SingleValueMetric):
    pass


class DummyRMSECalculation(LegacyRegressionDummyValueMetric[DummyRMSE]):
    def calculate_value(
        self,
        context: "Context",
        legacy_result: RegressionDummyMetricResults,
        render: List[BaseWidgetInfo],
    ) -> SingleValue:
        if legacy_result.rmse is None:
            raise ValueError("No RMSE was calculated")
        return self.result(legacy_result.rmse)

    def display_name(self) -> str:
        return "Dummy RMSE"
