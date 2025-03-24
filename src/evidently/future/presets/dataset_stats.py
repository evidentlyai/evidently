import dataclasses
from itertools import chain
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently.core import ColumnType
from evidently.future.container import ColumnMetricContainer
from evidently.future.container import MetricContainer
from evidently.future.container import MetricOrContainer
from evidently.future.metric_types import ByLabelCountValue
from evidently.future.metric_types import ByLabelMetricTests
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metric_types import SingleValueMetricTests
from evidently.future.metrics import ColumnCount
from evidently.future.metrics import DuplicatedRowCount
from evidently.future.metrics import MaxValue
from evidently.future.metrics import MeanValue
from evidently.future.metrics import MinValue
from evidently.future.metrics import QuantileValue
from evidently.future.metrics import RowCount
from evidently.future.metrics import StdValue
from evidently.future.metrics import UniqueValueCount
from evidently.future.metrics.column_statistics import MissingValueCount
from evidently.future.metrics.dataset_statistics import AlmostConstantColumnsCount
from evidently.future.metrics.dataset_statistics import AlmostDuplicatedColumnsCount
from evidently.future.metrics.dataset_statistics import ConstantColumnsCount
from evidently.future.metrics.dataset_statistics import DatasetMissingValueCount
from evidently.future.metrics.dataset_statistics import DuplicatedColumnsCount
from evidently.future.metrics.dataset_statistics import EmptyColumnsCount
from evidently.future.metrics.dataset_statistics import EmptyRowsCount
from evidently.future.report import Context
from evidently.future.report import _default_input_data_generator
from evidently.metric_results import Label
from evidently.metrics import DatasetSummaryMetric
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import link_metric
from evidently.renderers.html_widgets import rich_data


class ValueStats(ColumnMetricContainer):
    def __init__(
        self,
        column: str,
        row_count_tests: SingleValueMetricTests = None,
        missing_values_count_tests: SingleValueMetricTests = None,
        min_tests: SingleValueMetricTests = None,
        max_tests: SingleValueMetricTests = None,
        mean_tests: SingleValueMetricTests = None,
        std_tests: SingleValueMetricTests = None,
        q25_tests: SingleValueMetricTests = None,
        q50_tests: SingleValueMetricTests = None,
        q75_tests: SingleValueMetricTests = None,
        unique_values_count_tests: ByLabelMetricTests = None,
    ):
        super().__init__(column=column)
        self._row_count_tests = row_count_tests
        self._missing_values_count_tests = missing_values_count_tests
        self._min_tests = min_tests
        self._max_tests = max_tests
        self._mean_tests = mean_tests
        self._std_tests = std_tests
        self._q25_tests = q25_tests
        self._q50_tests = q50_tests
        self._q75_tests = q75_tests
        self._unique_values_count_tests = unique_values_count_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        metrics: List[Metric] = [
            RowCount(tests=self._row_count_tests),
            MissingValueCount(column=self._column, tests=self._missing_values_count_tests),
        ]
        column_type = context.column(self._column).column_type
        if column_type == ColumnType.Numerical:
            metrics += [
                MinValue(column=self._column, tests=self._min_tests),
                MaxValue(column=self._column, tests=self._max_tests),
                MeanValue(column=self._column, tests=self._mean_tests),
                StdValue(column=self._column, tests=self._std_tests),
                QuantileValue(column=self._column, quantile=0.25, tests=self._q25_tests),
                QuantileValue(column=self._column, quantile=0.5, tests=self._q50_tests),
                QuantileValue(column=self._column, quantile=0.75, tests=self._q75_tests),
            ]
        if column_type == ColumnType.Categorical:
            metrics += [
                UniqueValueCount(column=self._column, tests=self._unique_values_count_tests),
            ]
        if column_type == ColumnType.Datetime:
            metrics += [
                MinValue(column=self._column, tests=[]),
                MaxValue(column=self._column, tests=[]),
            ]
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        column_type = context.column(self._column).column_type
        widgets = []
        if column_type == ColumnType.Numerical:
            widgets = self._render_numerical(context)
        if column_type == ColumnType.Categorical:
            if len(context.column(self._column).labels()) <= 3:
                widgets = self._render_categorical_binary(context)
            else:
                widgets = self._render_categorical(context)
        if column_type == ColumnType.Datetime:
            widgets = self._render_datetime(context)
        if column_type == ColumnType.Text:
            widgets = self._render_text(context)
        for metric in self.list_metrics(context):
            link_metric(widgets, metric)
        return widgets

    def _render_numerical(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(
            MinValue(column=self._column, tests=self._min_tests).get_metric_id(),
        ).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self._column, tests=self._row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(
                                column=self._column,
                                tests=self._missing_values_count_tests,
                            ),
                        ),
                    },
                    {
                        "label": "min",
                        "values": self._get_metric(context, MinValue(column=self._column, tests=self._min_tests)),
                    },
                    {
                        "label": "max",
                        "values": self._get_metric(context, MaxValue(column=self._column, tests=self._max_tests)),
                    },
                    {
                        "label": "mean",
                        "values": self._get_metric(context, MeanValue(column=self._column, tests=self._mean_tests)),
                    },
                    {
                        "label": "std",
                        "values": self._get_metric(context, StdValue(column=self._column, tests=self._std_tests)),
                    },
                ],
                graph=result.params,
            )
        ]

    def _render_categorical(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(
            UniqueValueCount(column=self._column, tests=self._unique_values_count_tests),
        ).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self._column, tests=self._row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self._column, tests=self._missing_values_count_tests),
                        ),
                    },
                    {
                        "label": "most common",
                        "values": self._get_metric(
                            context,
                            UniqueValueCount(column=self._column, tests=self._unique_values_count_tests),
                            convert=self._most_common_value,
                        ),
                    },
                ],
                graph=result.params,
            )
        ]

    def _render_categorical_binary(self, context: "Context") -> List[BaseWidgetInfo]:
        unique_value_count = UniqueValueCount(column=self._column, tests=self._unique_values_count_tests)
        result = context.get_metric_result(
            unique_value_count,
        ).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self._column, tests=self._row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self._column, tests=self._missing_values_count_tests),
                        ),
                    },
                ]
                + [
                    {
                        "label": f"{label}",
                        "values": self._label_count(context, unique_value_count, label),
                    }
                    for label in context.column(self._column).labels()
                ],
                graph=result.params,
            )
        ]

    def _render_text(self, context: "Context") -> List[BaseWidgetInfo]:
        raise NotImplementedError()

    def _render_datetime(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(MinValue(column=self._column, tests=[]).get_metric_id()).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self._column, tests=self._row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self._column, tests=self._missing_values_count_tests),
                        ),
                    },
                    {"label": "min", "values": self._get_metric(context, MinValue(column=self._column, tests=[]))},
                    {"label": "max", "values": self._get_metric(context, MaxValue(column=self._column, tests=[]))},
                ],
                graph=result.params,
            )
        ]

    def _get_metric(
        self,
        context: "Context",
        metric: Metric,
        convert: Callable[[MetricResult], str] = lambda x: "{0:0.2f}".format(x),
    ) -> List[str]:
        if context.has_reference:
            return [
                convert(context.get_metric_result(metric)),
                convert(context.get_reference_metric_result(metric)),
            ]
        return [convert(context.get_metric_result(metric))]

    def _most_common_value(self, unique_value: MetricResult):
        if not isinstance(unique_value, ByLabelCountValue):
            raise ValueError("Most common value must be of type 'ByLabelCountValue'")
        first = sorted(unique_value.counts.items(), key=lambda x: x[1], reverse=True)[0]
        return f"Label: {first[0]} count: {first[1]}"

    def _label_count(
        self,
        context: "Context",
        metric: UniqueValueCount,
        label: Label,
    ):
        result = context.get_metric_result(metric)
        assert isinstance(result, ByLabelCountValue)
        if context.has_reference:
            ref_result = context.get_reference_metric_result(metric)
            assert isinstance(ref_result, ByLabelCountValue)
            return [
                f"{result.counts[label]} ({(result.shares[label] * 100):0.0f}%)",
                f"{ref_result.counts[label]} ({(ref_result.shares[label] * 100):0.0f}%)",
            ]
        return [
            f"{result.counts[label]} ({(result.shares[label] * 100):0.0f}%)",
        ]


