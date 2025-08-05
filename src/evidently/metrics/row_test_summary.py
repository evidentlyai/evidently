from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import SingleValue
from evidently.core.report import Context
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import pie_chart
from evidently.metrics import MeanValue
from evidently.metrics import RowCount
from evidently.tests import gte


class RowTestSummary(MetricContainer):
    columns: List[str] = []
    min_success_rate: float = 1

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        test_columns = self.get_test_columns(context)
        return [self.get_test_column_metric(tc, context) for tc in test_columns] + [self.get_row_count_metric()]

    def get_row_count_metric(self):
        return RowCount()

    def get_test_columns(self, context):
        return self.columns or context.data_definition.test_descriptors or []

    def get_test_column_metric(self, test_column: str, context) -> Metric:
        tests = None
        if context.configuration.include_tests:
            tests = [gte(self.min_success_rate, alias=f"Share of passed '{test_column}' row tests")]
        return MeanValue(column=test_column, tests=tests)

    def _render_test_column_widget(
        self, context: "Context", test_column: str, row_count: int, size: WidgetSize
    ) -> BaseWidgetInfo:
        title = f"Row test '{test_column}'"
        metric = self.get_test_column_metric(test_column, context)
        result = context.get_metric_result(metric)
        assert isinstance(result, SingleValue)
        success_count = int(result.value * row_count)
        if result.value == 1:
            return pie_chart(title=title, data=(["PASSED"], [row_count]), colors=["GREEN"], size=size)
        if result.value == 0:
            return pie_chart(title=title, data=(["FAILED"], [row_count]), colors=["RED"], size=size)
        return pie_chart(
            title=title,
            data=(["PASSED", "FAILED"], [success_count, row_count - success_count]),
            colors=["GREEN", "RED"],
            size=size,
        )

    def render(
        self, context: "Context", child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None
    ) -> List[BaseWidgetInfo]:
        test_columns = self.get_test_columns(context)
        is_last_full_size = len(test_columns) % 2 == 1
        row_count_result = context.get_metric_result(self.get_row_count_metric())
        assert isinstance(row_count_result, SingleValue)
        return [
            self._render_test_column_widget(
                context,
                tc,
                int(row_count_result.value),
                size=WidgetSize.FULL if is_last_full_size and i == len(test_columns) - 1 else WidgetSize.HALF,
            )
            for i, tc in enumerate(test_columns)
        ]
