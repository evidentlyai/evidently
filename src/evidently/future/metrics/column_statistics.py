import abc
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from evidently.future.datasets import Dataset
from evidently.future.datasets import DatasetColumn
from evidently.future.metrics import SingleValue
from evidently.future.metrics.base import CountCalculation
from evidently.future.metrics.base import CountMetric
from evidently.future.metrics.base import CountValue
from evidently.future.metrics.base import SingleValueCalculation
from evidently.future.metrics.base import SingleValueMetric
from evidently.metric_results import HistogramData
from evidently.metric_results import Label
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
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
        return self.config.column

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


class MinValueConfig(StatisticsMetric):
    pass


class MinValueCalculation(StatisticsCalculation[MinValueConfig]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.min()

    def display_name(self) -> str:
        return f"Minimal value of {self.column}"


class MeanValueConfig(StatisticsMetric):
    pass


class MeanValueCalculation(StatisticsCalculation[MeanValueConfig]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.mean()

    def display_name(self) -> str:
        return f"Mean value of {self.column}"


class MaxValueConfig(StatisticsMetric):
    pass


class MaxValueCalculation(StatisticsCalculation[MaxValueConfig]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.max()

    def display_name(self) -> str:
        return f"Maximum value of {self.column}"


class StdValueConfig(StatisticsMetric):
    pass


class StdValueCalculation(StatisticsCalculation[StdValueConfig]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.std()

    def display_name(self) -> str:
        return f"Std value of {self.column}"


class MedianValueConfig(StatisticsMetric):
    pass


class MedianValueCalculation(StatisticsCalculation[MedianValueConfig]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.median()

    def display_name(self) -> str:
        return f"Median value of {self.column}"


class QuantileValue(StatisticsMetric):
    quantile: float = 0.5


class QuantileValueCalculation(StatisticsCalculation[QuantileValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.quantile(self.config.quantile)

    def display_name(self) -> str:
        return f"Quantile {self.config.quantile} of {self.column}"


class CategoryCount(CountMetric):
    column: str
    category: Label


class CategoryCountCalculation(CountCalculation[CategoryCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.value_counts()[self.config.category]
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' category '{self.config.category}'"


class InRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]


class InRangeValueCountCalculation(CountCalculation[InRangeValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.between(self.config.left, self.config.right).count()
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' values in range {self.config.left} to {self.config.right}"


class OutRangeValueCount(CountMetric):
    column: str
    left: Union[int, float]
    right: Union[int, float]


class OutRangeValueCountCalculation(CountCalculation[OutRangeValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.between(self.config.left, self.config.right).count()
        total = column.data.count()
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' values out of range {self.config.left} to {self.config.right}"


class InListValueCount(CountMetric):
    column: str
    values: List[Label]


class InListValueCountCalculation(CountCalculation[InListValueCount]):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.value_counts()[self.config.values].sum()
        total = column.data.count()
        return CountValue(value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' values in list [{', '.join(self.config.values)}]"


class OutListValueCount(CountMetric):
    column: str
    values: List[Label]


class OutListValueCountCalculation(CountCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.value_counts()[self.config.values].sum()
        total = column.data.count()
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' values out of list [{', '.join(self.config.values)}]"


class MissingValueCount(CountMetric):
    column: str


class MissingValueCountCalculation(CountCalculation):
    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> CountValue:
        column = current_data.column(self.config.column)
        value = column.data.count()
        total = len(column.data)
        return CountValue(total - value, value / total)

    def display_name(self) -> str:
        return f"Column '{self.config.column}' missing values"
