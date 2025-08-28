import dataclasses
from itertools import chain
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently._pydantic_compat import PrivateAttr
from evidently._pydantic_compat import validator
from evidently.core.base_types import Label
from evidently.core.container import ColumnMetricContainer
from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import ByLabelMetricTests
from evidently.core.metric_types import GenericByLabelMetricTests
from evidently.core.metric_types import GenericSingleValueMetricTests
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import MetricResult
from evidently.core.metric_types import SingleValueMetricTests
from evidently.core.metric_types import convert_tests
from evidently.core.report import Context
from evidently.core.report import _default_input_data_generator
from evidently.legacy.core import ColumnType
from evidently.legacy.metrics import DatasetSummaryMetric
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import link_metric
from evidently.legacy.renderers.html_widgets import rich_data
from evidently.metrics import ColumnCount
from evidently.metrics import DuplicatedRowCount
from evidently.metrics import MaxValue
from evidently.metrics import MeanValue
from evidently.metrics import MinValue
from evidently.metrics import QuantileValue
from evidently.metrics import RowCount
from evidently.metrics import StdValue
from evidently.metrics import UniqueValueCount
from evidently.metrics.column_statistics import MissingValueCount
from evidently.metrics.dataset_statistics import AlmostConstantColumnsCount
from evidently.metrics.dataset_statistics import AlmostDuplicatedColumnsCount
from evidently.metrics.dataset_statistics import ConstantColumnsCount
from evidently.metrics.dataset_statistics import DatasetMissingValueCount
from evidently.metrics.dataset_statistics import DuplicatedColumnsCount
from evidently.metrics.dataset_statistics import EmptyColumnsCount
from evidently.metrics.dataset_statistics import EmptyRowsCount
from evidently.metrics.row_test_summary import RowTestSummary


