import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.core import ColumnType
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.metric_types import BoundTest
from evidently.future.metric_types import ByLabelCalculation
from evidently.future.metric_types import ByLabelMetric
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import CountCalculation
from evidently.future.metric_types import CountMetric
from evidently.future.metric_types import CountValue
from evidently.future.metric_types import MetricTest
from evidently.future.metric_types import MetricTestProto
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueBoundTest
from evidently.future.metric_types import SingleValueCalculation
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metric_types import TMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.report import Context
from evidently.future.tests import Reference
from evidently.future.tests import eq
from evidently.future.tests import lt
from evidently.metric_results import DatasetColumns
from evidently.metric_results import DatasetUtilityColumns
from evidently.metric_results import HistogramData
from evidently.metric_results import Label
from evidently.metric_results import ScatterField
from evidently.metrics import DatasetDriftMetric
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetricResults
from evidently.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
from evidently.options.base import Options
from evidently.options.data_drift import DataDriftOptions
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.tests.base_test import TestStatus
from evidently.utils.visualizations import get_distribution_for_column
from evidently.utils.visualizations import plot_agg_line_data
from evidently.utils.visualizations import plot_distr_with_perc_button
from evidently.utils.visualizations import plot_scatter_for_data_drift


def distribution(
    title: str,
    current: DatasetColumn,
    reference: Optional[DatasetColumn],
) -> List[BaseWidgetInfo]:
    distr_cur, distr_ref = get_distribution_for_column(
        column_type=current.type.value,
        current=current.data,
        reference=reference.data if reference is not None else None,
    )
    distr_fig = plot_distr_with_perc_button(
        hist_curr=HistogramData.from_distribution(distr_cur),
        hist_ref=HistogramData.from_distribution(distr_ref),
        xaxis_name="",
        yaxis_name="Count",
        yaxis_name_perc="Percent",
        same_color=False,
        color_options=ColorOptions(),
        subplots=False,
        to_json=False,
        current_name="current",
        reference_name="reference",
    )

    return [
        plotly_figure(title=title, figure=distr_fig, size=WidgetSize.FULL),
    ]


class StatisticsMetric(SingleValueMetric):
    column: str

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [eq(Reference(relative=0.1)).bind_single(self.get_fingerprint())]


TStatisticsMetric = TypeVar("TStatisticsMetric", bound=StatisticsMetric)


class StatisticsCalculation(SingleValueCalculation[TStatisticsMetric]):
    @property
    def column(self):
        return self.metric.column

    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        value = self.calculate_value(current_data.column(self.column))

        header = f"current: {value:.3f}"
        ref_value = None
        if reference_data is not None:
            ref_value = self.calculate_value(reference_data.column(self.column))
            header += f", reference: {ref_value:.3f}"
        result = SingleValue(value)
        result.widget = distribution(
            f"{self.display_name()}: {header}",
            current_data.column(self.column),
            None if reference_data is None else reference_data.column(self.column),
        )
        return (
            result,
            None if ref_value is None else SingleValue(ref_value),
        )

    @abc.abstractmethod
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        raise NotImplementedError()


class MinValue(StatisticsMetric):
    pass