class DatasetStats(MetricContainer):
    def __init__(
        self,
        row_count_tests: SingleValueMetricTests = None,
        column_count_tests: SingleValueMetricTests = None,
        duplicated_row_count_tests: SingleValueMetricTests = None,
        duplicated_column_count_tests: SingleValueMetricTests = None,
        almost_duplicated_column_count_tests: SingleValueMetricTests = None,
        almost_constant_column_count_tests: SingleValueMetricTests = None,
        empty_row_count_tests: SingleValueMetricTests = None,
        empty_column_count_tests: SingleValueMetricTests = None,
        constant_columns_count_tests: SingleValueMetricTests = None,
        dataset_missing_value_count_tests: SingleValueMetricTests = None,
    ):
        self.duplicated_row_count_tests = duplicated_row_count_tests
        self.duplicated_column_count_tests = duplicated_column_count_tests
        self.almost_constant_column_count_tests = almost_constant_column_count_tests
        self.almost_duplicated_column_count_tests = almost_duplicated_column_count_tests
        self.empty_row_count_tests = empty_row_count_tests
        self.empty_column_count_tests = empty_column_count_tests
        self.constant_columns_count_tests = constant_columns_count_tests
        self.dataset_missing_value_count_tests = dataset_missing_value_count_tests
        self.column_count_tests = column_count_tests
        self.row_count_tests = row_count_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            RowCount(tests=self.row_count_tests),
            ColumnCount(tests=self.column_count_tests),
            ColumnCount(column_type=ColumnType.Numerical, tests=[]),
            ColumnCount(column_type=ColumnType.Categorical, tests=[]),
            ColumnCount(column_type=ColumnType.Datetime, tests=[]),
            ColumnCount(column_type=ColumnType.Text, tests=[]),
            DuplicatedRowCount(tests=self.duplicated_row_count_tests),
            DuplicatedColumnsCount(tests=self.duplicated_column_count_tests),
            AlmostDuplicatedColumnsCount(tests=self.almost_duplicated_column_count_tests),
            AlmostConstantColumnsCount(tests=self.almost_constant_column_count_tests),
            EmptyRowsCount(tests=self.empty_row_count_tests),
            EmptyColumnsCount(tests=self.empty_column_count_tests),
            ConstantColumnsCount(tests=self.constant_columns_count_tests),
            DatasetMissingValueCount(tests=self.dataset_missing_value_count_tests),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        metric = DatasetSummaryMetric()
        _, render = context.get_legacy_metric(metric, _default_input_data_generator)
        for metric in self.list_metrics(context):
            link_metric(render, metric)
        return render