class ValueStats(ColumnMetricContainer):
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
    replace_nan: Label = None

    @validator(
        "row_count_tests",
        "missing_values_count_tests",
        "min_tests",
        "max_tests",
        "mean_tests",
        "std_tests",
        "q25_tests",
        "q50_tests",
        "q75_tests",
        pre=True,
    )
    def validate_tests(cls, v):
        return convert_tests(v)

    def __init__(
        self,
        column: str,
        row_count_tests: SingleValueMetricTests = None,
        missing_values_count_tests: SingleValueMetricTests = None,
        min_tests: GenericSingleValueMetricTests = None,
        max_tests: GenericSingleValueMetricTests = None,
        mean_tests: GenericSingleValueMetricTests = None,
        std_tests: GenericSingleValueMetricTests = None,
        q25_tests: GenericSingleValueMetricTests = None,
        q50_tests: GenericSingleValueMetricTests = None,
        q75_tests: GenericSingleValueMetricTests = None,
        unique_values_count_tests: GenericByLabelMetricTests = None,
        include_tests: bool = True,
        replace_nan: Label = None,
    ):
        self.row_count_tests = convert_tests(row_count_tests)
        self.missing_values_count_tests = convert_tests(missing_values_count_tests)
        self.min_tests = convert_tests(min_tests)
        self.max_tests = convert_tests(max_tests)
        self.mean_tests = convert_tests(mean_tests)
        self.std_tests = convert_tests(std_tests)
        self.q25_tests = convert_tests(q25_tests)
        self.q50_tests = convert_tests(q50_tests)
        self.q75_tests = convert_tests(q75_tests)
        self.unique_values_count_tests = convert_tests(unique_values_count_tests)
        self.replace_nan = replace_nan
        super().__init__(column=column, include_tests=include_tests)

    def _categorical_unique_value_count_metric(self) -> UniqueValueCount:
        return UniqueValueCount(
            column=self.column,
            tests=self._get_tests(self.unique_values_count_tests),
            replace_nan=self.replace_nan,
        )

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        metrics: List[Metric] = [
            RowCount(tests=self._get_tests(self.row_count_tests)),
            MissingValueCount(column=self.column, tests=self._get_tests(self.missing_values_count_tests)),
        ]
        column_type = context.column(self.column).column_type
        if column_type == ColumnType.Numerical:
            metrics += [
                MinValue(column=self.column, tests=self._get_tests(self.min_tests)),
                MaxValue(column=self.column, tests=self._get_tests(self.max_tests)),
                MeanValue(column=self.column, tests=self._get_tests(self.mean_tests)),
                StdValue(column=self.column, tests=self._get_tests(self.std_tests)),
                QuantileValue(column=self.column, quantile=0.25, tests=self._get_tests(self.q25_tests)),
                QuantileValue(column=self.column, quantile=0.5, tests=self._get_tests(self.q50_tests)),
                QuantileValue(column=self.column, quantile=0.75, tests=self._get_tests(self.q75_tests)),
            ]
        if column_type == ColumnType.Categorical:
            metrics += [self._categorical_unique_value_count_metric()]
        if column_type == ColumnType.Datetime:
            metrics += [
                MinValue(column=self.column, tests=[]),
                MaxValue(column=self.column, tests=[]),
            ]
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        column_type = context.column(self.column).column_type
        widgets = []
        if column_type == ColumnType.Numerical:
            widgets = self._render_numerical(context)
        if column_type == ColumnType.Categorical:
            if len(context.column(self.column).labels()) <= 3:
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
            MinValue(column=self.column, tests=self.min_tests).get_metric_id(),
        ).get_widgets()[0]
        return [
            rich_data(
                title=self.column,
                description=context.column(self.column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self.column, tests=self.row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(
                                column=self.column,
                                tests=self.missing_values_count_tests,
                            ),
                        ),
                    },
                    {
                        "label": "min",
                        "values": self._get_metric(context, MinValue(column=self.column, tests=self.min_tests)),
                    },
                    {
                        "label": "max",
                        "values": self._get_metric(context, MaxValue(column=self.column, tests=self.max_tests)),
                    },
                    {
                        "label": "mean",
                        "values": self._get_metric(context, MeanValue(column=self.column, tests=self.mean_tests)),
                    },
                    {
                        "label": "std",
                        "values": self._get_metric(context, StdValue(column=self.column, tests=self.std_tests)),
                    },
                ],
                graph=result.params,
            )
        ]

    def _render_categorical(self, context: "Context") -> List[BaseWidgetInfo]:
        unique_value_metric = self._categorical_unique_value_count_metric()
        result = context.get_metric_result(unique_value_metric).get_widgets()[0]
        return [
            rich_data(
                title=self.column,
                description=context.column(self.column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self.column, tests=self.row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self.column, tests=self.missing_values_count_tests),
                        ),
                    },
                    {
                        "label": "most common",
                        "values": self._get_metric(
                            context,
                            unique_value_metric,
                            convert=self._most_common_value,
                        ),
                    },
                ],
                graph=result.params,
            )
        ]

    def _render_categorical_binary(self, context: "Context") -> List[BaseWidgetInfo]:
        unique_value_count = self._categorical_unique_value_count_metric()
        result: ByLabelCountValue = context.get_metric_result(unique_value_count)  # type: ignore[assignment]
        assert isinstance(result, ByLabelCountValue)

        ref_result: Optional[ByLabelCountValue] = None
        if context.has_reference:
            ref_result = context.get_reference_metric_result(unique_value_count.metric_id)  # type: ignore[assignment]
            assert isinstance(ref_result, ByLabelCountValue)

        metrics_widget = result.get_widgets()[0]
        return [
            rich_data(
                title=self.column,
                description=context.column(self.column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self.column, tests=self.row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self.column, tests=self.missing_values_count_tests),
                        ),
                    },
                ]
                + [
                    {
                        "label": f"{label}",
                        "values": self._label_count(result, ref_result, label),
                    }
                    for label in result.counts.keys()
                ],
                graph=metrics_widget.params,
            )
        ]

    def _render_text(self, context: "Context") -> List[BaseWidgetInfo]:
        raise NotImplementedError()

    def _render_datetime(self, context: "Context") -> List[BaseWidgetInfo]:
        result = context.get_metric_result(MinValue(column=self.column, tests=[]).get_metric_id()).get_widgets()[0]
        return [
            rich_data(
                title=self.column,
                description=context.column(self.column).column_type.value,
                header=["current", "reference"] if context.has_reference else ["current"],
                metrics=[
                    {
                        "label": "count",
                        "values": self._get_metric(context, RowCount(column=self.column, tests=self.row_count_tests)),
                    },
                    {
                        "label": "missing",
                        "values": self._get_metric(
                            context,
                            MissingValueCount(column=self.column, tests=self.missing_values_count_tests),
                        ),
                    },
                    {"label": "min", "values": self._get_metric(context, MinValue(column=self.column, tests=[]))},
                    {"label": "max", "values": self._get_metric(context, MaxValue(column=self.column, tests=[]))},
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
                convert(context.get_reference_metric_result(metric.metric_id)),
            ]
        return [convert(context.get_metric_result(metric))]

    def _most_common_value(self, unique_value: MetricResult):
        if not isinstance(unique_value, ByLabelCountValue):
            raise ValueError("Most common value must be of type 'ByLabelCountValue'")
        first = sorted(unique_value.counts.items(), key=lambda x: x[1].value, reverse=True)[0]
        return f"Label: {first[0]} count: {first[1]}"

    def _label_count(
        self,
        result: ByLabelCountValue,
        ref_result: Optional[ByLabelCountValue],
        label: Label,
    ):
        if ref_result is not None:
            return [
                f"{result.counts[label]} ({(result.shares[label].value * 100):0.0f}%)",
                f"{ref_result.counts[label]} ({(ref_result.shares[label].value * 100):0.0f}%)",
            ]
        return [
            f"{result.counts[label]} ({(result.shares[label].value * 100):0.0f}%)",
        ]


class DatasetStats(MetricContainer):
    row_count_tests: SingleValueMetricTests = None
    column_count_tests: SingleValueMetricTests = None
    duplicated_row_count_tests: SingleValueMetricTests = None
    duplicated_column_count_tests: SingleValueMetricTests = None
    almost_duplicated_column_count_tests: SingleValueMetricTests = None
    almost_constant_column_count_tests: SingleValueMetricTests = None
    empty_row_count_tests: SingleValueMetricTests = None
    empty_column_count_tests: SingleValueMetricTests = None
    constant_columns_count_tests: SingleValueMetricTests = None
    dataset_missing_value_count_tests: SingleValueMetricTests = None
    dataset_missing_value_share_tests: SingleValueMetricTests = None

    def __init__(
        self,
        row_count_tests: GenericSingleValueMetricTests = None,
        column_count_tests: GenericSingleValueMetricTests = None,
        duplicated_row_count_tests: GenericSingleValueMetricTests = None,
        duplicated_column_count_tests: GenericSingleValueMetricTests = None,
        almost_duplicated_column_count_tests: GenericSingleValueMetricTests = None,
        almost_constant_column_count_tests: GenericSingleValueMetricTests = None,
        empty_row_count_tests: GenericSingleValueMetricTests = None,
        empty_column_count_tests: GenericSingleValueMetricTests = None,
        constant_columns_count_tests: GenericSingleValueMetricTests = None,
        dataset_missing_value_count_tests: GenericSingleValueMetricTests = None,
        dataset_missing_value_share_tests: GenericSingleValueMetricTests = None,
        include_tests: bool = True,
    ):
        self.duplicated_row_count_tests = convert_tests(duplicated_row_count_tests)
        self.duplicated_column_count_tests = convert_tests(duplicated_column_count_tests)
        self.almost_constant_column_count_tests = convert_tests(almost_constant_column_count_tests)
        self.almost_duplicated_column_count_tests = convert_tests(almost_duplicated_column_count_tests)
        self.empty_row_count_tests = convert_tests(empty_row_count_tests)
        self.empty_column_count_tests = convert_tests(empty_column_count_tests)
        self.constant_columns_count_tests = convert_tests(constant_columns_count_tests)
        self.dataset_missing_value_count_tests = convert_tests(dataset_missing_value_count_tests)
        self.dataset_missing_value_share_tests = convert_tests(dataset_missing_value_share_tests)
        self.column_count_tests = convert_tests(column_count_tests)
        self.row_count_tests = convert_tests(row_count_tests)
        super().__init__(include_tests=include_tests)

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        return [
            RowCount(tests=self._get_tests(self.row_count_tests)),
            ColumnCount(tests=self._get_tests(self.column_count_tests)),
            ColumnCount(column_type=ColumnType.Numerical, tests=[]),
            ColumnCount(column_type=ColumnType.Categorical, tests=[]),
            ColumnCount(column_type=ColumnType.Datetime, tests=[]),
            ColumnCount(column_type=ColumnType.Text, tests=[]),
            DuplicatedRowCount(tests=self._get_tests(self.duplicated_row_count_tests)),
            DuplicatedColumnsCount(tests=self._get_tests(self.duplicated_column_count_tests)),
            AlmostDuplicatedColumnsCount(tests=self._get_tests(self.almost_duplicated_column_count_tests)),
            AlmostConstantColumnsCount(tests=self._get_tests(self.almost_constant_column_count_tests)),
            EmptyRowsCount(tests=self._get_tests(self.empty_row_count_tests)),
            EmptyColumnsCount(tests=self._get_tests(self.empty_column_count_tests)),
            ConstantColumnsCount(tests=self._get_tests(self.constant_columns_count_tests)),
            DatasetMissingValueCount(
                tests=self._get_tests(self.dataset_missing_value_count_tests),
                share_tests=self._get_tests(self.dataset_missing_value_share_tests),
            ),
        ]

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        legacy_metric = DatasetSummaryMetric()
        _, render = context.get_legacy_metric(legacy_metric, _default_input_data_generator, None)
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

    def convert(self) -> "ValueStatsTests":
        return ValueStatsTests(**{k: convert_tests(v) for k, v in dataclasses.asdict(self).items()})


class TextEvals(MetricContainer):
    columns: Optional[List[str]] = None
    row_count_tests: SingleValueMetricTests = None
    column_tests: Optional[Dict[str, ValueStatsTests]] = None

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        row_count_tests: GenericSingleValueMetricTests = None,
        column_tests: Optional[Dict[str, ValueStatsTests]] = None,
        include_tests: bool = True,
    ):
        self.columns = columns
        self.row_count_tests = convert_tests(row_count_tests)
        self.column_tests = {k: v.convert() for k, v in column_tests.items()} if column_tests is not None else None
        super().__init__(include_tests=include_tests)

    def get_cols(self, context: Context):
        if self.columns is None:
            return context.data_definition.numerical_descriptors + context.data_definition.categorical_descriptors
        else:
            return self.columns

    def get_value_stats(self, context: Context) -> List[ValueStats]:
        cols = self.get_cols(context)
        return [
            ValueStats(
                column,
                **{
                    k: v
                    for k, v in (self.column_tests or {}).get(column, ValueStatsTests()).__dict__.items()
                    if not k.startswith("__")
                },
                include_tests=self.include_tests,
            )
            for column in cols
            if column not in (context.data_definition.test_descriptors or [])
        ]

    def generate_metrics(self, context: Context) -> Sequence[MetricOrContainer]:
        metrics: List[MetricOrContainer] = [RowTestSummary(), RowCount(tests=self._get_tests(self.row_count_tests))]
        value_stats = self.get_value_stats(context)
        metrics.extend(list(chain(*[vs.metrics(context)[1:] for vs in value_stats])))
        for column_info in context.data_definition.special_columns:
            metrics.extend(column_info.get_metrics())
        return metrics

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        value_stats = self.get_value_stats(context)
        result = list(chain(*([RowTestSummary().render(context)] + [vs.render(context) for vs in value_stats])))
        for column_info in context.data_definition.special_columns:
            for metric in column_info.get_metrics():
                if isinstance(metric, MetricContainer):
                    result.extend(metric.render(context))
                else:
                    result.extend(context.get_metric_result(metric).widget or [])
        return result


class DataSummaryPreset(MetricContainer):
    columns: Optional[List[str]] = None
    row_count_tests: SingleValueMetricTests = None
    column_count_tests: SingleValueMetricTests = None
    duplicated_row_count_tests: SingleValueMetricTests = None
    duplicated_column_count_tests: SingleValueMetricTests = None
    almost_duplicated_column_count_tests: SingleValueMetricTests = None
    almost_constant_column_count_tests: SingleValueMetricTests = None
    empty_row_count_tests: SingleValueMetricTests = None
    empty_column_count_tests: SingleValueMetricTests = None
    constant_columns_count_tests: SingleValueMetricTests = None
    dataset_missing_value_count_tests: SingleValueMetricTests = None
    column_tests: Optional[Dict[str, ValueStatsTests]] = None

    _dataset_stats: Optional[DatasetStats] = PrivateAttr(None)
    _text_evals: Optional[TextEvals] = PrivateAttr(None)

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        row_count_tests: GenericSingleValueMetricTests = None,
        column_count_tests: GenericSingleValueMetricTests = None,
        duplicated_row_count_tests: GenericSingleValueMetricTests = None,
        duplicated_column_count_tests: GenericSingleValueMetricTests = None,
        almost_duplicated_column_count_tests: GenericSingleValueMetricTests = None,
        almost_constant_column_count_tests: GenericSingleValueMetricTests = None,
        empty_row_count_tests: GenericSingleValueMetricTests = None,
        empty_column_count_tests: GenericSingleValueMetricTests = None,
        constant_columns_count_tests: GenericSingleValueMetricTests = None,
        dataset_missing_value_count_tests: GenericSingleValueMetricTests = None,
        column_tests: Optional[Dict[str, ValueStatsTests]] = None,
        include_tests: bool = True,
    ):
        self.duplicated_row_count_tests = convert_tests(duplicated_row_count_tests)
        self.duplicated_column_count_tests = convert_tests(duplicated_column_count_tests)
        self.almost_constant_column_count_tests = convert_tests(almost_constant_column_count_tests)
        self.almost_duplicated_column_count_tests = convert_tests(almost_duplicated_column_count_tests)
        self.empty_row_count_tests = convert_tests(empty_row_count_tests)
        self.empty_column_count_tests = convert_tests(empty_column_count_tests)
        self.constant_columns_count_tests = convert_tests(constant_columns_count_tests)
        self.dataset_missing_value_count_tests = convert_tests(dataset_missing_value_count_tests)
        self.column_count_tests = convert_tests(column_count_tests)
        self.row_count_tests = convert_tests(row_count_tests)
        self.columns = columns
        self.column_tests = {k: v.convert() for k, v in column_tests.items()} if column_tests is not None else None
        super().__init__(include_tests=include_tests)

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
            include_tests=self.include_tests,
        )
        self._text_evals = TextEvals(
            self.columns or columns_, column_tests=self.column_tests, include_tests=self.include_tests
        )
        return self._dataset_stats.metrics(context) + self._text_evals.metrics(context)

    def render(
        self,
        context: "Context",
        child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None,
    ) -> List[BaseWidgetInfo]:
        if self._dataset_stats is None or self._text_evals is None:
            raise ValueError("Inconsistent internal state for DataSummaryPreset")
        return self._dataset_stats.render(context) + self._text_evals.render(context)
