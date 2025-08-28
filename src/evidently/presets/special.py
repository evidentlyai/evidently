from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

import pandas as pd

from evidently.core.container import MetricContainer
from evidently.core.container import MetricOrContainer
from evidently.core.datasets import TestSummaryInfo
from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import Metric
from evidently.core.metric_types import MetricId
from evidently.core.metric_types import SingleValue
from evidently.core.report import Context
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.model.widget import WidgetType
from evidently.legacy.options import ColorOptions
from evidently.legacy.renderers.html_widgets import WidgetSize
from evidently.legacy.renderers.html_widgets import group_widget
from evidently.legacy.renderers.html_widgets import histogram
from evidently.legacy.renderers.html_widgets import pie_chart
from evidently.legacy.tests.base_test import TestStatus
from evidently.metrics import MeanValue
from evidently.metrics import UniqueValueCount


class TestSummaryInfoPreset(MetricContainer):
    column_info: TestSummaryInfo

    def generate_metrics(self, context: "Context") -> Sequence[MetricOrContainer]:
        result = []
        if self.column_info.has_all:
            result.append(self._all_metric)
        if self.column_info.has_any:
            result.append(self._any_metric)
        if self.column_info.has_count:
            result.append(self._count_metric)
        if self.column_info.has_rate:
            result.append(self._rate_metric)
        if self.column_info.has_score:
            result.append(self._score_metric)
        return result

    @property
    def _all_metric(self) -> Metric:
        return UniqueValueCount(column=self.column_info.all_column)

    @property
    def _any_metric(self) -> Metric:
        return UniqueValueCount(column=self.column_info.any_column)

    @property
    def _count_metric(self) -> Metric:
        return UniqueValueCount(column=self.column_info.count_column)

    @property
    def _rate_metric(self) -> Metric:
        return MeanValue(column=self.column_info.rate_column)

    @property
    def _score_metric(self) -> Metric:
        return MeanValue(column=self.column_info.score_column)

    def render(
        self, context: "Context", child_widgets: Optional[List[Tuple[Optional[MetricId], List[BaseWidgetInfo]]]] = None
    ) -> List[BaseWidgetInfo]:
        widgets = []
        if self.column_info.has_all:
            all_results = context.get_metric_result(self._all_metric)
            assert isinstance(all_results, ByLabelCountValue)
            widgets.append(
                pie_chart(
                    title="All tests passed",
                    size=WidgetSize.HALF,
                    data={
                        TestStatus.SUCCESS.value: all_results.counts[True].value if True in all_results.counts else 0,
                        TestStatus.FAIL.value: all_results.counts[False].value if False in all_results.counts else 0,
                    },
                )
            )
        if self.column_info.has_any:
            any_results = context.get_metric_result(self._any_metric)
            assert isinstance(any_results, ByLabelCountValue)
            widgets.append(
                pie_chart(
                    title="Any tests passed",
                    size=WidgetSize.HALF,
                    data={
                        TestStatus.SUCCESS.value: any_results.counts[True].value if True in any_results.counts else 0,
                        TestStatus.FAIL.value: any_results.counts[False].value if False in any_results.counts else 0,
                    },
                )
            )

        if self.column_info.has_count:
            count_results = context.get_metric_result(self._count_metric)
            assert isinstance(count_results, ByLabelCountValue)
            widgets.append(
                histogram(
                    title="Count of tests passed",
                    color_options=ColorOptions(),
                    size=WidgetSize.HALF,
                    primary_hist=HistogramData(
                        x=pd.Series(count_results.counts.keys()),
                        count=pd.Series([v.value for v in count_results.counts.values()]),
                    ),
                )
            )
        if self.column_info.has_rate:
            rate_results = context.get_metric_result(self._rate_metric)
            assert isinstance(rate_results, SingleValue)
            assert rate_results.widget is not None
            distr_widget = rate_results.widget[0]
            widgets.append(
                BaseWidgetInfo(
                    title="Rate of tests passed",
                    type=WidgetType.BIG_GRAPH.value,
                    size=WidgetSize.HALF,
                    params=distr_widget.params,
                )
            )
        if self.column_info.has_score:
            score_results = context.get_metric_result(self._score_metric)
            assert isinstance(score_results, SingleValue)
            assert score_results.widget is not None
            distr_widget = score_results.widget[0]
            widgets.append(
                BaseWidgetInfo(
                    title="Row scores",
                    type=WidgetType.BIG_GRAPH.value,
                    size=WidgetSize.HALF,
                    params=distr_widget.params,
                )
            )
        return [group_widget(title="Row test summary", widgets=widgets)]
