import abc
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from evidently import ColumnType
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.metric_types import ByLabelCalculation
from evidently.future.metric_types import ByLabelMetric
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import CountCalculation
from evidently.future.metric_types import CountMetric
from evidently.future.metric_types import CountValue
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import SingleValueCalculation
from evidently.future.metric_types import SingleValueMetric
from evidently.future.metric_types import TMetric
from evidently.future.metrics._legacy import LegacyMetricCalculation
from evidently.future.report import Context
from evidently.metric_results import DatasetColumns
from evidently.metric_results import DatasetUtilityColumns
from evidently.metric_results import HistogramData
from evidently.metric_results import Label
from evidently.metrics import DatasetDriftMetric
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetricResults
from evidently.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
from evidently.options.data_drift import DataDriftOptions
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.visualizations import get_distribution_for_column
from evidently.utils.visualizations import plot_distr_with_perc_button


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


TStatisticsMetric = TypeVar("TStatisticsMetric", bound=StatisticsMetric)


class StatisticsCalculation(SingleValueCalculation[TStatisticsMetric]):
    @property
    def column(self):
        return self.metric.column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        value = self.calculate_value(current_data.column(self.column))

        header = f"current: {value:.3f}"
        if reference_data is not None:
            ref_value = self.calculate_value(reference_data.column(self.column))
            header += f", reference: {ref_value:.3f}"
        result = SingleValue(value)
        result.widget = distribution(
            f"{self.display_name()}: {header}",
            current_data.column(self.column),
            None if reference_data is None else reference_data.column(self.column),
        )
        return result

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
    column: str
    category: Label


class CategoryCountCalculation(CountCalculation[CategoryCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        try:
            value = column.data.value_counts()[self.metric.category]
        except KeyError:
            value = 0
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' category '{self.metric.category}'"


class InRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]


class InRangeValueCountCalculation(CountCalculation[InRangeValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        value = column.data.between(self.metric.left, self.metric.right).count()
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values in range {self.metric.left} to {self.metric.right}"


class OutRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]


class OutRangeValueCountCalculation(CountCalculation[OutRangeValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        value = column.data.between(self.metric.left, self.metric.right).count()
        total = column.data.count()
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values out of range {self.metric.left} to {self.metric.right}"


class InListValueCount(CountMetric):
    column: str
    values: List[Label]


class InListValueCountCalculation(CountCalculation[InListValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        value = column.data.value_counts()[self.metric.values].sum()  # type: ignore[index]
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values in list [{', '.join(str(x) for x in self.metric.values)}]"


class OutListValueCount(CountMetric):
    column: str
    values: List[Label]


class OutListValueCountCalculation(CountCalculation[OutListValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        value = column.data.value_counts()[self.metric.values].sum()  # type: ignore[index]
        total = column.data.count()
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' values out of list [{', '.join(str(x) for x in self.metric.values)}]"


class MissingValueCount(CountMetric):
    column: str


class MissingValueCountCalculation(CountCalculation[MissingValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.metric.column)
        value = column.data.count()
        total = len(column.data)
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.metric.column}' missing values"


class ValueDrift(SingleValueMetric):
    column: str
    method: Optional[str] = None


class ValueDriftCalculation(SingleValueCalculation[ValueDrift]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        column = self.metric.column
        column_type = current_data.column(column).type
        if reference_data is None:
            raise ValueError("Reference data is required for Value Drift")
        drift = get_one_column_drift(
            current_data=current_data.as_dataframe(),
            reference_data=reference_data.as_dataframe(),
            column_name=column,
            options=DataDriftOptions(all_features_stattest=self.metric.method),
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

        return SingleValue(drift.drift_score)

    def display_name(self) -> str:
        return f"Value drift for {self.metric.column}"


class DriftedColumnsCount(CountMetric):
    columns: Optional[List[str]] = None
    embeddings: Optional[List[str]] = None
    embeddings_drift_method: Optional[Dict[str, DriftMethod]] = None
    drift_share: float = 0.5
    stattest: Optional[PossibleStatTestType] = None
    cat_stattest: Optional[PossibleStatTestType] = None
    num_stattest: Optional[PossibleStatTestType] = None
    text_stattest: Optional[PossibleStatTestType] = None
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None
    stattest_threshold: Optional[float] = None
    cat_stattest_threshold: Optional[float] = None
    num_stattest_threshold: Optional[float] = None
    text_stattest_threshold: Optional[float] = None
    per_column_stattest_threshold: Optional[Dict[str, float]] = None


class LegacyDriftedColumnsMetric(
    LegacyMetricCalculation[CountValue, TMetric, DatasetDriftMetricResults, DatasetDriftMetric],
    Generic[TMetric],
    abc.ABC,
):
    pass


class DriftedColumnCalculation(LegacyDriftedColumnsMetric[DriftedColumnsCount]):
    def legacy_metric(self) -> DatasetDriftMetric:
        return DatasetDriftMetric(
            columns=self.metric.columns,
            drift_share=self.metric.drift_share,
            stattest=self.metric.stattest,
            cat_stattest=self.metric.cat_stattest,
            num_stattest=self.metric.num_stattest,
            text_stattest=self.metric.text_stattest,
            per_column_stattest=self.metric.per_column_stattest,
            stattest_threshold=self.metric.stattest_threshold,
            cat_stattest_threshold=self.metric.cat_stattest_threshold,
            num_stattest_threshold=self.metric.num_stattest_threshold,
            text_stattest_threshold=self.metric.text_stattest_threshold,
            per_column_stattest_threshold=self.metric.per_column_stattest_threshold,
        )

    def calculate_value(
        self, context: Context, legacy_result: DatasetDriftMetricResults, render: List[BaseWidgetInfo]
    ) -> CountValue:
        result = CountValue(legacy_result.number_of_drifted_columns, legacy_result.share_of_drifted_columns)
        return result

    def display_name(self) -> str:
        return "Count of Drifted Columns"


class UniqueValueCount(ByLabelMetric):
    column: str


class UniqueValueCountCalculation(ByLabelCalculation[UniqueValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> ByLabelValue:
        value_counts = current_data.as_dataframe()[self.metric.column].value_counts()
        return ByLabelValue(value_counts.to_dict())  # type: ignore[arg-type]

    def display_name(self) -> str:
        return "Unique Value Count"
