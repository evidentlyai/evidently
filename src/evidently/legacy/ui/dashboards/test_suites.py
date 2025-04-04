import datetime
import re
import typing
import warnings
from collections import Counter
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from plotly import graph_objs as go

from evidently._pydantic_compat import BaseModel
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import plotly_figure
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests.base_test import Test
from evidently.legacy.tests.base_test import TestStatus
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import TestInfo
from evidently.legacy.ui.type_aliases import TestResultPoints
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import autoregister

from .base import DashboardPanel
from .base import ReportFilter
from .base import assign_panel_id
from .utils import TEST_COLORS
from .utils import CounterAgg
from .utils import TestSuitePanelType
from .utils import _get_hover_params
from .utils import _get_test_hover
from .utils import getattr_nested

if typing.TYPE_CHECKING:
    from evidently.legacy.ui.base import DataStorage


class TestFilter(BaseModel):
    test_id: Optional[str] = None
    test_fingerprint: Optional[str] = None
    test_args: Dict[str, Union[EvidentlyBaseModel, Any]] = {}

    def __init__(
        self,
        *,
        test_id: Optional[str] = None,
        test_fingerprint: Optional[str] = None,
        test_args: Dict[str, Union[EvidentlyBaseModel, Any]] = None,
        test_hash: Optional[str] = None,
    ):
        if test_hash is not None:
            warnings.warn("test_hash is deprecated, please use test_fingerprint")
            test_fingerprint = test_hash
        super().__init__(test_id=test_id, test_fingerprint=test_fingerprint, test_args=test_args or {})

    def test_matched(self, test: Test) -> bool:
        if self.test_fingerprint is not None:
            return test.get_fingerprint() == self.test_fingerprint
        if self.test_id is not None and self.test_id != test.get_id():
            return False
        for field, value in self.test_args.items():
            try:
                if getattr_nested(test, field.split(".")) != value:
                    return False
            except AttributeError:
                return False
        return True

    def get(self, test_suite: TestSuite) -> Dict[Test, TestInfo]:
        results = {}
        for test in test_suite._inner_suite.context.tests:
            if self.test_matched(test):
                try:
                    result = test.get_result()
                    results[test] = TestInfo(test_suite.id, result.status, result.description)
                except AttributeError:
                    pass
        return results


descr_re = re.compile(r"\.\s+([A-Z])")


@autoregister
class DashboardPanelTestSuite(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelTestSuite"

    test_filters: List[TestFilter] = []
    filter: ReportFilter = ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True)
    panel_type: TestSuitePanelType = TestSuitePanelType.AGGREGATE
    time_agg: Optional[str] = None

    @assign_panel_id
    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> BaseWidgetInfo:
        self.filter.include_test_suites = True
        points: TestResultPoints = await data_storage.load_test_results(
            project_id, self.filter, self.test_filters, self.time_agg, timestamp_start, timestamp_end
        )

        if self.panel_type == TestSuitePanelType.AGGREGATE:
            fig = self._create_aggregate_fig(points)
        elif self.panel_type == TestSuitePanelType.DETAILED:
            fig = self._create_detailed_fig(points)
        else:
            raise ValueError(f"Unknown panel type {self.panel_type}")

        return plotly_figure(title=self.title, figure=fig, size=self.size)

    def _create_aggregate_fig(self, points: TestResultPoints):
        dates = list(sorted(points.keys()))
        bars = [Counter(ti.status for ti in points[d].values()) for d in dates]
        fig = go.Figure(
            data=[
                go.Bar(name=status.value, x=dates, y=[c[status] for c in bars], marker_color=color)
                for status, color in TEST_COLORS.items()
            ],
            layout={"showlegend": True},
        )
        fig.update_layout(barmode="stack")
        fig.update_xaxes(type="category")
        return fig

    def _create_detailed_fig(self, points: TestResultPoints):
        dates = list(sorted(points.keys()))
        all_tests = set(t for p in points.values() for t in p.keys())
        tests = list(all_tests)
        hover_params = _get_hover_params(all_tests)

        def get_description(test: Test, date):
            test_info = points[date][test]
            description = test_info.description
            description, _ = descr_re.subn(r".<br>\g<1>", description)
            return {
                "description": description,
                "test_fingerprint": test.get_fingerprint(),
                "snapshot_id": str(test_info.snapshot_id),
            }

        def get_color(test, date) -> Optional[str]:
            ti = points[date].get(test)
            if ti is None:
                return TEST_COLORS[TestStatus.SKIPPED]
            return TEST_COLORS.get(ti.status)

        fig = go.Figure(
            data=[
                go.Bar(
                    name="",
                    x=dates,
                    y=[1 for _ in range(len(dates))],
                    marker_color=[get_color(test, d) for d in dates],
                    hovertemplate=_get_test_hover(test, hover_params[test]),
                    customdata=[get_description(test, d) for i, d in enumerate(dates)],
                    showlegend=False,
                )
                for test in tests
            ]
            + [
                go.Scatter(
                    x=[None],
                    y=[None],
                    mode="markers",
                    name=status.value,
                    marker=dict(size=7, color=col, symbol="square"),
                )
                for status, col in TEST_COLORS.items()
            ],
            layout={"showlegend": True},
        )
        fig.update_layout(
            barmode="stack",
            bargap=0.01,
            barnorm="fraction",
        )
        fig.update_yaxes(showticklabels=False)
        fig.update_xaxes(type="category")
        return fig


def to_period(time_agg: Optional[str], timestamp: datetime.datetime) -> datetime.datetime:
    if time_agg is None:
        return timestamp
    return pd.Series([timestamp], name="dt").dt.to_period(time_agg)[0].to_timestamp()


@autoregister
class DashboardPanelTestSuiteCounter(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelTestSuiteCounter"

    agg: CounterAgg = CounterAgg.NONE
    filter: ReportFilter = ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True)
    test_filters: List[TestFilter] = []
    statuses: List[TestStatus] = [TestStatus.SUCCESS]

    @assign_panel_id
    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> BaseWidgetInfo:
        if self.agg == CounterAgg.NONE:
            statuses, postfix = await self._build_none(data_storage, project_id, timestamp_start, timestamp_end)
        elif self.agg == CounterAgg.LAST:
            statuses, postfix = await self._build_last(data_storage, project_id, timestamp_start, timestamp_end)
        else:
            raise ValueError(f"TestSuite Counter does not support agg {self.agg}")

        total = sum(statuses.values())
        value = sum(statuses[s] for s in self.statuses)
        statuses_join = ", ".join(s.value for s in self.statuses)
        return counter(counters=[CounterData(f"{value}/{total} {statuses_join}{postfix}", self.title)], size=self.size)

    async def _build_none(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> Tuple[Counter, str]:
        points = await data_storage.load_test_results(
            project_id, self.filter, self.test_filters, None, timestamp_start, timestamp_end
        )
        statuses: typing.Counter[TestStatus] = Counter()
        for values in points.values():
            statuses.update(v.status for v in values.values())
        return statuses, ""

    async def _build_last(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> Tuple[Counter, str]:
        points = await data_storage.load_test_results(
            project_id, self.filter, self.test_filters, None, timestamp_start, timestamp_end
        )

        if len(points) == 0:
            return Counter(), "(no data)"
        last_ts = max(points.keys())
        statuses: typing.Counter[TestStatus] = Counter(v.status for v in points[last_ts].values())
        return statuses, f" ({last_ts})"
