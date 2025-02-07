from itertools import chain
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from evidently.core import ColumnType
from evidently.future.container import MetricContainer
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
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


class ValueStats(MetricContainer):
    def __init__(self, column: str):
        self._column = column

    def generate_metrics(self, context: Context) -> List[Metric]:
        metrics: List[Metric] = [
            RowCount(),
            MissingValueCount(column=self._column),
        ]
        column_type = context.column(self._column).column_type
        if column_type == ColumnType.Numerical:
            metrics += [
                MinValue(column=self._column),
                MaxValue(column=self._column),
                MeanValue(column=self._column),
                StdValue(column=self._column),
                QuantileValue(column=self._column, quantile=0.25),
                QuantileValue(column=self._column, quantile=0.5),
                QuantileValue(column=self._column, quantile=0.75),
            ]
        if column_type == ColumnType.Categorical:
            metrics += [
                UniqueValueCount(column=self._column),
            ]
        if column_type == ColumnType.Datetime:
            metrics += [
                MinValue(column=self._column, tests=[]),
                MaxValue(column=self._column, tests=[]),
            ]
        return metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
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
        for metric in self.metrics(context):
            link_metric(widgets, metric)
        return widgets

    def _render_numerical(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(MinValue(column=self._column).get_metric_id()).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {"label": "count", "values": self._get_metric(context, RowCount(column=self._column))},
                    {"label": "missing", "values": self._get_metric(context, MissingValueCount(column=self._column))},
                    {"label": "min", "values": self._get_metric(context, MinValue(column=self._column))},
                    {"label": "max", "values": self._get_metric(context, MaxValue(column=self._column))},
                    {"label": "mean", "values": self._get_metric(context, MeanValue(column=self._column))},
                    {"label": "std", "values": self._get_metric(context, StdValue(column=self._column))},
                ],
                graph=result.params,
            )
        ]

    def _render_categorical(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(UniqueValueCount(column=self._column)).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {"label": "count", "values": self._get_metric(context, RowCount(column=self._column))},
                    {"label": "missing", "values": self._get_metric(context, MissingValueCount(column=self._column))},
                    {
                        "label": "most common",
                        "values": self._get_metric(
                            context,
                            UniqueValueCount(column=self._column),
                            convert=self._most_common_value,
                        ),
                    },
                ],
                graph=result.params,
            )
        ]

    def _render_categorical_binary(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(UniqueValueCount(column=self._column)).widget[0]
        return [
            rich_data(
                title=self._column,
                description=context.column(self._column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {"label": "count", "values": self._get_metric(context, RowCount(column=self._column))},
                    {"label": "missing", "values": self._get_metric(context, MissingValueCount(column=self._column))},
                ]
                + [
                    {
                        "label": f"{label}",
                        "values": self._label_count(context, UniqueValueCount(column=self._column), label),
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
                    {"label": "count", "values": self._get_metric(context, RowCount(column=self._column))},
                    {"label": "missing", "values": self._get_metric(context, MissingValueCount(column=self._column))},
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
        if not isinstance(unique_value, ByLabelValue):
            raise ValueError("Most common value must be of type 'ByLabelValue'")
        first = sorted(unique_value.values.items(), key=lambda x: x[1], reverse=True)[0]
        return f"Label: {first[0]} count: {first[1]}"

    def _label_count(
        self,
        context: "Context",
        metric: UniqueValueCount,
        label: Label,
    ):
        result = context.get_metric_result(metric)
        assert isinstance(result, ByLabelValue)
        if context.has_reference:
            ref_result = context.get_reference_metric_result(metric)
            assert isinstance(ref_result, ByLabelValue)
            return [
                str(result.values[label]),
                str(ref_result.values[label]),
            ]
        return [
            str(result.values[label]),
        ]


class DatasetStats(MetricContainer):
    def generate_metrics(self, context: Context) -> List[Metric]:
        return [
            RowCount(),
            ColumnCount(),
            ColumnCount(column_type=ColumnType.Numerical, tests=[]),
            ColumnCount(column_type=ColumnType.Categorical, tests=[]),
            ColumnCount(column_type=ColumnType.Datetime, tests=[]),
            ColumnCount(column_type=ColumnType.Text, tests=[]),
            DuplicatedRowCount(),
            DuplicatedColumnsCount(),
            AlmostDuplicatedColumnsCount(),
            AlmostConstantColumnsCount(),
            EmptyRowsCount(),
            EmptyColumnsCount(),
            ConstantColumnsCount(),
            DatasetMissingValueCount(),
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        metric = DatasetSummaryMetric()
        _, render = context.get_legacy_metric(metric, _default_input_data_generator)
        for metric in self.metrics(context):
            link_metric(render, metric)
        return render


class TextEvals(MetricContainer):
    def __init__(self, columns: Optional[List[str]] = None):
        self._columns = columns
        self._value_stats: List[ValueStats] = []

    def generate_metrics(self, context: Context) -> List[Metric]:
        if self._columns is None:
            cols = context.data_definition.numerical_descriptors + context.data_definition.categorical_descriptors
        else:
            cols = self._columns
        metrics: List[Metric] = [RowCount()]
        self._value_stats = [ValueStats(column) for column in cols]
        metrics.extend(list(chain(*[vs.metrics(context)[1:] for vs in self._value_stats])))
        return metrics

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        return list(chain(*[vs.render(context, results) for vs in self._value_stats]))


class DataSummaryPreset(MetricContainer):
    def __init__(self, columns: Optional[List[str]] = None):
        self._columns = columns

    def generate_metrics(self, context: Context) -> List[Metric]:
        columns_ = context.data_definition.get_categorical_columns() + context.data_definition.get_numerical_columns()
        self._dataset_stats = DatasetStats()
        self._text_evals = TextEvals(self._columns or columns_)
        return self._dataset_stats.metrics(context) + self._text_evals.metrics(context)

    def render(self, context: "Context", results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        return self._dataset_stats.render(context, results) + self._text_evals.render(context, results)
