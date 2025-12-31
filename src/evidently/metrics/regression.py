import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import MeanStdCalculation
from evidently.core.metric_types import MeanStdMetric
from evidently.core.metric_types import MeanStdValue
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import SingleValueCalculation
from evidently.core.metric_types import SingleValueMetric
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


def _gen_regression_input_data(context: "Context", task_name: Optional[str]) -> InputData:
    default_data = _default_input_data_generator(context, task_name)
    if task_name is None:
        return default_data
    regression = context.data_definition.get_regression(task_name)
    if regression is None:
        raise ValueError(f"No regression '{task_name}' in data definition")
    default_data.column_mapping.target = regression.target
    default_data.column_mapping.prediction = regression.prediction

    definition = create_data_definition(
        default_data.reference_data,
        default_data.current_data,
        default_data.column_mapping,
    )
    default_data.data_definition = definition
    return default_data


class SingleValueRegressionMetric(SingleValueMetric):
    regression_name: str = "default"


class MeanStdRegressionMetric(MeanStdMetric):
    regression_name: str = "default"


TSingleValueRegressionMetric = TypeVar("TSingleValueRegressionMetric", bound=SingleValueRegressionMetric)
TMeanStdRegressionMetric = TypeVar("TMeanStdRegressionMetric", bound=MeanStdRegressionMetric)


class LegacyRegressionMeanStdMetric(
    MeanStdCalculation[TMeanStdRegressionMetric],
    LegacyMetricCalculation[
        MeanStdValue, TMeanStdRegressionMetric, RegressionQualityMetricResults, RegressionQualityMetric
    ],
    Generic[TMeanStdRegressionMetric],
    abc.ABC,
):
    def task_name(self) -> str:
        return self.metric.regression_name

    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, _gen_regression_input_data, self.task_name())
                result += widgets
        return result

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_regression_input_data(context, task_name)


class LegacyRegressionSingleValueMetric(
    SingleValueCalculation[TSingleValueRegressionMetric],
    LegacyMetricCalculation[
        SingleValue, TSingleValueRegressionMetric, RegressionQualityMetricResults, RegressionQualityMetric
    ],
    Generic[TSingleValueRegressionMetric],
    abc.ABC,
):
    def task_name(self) -> str:
        return self.metric.regression_name

    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def get_additional_widgets(self, context: "Context") -> List[BaseWidgetInfo]:
        result = []
        for field, metric in ADDITIONAL_WIDGET_MAPPING.items():
            if hasattr(self.metric, field) and getattr(self.metric, field):
                _, widgets = context.get_legacy_metric(metric, _gen_regression_input_data, self.task_name())
                result += widgets
        return result

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_regression_input_data(context, task_name)


class MeanError(MeanStdRegressionMetric):
    """Calculate mean error and standard deviation of errors for regression.

    Computes the average prediction error (prediction - target) and its standard deviation.
    Positive values indicate over-prediction, negative values indicate under-prediction.

    """

    error_plot: bool = True
    """Whether to show error plot visualization."""
    error_distr: bool = False
    """Whether to show error distribution."""
    error_normality: bool = False
    """Whether to show error normality test."""

    def __init__(self, **kwargs):
        if "tests" in kwargs:
            raise ValueError("'tests' is not a valid argument for MAE. Did you mean 'mean_tests=' or 'std_tests='?")
        super().__init__(**kwargs)

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

    def mean_display_name(self) -> str:
        return "Mean Error"

    def std_display_name(self) -> str:
        return "Std Error"


class MAE(MeanStdRegressionMetric):
    """Calculate Mean Absolute Error (MAE) for regression.

    MAE measures the average magnitude of errors without considering direction.
    Lower values indicate better performance. Returns both mean and standard deviation.

    """

    error_plot: bool = False
    """Whether to show error plot visualization."""
    error_distr: bool = True
    """Whether to show error distribution."""
    error_normality: bool = False
    """Whether to show error normality test."""

    def __init__(self, **kwargs):
        if "tests" in kwargs:
            raise ValueError("'tests' is not a valid argument for MAE. Did you mean 'mean_tests=' or 'std_tests='?")
        super().__init__(**kwargs)

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_mean_std(self.get_fingerprint(), True)]

    def _default_tests(self, context: "Context") -> List[BoundTest]:
        dv: SingleValue = context.calculate_metric(DummyMAE().to_calculation())
        return [lt(dv.value).bind_mean_std(self.get_fingerprint())]