class MinValueCalculation(StatisticsCalculation[MinValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.min()

    def display_name(self) -> str:
        return f"Minimal value of {self.column}"


class MeanValue(StatisticsMetric):
    pass


class MeanValueCalculation(StatisticsCalculation[MeanValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.mean()

    def display_name(self) -> str:
        return f"Mean value of {self.column}"


class MaxValue(StatisticsMetric):
    pass


class MaxValueCalculation(StatisticsCalculation[MaxValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.max()

    def display_name(self) -> str:
        return f"Maximum value of {self.column}"


class StdValue(StatisticsMetric):
    pass


class StdValueCalculation(StatisticsCalculation[StdValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.std()

    def display_name(self) -> str:
        return f"Std value of {self.column}"


class MedianValue(StatisticsMetric):
    pass


class MedianValueCalculation(StatisticsCalculation[MedianValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.median()

    def display_name(self) -> str:
        return f"Median value of {self.column}"


class QuantileValue(StatisticsMetric):
    quantile: float = 0.5


class QuantileValueCalculation(StatisticsCalculation[QuantileValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.quantile(self.metric.quantile)

    def display_name(self) -> str:
        return f"Quantile {self.metric.quantile} of {self.column}"


class CategoryCount(CountMetric):
    class Config:
        smart_union = True

    column: str
    category: Union[bool, Label]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class CategoryCountCalculation(CountCalculation[CategoryCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' category '{self.metric.category}'"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        try:
            value = column.data.value_counts().loc[self.metric.category]
        except KeyError:
            value = 0
        total = column.data.count()
        return CountValue(value, value / total)


class InRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class InRangeValueCountCalculation(CountCalculation[InRangeValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values in range {self.metric.left} to {self.metric.right}"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        value = column.data.between(self.metric.left, self.metric.right).sum()
        total = column.data.count()
        return CountValue(value, value / total)


class OutRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class OutRangeValueCountCalculation(CountCalculation[OutRangeValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values out of range {self.metric.left} to {self.metric.right}"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        value = column.data.between(self.metric.left, self.metric.right).sum()
        total = column.data.count()
        return CountValue(total - value, (total - value) / total)


class InListValueCount(CountMetric):
    column: str
    values: List[Label]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class InListValueCountCalculation(CountCalculation[InListValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values in list [{', '.join(str(x) for x in self.metric.values)}]"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        value = column.data.value_counts().loc[self.metric.values].sum()  # type: ignore[index]
        total = column.data.count()
        return CountValue(value, value / total)


class OutListValueCount(CountMetric):
    column: str
    values: List[Label]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class OutListValueCountCalculation(CountCalculation[OutListValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values out of list [{', '.join(str(x) for x in self.metric.values)}]"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        value = column.data.value_counts().loc[self.metric.values].sum()  # type: ignore[index]
        total = column.data.count()
        return CountValue(total - value, (total - value) / total)


class MissingValueCount(CountMetric):
    column: str

    def _default_tests(self, context: Context) -> List[BoundTest]:
        return [eq(0).bind_count(self.get_fingerprint(), is_count=True)]

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), True),
            eq(Reference(relative=0.1)).bind_count(self.get_fingerprint(), False),
        ]


class MissingValueCountCalculation(CountCalculation[MissingValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        return (
            self._calculate_value(current_data),
            None if reference_data is None else self._calculate_value(reference_data),
        )

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' missing values"

    def _calculate_value(self, dataset: Dataset):
        column = dataset.column(self.metric.column)
        value = column.data.count()
        total = len(column.data)
        return CountValue(total - value, (total - value) / total)


class ValueDrift(SingleValueMetric):
    column: str
    method: Optional[str] = None
    threshold: Optional[float] = None


class ValueDriftTest(MetricTest):
    def to_test(self) -> MetricTestProto:
        raise NotImplementedError()


class ValueDriftCalculation(SingleValueCalculation[ValueDrift]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        column = self.metric.column
        column_type = current_data.column(column).type
        if reference_data is None:
            raise ValueError("Reference data is required for Value Drift")
        options = DataDriftOptions(
            all_features_stattest=self.metric.method,
            all_features_threshold=self.metric.threshold,
        )

        drift = get_one_column_drift(
            current_data=current_data.as_dataframe(),
            reference_data=reference_data.as_dataframe(),
            column_name=column,
            options=options,
            dataset_columns=DatasetColumns(
                utility_columns=DatasetUtilityColumns(),
                num_feature_names=[column] if column_type == ColumnType.Numerical else [],
                cat_feature_names=[column] if column_type == ColumnType.Categorical else [],
                text_feature_names=[column] if column_type == ColumnType.Text else [],
                datetime_feature_names=[column] if column_type == ColumnType.Datetime else [],
            ),
            column_type=column_type,
            agg_data=True,
        )

        result = SingleValue(drift.drift_score)
        result.widget = self._render(drift, Options(), ColorOptions())
        if self.metric.tests is None and context.configuration.include_tests:
            # todo: move to _default_tests
            result.set_tests(
                {
                    SingleValueBoundTest(
                        metric_fingerprint=self.metric.get_fingerprint(), test=ValueDriftTest()
                    ): MetricTestResult(
                        "drift",
                        f"Value Drift for column {self.metric.column}",
                        f"Drift score is {drift.drift_score:0.2f}. "
                        f"The drift detection method is {drift.stattest_name}. "
                        f"The drift threshold is {drift.stattest_threshold:0.2f}.",
                        status=TestStatus.FAIL if drift.drift_detected else TestStatus.SUCCESS,
                    )
                }
            )
        return result

    def display_name(self) -> str:
        return f"Value drift for {self.metric.column}"

    def _render(self, result: ColumnDataDriftMetrics, options, color_options):
        if result.drift_detected:
            drift = "detected"

        else:
            drift = "not detected"

        drift_score = round(result.drift_score, 3)
        tabs = []
        if result.scatter is not None:
            if options.render_options.raw_data:
                if not isinstance(result.scatter, ScatterField):
                    raise ValueError("Result have incompatible type")
                scatter_fig = plot_scatter_for_data_drift(
                    curr_y=result.scatter.scatter[result.column_name].tolist(),
                    curr_x=result.scatter.scatter[result.scatter.x_name].tolist(),
                    y0=result.scatter.plot_shape["y0"],
                    y1=result.scatter.plot_shape["y1"],
                    y_name=result.column_name,
                    x_name=result.scatter.x_name,
                    color_options=color_options,
                )
            else:
                scatter_fig = plot_agg_line_data(
                    curr_data=result.scatter.scatter,
                    ref_data=None,
                    line=(result.scatter.plot_shape["y0"] + result.scatter.plot_shape["y1"]) / 2,
                    std=(result.scatter.plot_shape["y0"] - result.scatter.plot_shape["y1"]) / 2,
                    xaxis_name=result.scatter.x_name,
                    xaxis_name_ref=None,
                    yaxis_name=f"{result.column_name} (mean +/- std)",
                    color_options=color_options,
                    return_json=False,
                    line_name="reference (mean)",
                )
            tabs.append(TabData("DATA DRIFT", plotly_figure(title="", figure=scatter_fig)))

        if result.current.distribution is not None and result.reference.distribution is not None:
            distr_fig = plot_distr_with_perc_button(
                hist_curr=HistogramData.from_distribution(result.current.distribution),
                hist_ref=HistogramData.from_distribution(result.reference.distribution),
                xaxis_name="",
                yaxis_name="Count",
                yaxis_name_perc="Percent",
                same_color=False,
                color_options=color_options,
                subplots=False,
                to_json=False,
            )
            tabs.append(TabData("DATA DISTRIBUTION", plotly_figure(title="", figure=distr_fig)))

        if (
            result.current.characteristic_examples is not None
            and result.reference.characteristic_examples is not None
            and result.current.characteristic_words is not None
            and result.reference.characteristic_words is not None
        ):
            current_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.characteristic_words],
            )
            reference_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.characteristic_words],
            )
            current_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.characteristic_examples],
            )
            reference_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.characteristic_examples],
            )

            tabs = [
                TabData(title="current: characteristic words", widget=current_table_words),
                TabData(
                    title="reference: characteristic words",
                    widget=reference_table_words,
                ),
                TabData(
                    title="current: characteristic examples",
                    widget=current_table_examples,
                ),
                TabData(
                    title="reference: characteristic examples",
                    widget=reference_table_examples,
                ),
            ]
        render_result = [
            counter(
                counters=[
                    CounterData(
                        (
                            f"Data drift {drift}. "
                            f"Drift detection method: {result.stattest_name}. "
                            f"Drift score: {drift_score}"
                        ),
                        f"Drift in column '{result.column_name}'",
                    )
                ],
                title="",
            )
        ]
        if len(tabs) > 0:
            render_result.append(
                widget_tabs(
                    title="",
                    tabs=tabs,
                )
            )
        return render_result


class DriftedColumnsCount(CountMetric):
    columns: Optional[List[str]] = None
    embeddings: Optional[List[str]] = None
    embeddings_drift_method: Optional[Dict[str, DriftMethod]] = None
    drift_share: float = 0.5
    method: Optional[PossibleStatTestType] = None
    cat_method: Optional[PossibleStatTestType] = None
    num_method: Optional[PossibleStatTestType] = None
    text_method: Optional[PossibleStatTestType] = None
    per_column_method: Optional[Dict[str, PossibleStatTestType]] = None
    threshold: Optional[float] = None
    cat_threshold: Optional[float] = None
    num_threshold: Optional[float] = None
    text_threshold: Optional[float] = None
    per_column_threshold: Optional[Dict[str, float]] = None

    def _default_tests_with_reference(self, context: Context) -> List[BoundTest]:
        return [lt(self.drift_share).bind_count(self.get_fingerprint(), is_count=False)]


class LegacyDriftedColumnsMetric(
    LegacyMetricCalculation[CountValue, TMetric, DatasetDriftMetricResults, DatasetDriftMetric],
    Generic[TMetric],
    abc.ABC,
):
    pass


class DriftedColumnCalculation(CountCalculation[DriftedColumnsCount], LegacyDriftedColumnsMetric[DriftedColumnsCount]):
    def legacy_metric(self) -> DatasetDriftMetric:
        return DatasetDriftMetric(
            columns=self.metric.columns,
            drift_share=self.metric.drift_share,
            stattest=self.metric.method,
            cat_stattest=self.metric.cat_method,
            num_stattest=self.metric.num_method,
            text_stattest=self.metric.text_method,
            per_column_stattest=self.metric.per_column_method,
            stattest_threshold=self.metric.threshold,
            cat_stattest_threshold=self.metric.cat_threshold,
            num_stattest_threshold=self.metric.num_threshold,
            text_stattest_threshold=self.metric.text_threshold,
            per_column_stattest_threshold=self.metric.per_column_threshold,
        )

    def calculate_value(
        self, context: Context, legacy_result: DatasetDriftMetricResults, render: List[BaseWidgetInfo]
    ) -> CountValue:
        result = CountValue(legacy_result.number_of_drifted_columns, legacy_result.share_of_drifted_columns)
        return result

    def display_name(self) -> str:
        return "Count of Drifted Columns"

    def share_display_name(self) -> str:
        return "Share of Drifted Columns"


class UniqueValueCount(ByLabelMetric):
    column: str


class UniqueValueCountCalculation(ByLabelCalculation[UniqueValueCount]):
    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]):
        current_result = self._calculate_value(current_data)
        current_result.widget = distribution(
            f"Unique value count: {self.metric.column}",
            current_data.column(self.metric.column),
            None if reference_data is None else reference_data.column(self.metric.column),
        )
        reference_result = None if reference_data is None else self._calculate_value(reference_data)
        return (
            current_result,
            reference_result,
        )

    def display_name(self) -> str:
        return "Unique Value Count"

    def _calculate_value(self, dataset: Dataset):
        value_counts = dataset.as_dataframe()[self.metric.column].value_counts(dropna=False)
        result = ByLabelValue(value_counts.to_dict())  # type: ignore[arg-type]
        return result
