import abc
from typing import List
from typing import Optional
from typing import Union

from evidently.metric_results import HistogramData
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.visualizations import get_distribution_for_column
from evidently.utils.visualizations import plot_distr_with_perc_button
from evidently.v2.datasets import Dataset
from evidently.v2.datasets import DatasetColumn
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import SingleValueMetricTest
from evidently.v2.metrics.base import SingleValueMetric


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
    def __init__(self, metric_id: str, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(metric_id)
        self.with_tests(tests)
        self._column = column

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> SingleValue:
        value = self.calculate_value(current_data.column(self._column))

        header = f"current: {value:.3f}"
        if reference_data is not None:
            ref_value = self.calculate_value(reference_data.column(self._column))
            header += f", reference: {ref_value:.3f}"
        result = SingleValue(value)
        result.widget = distribution(
            f"{self.display_name()}: {header}",
            current_data.column(self._column),
            None if reference_data is None else reference_data.column(self._column),
        )
        return result

    @abc.abstractmethod
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        raise NotImplementedError()


class MinValue(StatisticsMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"min:{column}", column, tests)

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.min()

    def display_name(self) -> str:
        return f"Minimal value of {self._column}"


class MeanValue(StatisticsMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"mean:{column}", column, tests)

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.mean()

    def display_name(self) -> str:
        return f"Mean value of {self._column}"


class MaxValue(StatisticsMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"max:{column}", column, tests)

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.max()

    def display_name(self) -> str:
        return f"Maximum value of {self._column}"


class StdValue(StatisticsMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"std:{column}", column, tests)
        self.with_tests(tests)
        self._column = column

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.std()

    def display_name(self) -> str:
        return f"Std value of {self._column}"


class MedianValue(StatisticsMetric):
    def __init__(self, column: str, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"median:{column}", column, tests)

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.median()

    def display_name(self) -> str:
        return f"Median value of {self._column}"


class QuantileValue(StatisticsMetric):
    def __init__(self, column: str, quantile: float = 0.5, tests: Optional[List[SingleValueMetricTest]] = None):
        super().__init__(f"quantile:{quantile}:{column}", column, tests)
        self.with_tests(tests)
        self._quantile = quantile
        self._column = column

    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.quantile(self._quantile)

    def display_name(self) -> str:
        return f"Quantile {self._quantile} of {self._column}"