class MAECalculation(LegacyRegressionMeanStdMetric[MAE]):
    def task_name(self) -> str:
        return self.metric.regression_name

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

    def mean_display_name(self) -> str:
        return "Mean Absolute Error"

    def std_display_name(self) -> str:
        return "Std Absolute Error"


class RMSE(SingleValueRegressionMetric):
    """Calculate Root Mean Squared Error (RMSE) for regression.

    RMSE measures the square root of the average squared errors. It penalizes
    large errors more than MAE. Lower values indicate better performance.

    """

    error_plot: bool = False
    """Whether to show error plot visualization."""
    error_distr: bool = True
    """Whether to show error distribution."""
    error_normality: bool = False
    """Whether to show error normality test."""

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


class MAPE(MeanStdRegressionMetric):
    """Calculate Mean Absolute Percentage Error (MAPE) for regression.

    MAPE expresses errors as a percentage of the actual values, making it
    scale-independent. Returns both mean and standard deviation. Lower values are better.

    """

    perc_error_plot: bool = True
    """Whether to show percentage error plot."""
    error_distr: bool = False
    """Whether to show error distribution."""

    def __init__(self, **kwargs):
        if "tests" in kwargs:
            raise ValueError("'tests' is not a valid argument for MAE. Did you mean 'mean_tests=' or 'std_tests='?")
        super().__init__(**kwargs)

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

    def mean_display_name(self) -> str:
        return "Mean Absolute Percentage Error"

    def std_display_name(self) -> str:
        return "Std Absolute Percentage Error"


class R2Score(SingleValueRegressionMetric):
    """Calculate R² (coefficient of determination) score for regression.

    R² measures how well the model explains the variance in the target variable.
    Values range from negative infinity to 1.0, with 1.0 being perfect fit.
    Higher values indicate better performance.

    """

    error_distr: bool = False
    """Whether to show error distribution."""
    error_normality: bool = False
    """Whether to show error normality test."""

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


class AbsMaxError(SingleValueRegressionMetric):
    """Calculate the maximum absolute error for regression.

    Returns the largest absolute error across all predictions. Useful for
    identifying worst-case prediction errors.

    """

    error_distr: bool = False
    """Whether to show error distribution."""
    error_normality: bool = False
    """Whether to show error normality test."""

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
    MeanStdCalculation[TMeanStdRegressionMetric],
    LegacyMetricCalculation[
        MeanStdValue, TMeanStdRegressionMetric, RegressionDummyMetricResults, RegressionDummyMetric
    ],
    Generic[TMeanStdRegressionMetric],
    abc.ABC,
):
    def task_name(self) -> str:
        return self.metric.regression_name

    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_regression_input_data(context, task_name)


class LegacyRegressionDummyValueMetric(
    SingleValueCalculation[TSingleValueRegressionMetric],
    LegacyMetricCalculation[
        SingleValue, TSingleValueRegressionMetric, RegressionDummyMetricResults, RegressionDummyMetric
    ],
    Generic[TSingleValueRegressionMetric],
    abc.ABC,
):
    def task_name(self) -> str:
        return self.metric.regression_name

    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context", task_name: Optional[str]) -> InputData:
        return _gen_regression_input_data(context, task_name)


class DummyMAE(SingleValueRegressionMetric):
    """Calculate Mean Absolute Error for a dummy/baseline regression model.

    Computes MAE using a simple baseline (e.g., always predict the mean).
    Useful as a baseline to compare your model against.

    """

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


class DummyMAPE(SingleValueRegressionMetric):
    """Calculate Mean Absolute Percentage Error for a dummy/baseline regression model.

    Computes MAPE using a simple baseline. Useful as a baseline to compare your model against.

    """

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


class DummyRMSE(SingleValueRegressionMetric):
    """Calculate Root Mean Squared Error for a dummy/baseline regression model.

    Computes RMSE using a simple baseline. Useful as a baseline to compare your model against.

    Args:
    * `regression_name`: Name of the regression task (default: "default").
    """

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