@dataclasses.dataclass
class ValueStatsTests:
    row_count_tests: SingleValueMetricTests = None
    missing_values_count_tests: SingleValueMetricTests = None
    min_tests: SingleValueMetricTests = None
    max_tests: SingleValueMetricTests = None
    mean_tests: SingleValueMetricTests = None
    std_tests: SingleValueMetricTests = None
    q25_tests: SingleValueMetricTests = None
    q50_tests: SingleValueMetricTests = None
    q75_tests: SingleValueMetricTests = None
    unique_values_count_tests: ByLabelMetricTests = None


class TextEvals(MetricContainer):
    def __init__(
        self,
        columns: Optional[List[str]] = None,
        row_count_tests: SingleValueMetricTests = None,
        column_tests: Optional[Dict[str, ValueStatsTests]] = None,
    ):
        self._columns = columns
        self._value_stats: List[ValueStats] = []
        self._row_count_tests = row_count_tests
        self._column_tests = column_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        if self._columns is None:
            cols = context.data_definition.numerical_descriptors + context.data_definition.categorical_descriptors
        else:
            cols = self._columns
        metrics: List[MetricOrContainer] = [RowCount(tests=self._row_count_tests)]
        self._value_stats = [
            ValueStats(column, **(self._column_tests or {}).get(column, ValueStatsTests()).__dict__) for column in cols
        ]
        metrics.extend(list(chain(*[vs.metrics(context)[1:] for vs in self._value_stats])))
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        return list(chain(*[vs.render(context) for vs in self._value_stats]))


class DataSummaryPreset(MetricContainer):
    _dataset_stats: Optional[DatasetStats] = None
    _text_evals: Optional[TextEvals] = None

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        row_count_tests: SingleValueMetricTests = None,
        column_count_tests: SingleValueMetricTests = None,
        duplicated_row_count_tests: SingleValueMetricTests = None,
        duplicated_column_count_tests: SingleValueMetricTests = None,
        almost_duplicated_column_count_tests: SingleValueMetricTests = None,
        almost_constant_column_count_tests: SingleValueMetricTests = None,
        empty_row_count_tests: SingleValueMetricTests = None,
        empty_column_count_tests: SingleValueMetricTests = None,
        constant_columns_count_tests: SingleValueMetricTests = None,
        dataset_missing_value_count_tests: SingleValueMetricTests = None,
        column_tests: Optional[Dict[str, ValueStatsTests]] = None,
    ):
        self.duplicated_row_count_tests = duplicated_row_count_tests
        self.duplicated_column_count_tests = duplicated_column_count_tests
        self.almost_constant_column_count_tests = almost_constant_column_count_tests
        self.almost_duplicated_column_count_tests = almost_duplicated_column_count_tests
        self.empty_row_count_tests = empty_row_count_tests
        self.empty_column_count_tests = empty_column_count_tests
        self.constant_columns_count_tests = constant_columns_count_tests
        self.dataset_missing_value_count_tests = dataset_missing_value_count_tests
        self.column_count_tests = column_count_tests
        self.row_count_tests = row_count_tests
        self._columns = columns
        self._column_tests = column_tests

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        columns_ = context.data_definition.get_categorical_columns() + context.data_definition.get_numerical_columns()
        self._dataset_stats = DatasetStats(
            row_count_tests=self.row_count_tests,
            column_count_tests=self.column_count_tests,
            duplicated_row_count_tests=self.duplicated_row_count_tests,
            duplicated_column_count_tests=self.duplicated_column_count_tests,
            almost_duplicated_column_count_tests=self.almost_duplicated_column_count_tests,
            almost_constant_column_count_tests=self.almost_constant_column_count_tests,
            empty_row_count_tests=self.empty_row_count_tests,
            empty_column_count_tests=self.empty_column_count_tests,
            constant_columns_count_tests=self.constant_columns_count_tests,
            dataset_missing_value_count_tests=self.dataset_missing_value_count_tests,
        )
        self._text_evals = TextEvals(self._columns or columns_, column_tests=self._column_tests)
        return self._dataset_stats.metrics(context) + self._text_evals.metrics(context)

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        if self._dataset_stats is None or self._text_evals is None:
            raise ValueError("Inconsistent internal state for DataSummaryPreset")
        return self._dataset_stats.render(context) + self._text_evals.render(context)
