import abc
from typing import Generic
from typing import List

from evidently.base_metric import InputData
from evidently.future.metric_types import MeanStdMetric
from evidently.future.metric_types import MeanStdValue
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metric_types import TMeanStdMetric
from evidently.future.metric_types import TSingleValueMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.report import Context
from evidently.metrics import RegressionDummyMetric
from evidently.metrics.regression_performance.regression_dummy_metric import RegressionDummyMetricResults
from evidently.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.metrics.regression_performance.regression_quality import RegressionQualityMetricResults
from evidently.model.widget import BaseWidgetInfo
from evidently.utils.data_preprocessing import create_data_definition


class LegacyRegressionMeanStdMetric(
    LegacyMetricCalculation[MeanStdValue, TMeanStdMetric, RegressionQualityMetricResults, RegressionQualityMetric],
    Generic[TMeanStdMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        default_data = super()._gen_input_data(context)
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


class LegacyRegressionSingleValueMetric(
    LegacyMetricCalculation[SingleValue, TSingleValueMetric, RegressionQualityMetricResults, RegressionQualityMetric],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionQualityMetric:
        return RegressionQualityMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        default_data = super()._gen_input_data(context)
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


class MeanError(MeanStdMetric):
    pass


class MeanErrorCalculation(LegacyRegressionMeanStdMetric[MeanError]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            MeanStdValue(legacy_result.current.mean_error, legacy_result.current.error_std),
            None
            if legacy_result.reference is None
            else MeanStdValue(legacy_result.reference.mean_error, legacy_result.reference.error_std),
        )

    def display_name(self) -> str:
        return "Mean Error"


class MAE(MeanStdMetric):
    pass


class MAECalculation(LegacyRegressionMeanStdMetric[MAE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            MeanStdValue(legacy_result.current.mean_abs_error, legacy_result.current.abs_error_std),
            None
            if legacy_result.reference is None
            else MeanStdValue(legacy_result.reference.mean_abs_error, legacy_result.reference.abs_error_std),
        )

    def display_name(self) -> str:
        return "Mean Absolute Error"


class RMSE(SingleValueMetric):
    pass


class RMSECalculation(LegacyRegressionSingleValueMetric[RMSE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            SingleValue(legacy_result.current.rmse),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.rmse),
        )

    def display_name(self) -> str:
        return "RMSE"


class MAPE(MeanStdMetric):
    pass


class MAPECalculation(LegacyRegressionMeanStdMetric[MAPE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            MeanStdValue(legacy_result.current.mean_abs_perc_error, legacy_result.current.abs_perc_error_std),
            None
            if legacy_result.reference is None
            else MeanStdValue(legacy_result.reference.mean_abs_perc_error, legacy_result.reference.abs_perc_error_std),
        )

    def display_name(self) -> str:
        return "Mean Absolute Percentage Error"


class R2Score(SingleValueMetric):
    pass


class R2ScoreCalculation(LegacyRegressionSingleValueMetric[R2Score]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            SingleValue(legacy_result.current.r2_score),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.r2_score),
        )

    def display_name(self) -> str:
        return "R2 Score"


class AbsMaxError(SingleValueMetric):
    pass


class AbsMaxErrorCalculation(LegacyRegressionSingleValueMetric[AbsMaxError]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            SingleValue(legacy_result.current.abs_error_max),
            None if legacy_result.reference is None else SingleValue(legacy_result.reference.abs_error_max),
        )

    def display_name(self) -> str:
        return "Absolute Max Error"


class LegacyRegressionDummyMeanStdMetric(
    LegacyMetricCalculation[MeanStdValue, TMeanStdMetric, RegressionDummyMetricResults, RegressionDummyMetric],
    Generic[TMeanStdMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        default_data = super()._gen_input_data(context)
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


class LegacyRegressionDummyValueMetric(
    LegacyMetricCalculation[SingleValue, TSingleValueMetric, RegressionDummyMetricResults, RegressionDummyMetric],
    Generic[TSingleValueMetric],
    abc.ABC,
):
    def legacy_metric(self) -> RegressionDummyMetric:
        return RegressionDummyMetric()

    def _gen_input_data(self, context: "Context") -> InputData:
        default_data = super()._gen_input_data(context)
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
        return SingleValue(legacy_result.mean_abs_error)

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
        return SingleValue(legacy_result.mean_abs_perc_error)

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
        return SingleValue(legacy_result.rmse)

    def display_name(self) -> str:
        return "Dummy RMSE"
