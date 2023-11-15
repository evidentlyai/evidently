import abc
import datetime
import traceback
import typing
import uuid
from collections import Counter
from collections import defaultdict
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
import plotly.io as pio
from plotly import graph_objs as go

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import validator
from evidently.base_metric import ColumnName
from evidently.base_metric import Metric
from evidently.core import IncludeOptions
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import EnumValueMixin
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import FieldPath
from evidently.pydantic_utils import PolymorphicModel
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.report import Report
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import ReportBase
from evidently.suite.base_suite import T
from evidently.test_suite import TestSuite
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestStatus

COLOR_DISCRETE_SEQUENCE = (
    "#ed0400",
    "#0a5f38",
    "#6c3461",
    "#71aa34",
    "#6b8ba4",
    "#60460f",
    "#a00498",
    "#017b92",
    "#ffad01",
    "#464196",
)

pio.templates[pio.templates.default].layout.colorway = COLOR_DISCRETE_SEQUENCE


class ReportFilter(BaseModel):
    metadata_values: Dict[str, str]
    tag_values: List[str]
    include_test_suites: bool = False

    def filter(self, report: ReportBase):
        if not self.include_test_suites and isinstance(report, TestSuite):
            return False
        return all(report.metadata.get(key) == value for key, value in self.metadata_values.items()) and all(
            tag in report.tags for tag in self.tag_values
        )


def get_nested(d: dict, path: List[str]):
    if len(path) == 1:
        return d[path[0]]
    return get_nested(d[path[0]], path[1:])


_not_set = object()


def _getattr_or_getitem(obj: Any, item: str, default=_not_set):
    if isinstance(obj, dict):
        if default is _not_set:
            return obj[item]
        return obj.get(item, default)
    if default is _not_set:
        return getattr(obj, item)
    return getattr(obj, item, default)


def getattr_nested(obj: Any, path: List[str], default=_not_set):
    item = path[0]
    if len(path) == 1:
        return _getattr_or_getitem(obj, item, default)
    return getattr_nested(_getattr_or_getitem(obj, item, default), path[1:], default)


class PanelValue(BaseModel):
    field_path: Union[str, FieldPath]
    metric_id: Optional[str] = None
    metric_hash: Optional[int] = None
    metric_args: Dict[str, Union[EvidentlyBaseModel, Any]] = {}
    legend: Optional[str] = None

    @property
    def field_path_str(self):
        if isinstance(self.field_path, FieldPath):
            return self.field_path.get_path()
        return self.field_path

    @validator("field_path")
    def validate_field_path(cls, value):
        if isinstance(value, FieldPath):
            value = value.get_path()
        return value

    def metric_matched(self, metric: Metric) -> bool:
        if self.metric_hash is not None and hash(metric) == self.metric_hash:
            return True
        if self.metric_id is not None and self.metric_id != metric.get_id():
            return False
        for field, value in self.metric_args.items():
            try:
                if getattr_nested(metric, field.split(".")) != value:
                    return False
            except AttributeError:
                return False
        return True

    def get(self, report: ReportBase) -> Dict[Metric, Any]:
        results = {}
        metrics = []
        if isinstance(report, Report):
            metrics = report._first_level_metrics
        elif isinstance(report, TestSuite):
            metrics = report._inner_suite.context.metrics
        for metric in metrics:
            if self.metric_matched(metric):
                try:
                    results[metric] = getattr_nested(metric.get_result(), self.field_path_str.split("."))
                except AttributeError:
                    pass
        return results


class PlotType(Enum):
    # todo: move it to core lib?
    SCATTER = "scatter"
    BAR = "bar"
    LINE = "line"
    HISTOGRAM = "histogram"


class DashboardPanel(EnumValueMixin, PolymorphicModel):
    id: uuid.UUID = uuid.uuid4()
    title: str
    filter: ReportFilter
    size: WidgetSize = WidgetSize.FULL

    @abc.abstractmethod
    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        raise NotImplementedError


def _flatten_params_rec(obj: Any, paths: List[str]) -> List[Tuple[List[str], str]]:
    res = []
    if isinstance(obj, ColumnName) and obj == ColumnName.from_any(obj.name):
        return [(paths, obj.name)]
    if isinstance(obj, BaseModel):
        for field_name, field in obj.__fields__.items():
            if isinstance(obj, EvidentlyBaseModel) and field_name == "type":
                continue
            field_value = getattr(obj, field_name)
            if field_value == field.default:
                continue
            if isinstance(field.type_, type) and issubclass(field.type_, BaseModel):
                res.extend(_flatten_params_rec(field_value, paths + [field_name]))
            else:
                res.append((paths + [field_name], str(field_value)))
    return res


def _flatten_params(obj: EvidentlyBaseModel) -> Dict[str, str]:
    return {".".join(path): val for path, val in _flatten_params_rec(obj, [])}


def _get_metric_hover(metric: Metric, value: PanelValue):
    params = []
    for name, v in metric.dict().items():
        if name in ["type"]:
            continue
        if v is None:
            continue
        params.append(f"{name}: {v}")
    params_join = "<br>".join(params)
    hover = f"<b>Timestamp: %{{x}}</b><br><b>Value: %{{y}}</b><br>{params_join}<br>.{value.field_path}"
    return hover


class DashboardPanelPlot(DashboardPanel):
    values: List[PanelValue]
    plot_type: PlotType

    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:

        points: List[Dict[Metric, List[Tuple[datetime.datetime, Any]]]] = [{} for _ in range(len(self.values))]
        for report in reports:
            if not self.filter.filter(report):
                continue
            for i, value in enumerate(self.values):
                for metric, metric_field_value in value.get(report).items():
                    if metric not in points[i]:
                        points[i][metric] = []
                    points[i][metric].append((report.timestamp, metric_field_value))

        fig = go.Figure(layout={"showlegend": True})
        for val, metric_pts in zip(self.values, points):
            if len(metric_pts) == 0:
                # no matching metrics, show error?
                continue

            for metric, pts in metric_pts.items():
                pts.sort(key=lambda x: x[0])

                hover = _get_metric_hover(metric, val)
                if self.plot_type == PlotType.HISTOGRAM:
                    plot = go.Histogram(
                        x=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                    )
                else:
                    cls, args = self.plot_type_cls
                    plot = cls(
                        x=[p[0] for p in pts],
                        y=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                        **args,
                    )
                fig.add_trace(plot)
        return plotly_figure(title=self.title, figure=fig, size=self.size)

    @property
    def plot_type_cls(self):
        if self.plot_type == PlotType.SCATTER:
            return go.Scatter, {"mode": "markers"}
        if self.plot_type == PlotType.BAR:
            return go.Bar, {}
        if self.plot_type == PlotType.LINE:
            return go.Line, {}
        raise ValueError(f"Unsupported plot type {self.plot_type}")


class CounterAgg(Enum):
    SUM = "sum"
    LAST = "last"
    NONE = "none"


class DashboardPanelCounter(DashboardPanel):
    agg: CounterAgg
    value: Optional[PanelValue] = None
    text: Optional[str] = None

    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        if self.agg == CounterAgg.NONE:
            return counter(counters=[CounterData(self.title, self.text or "")], size=self.size)
        value = self._get_counter_value(reports)
        if isinstance(value, float):
            ct = CounterData.float(self.text or "", value, 3)
        else:
            ct = CounterData.int(self.text or "", value)
        return counter(title=self.title, counters=[ct], size=self.size)

    def _get_counter_value(self, reports: Iterable[ReportBase]):
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        if self.agg == CounterAgg.LAST:
            return max(
                ((r.timestamp, v) for r in reports if self.filter.filter(r) for v in self.value.get(r).values()),
                key=lambda x: x[0],
            )[1]
        if self.agg == CounterAgg.SUM:
            return sum(v or 0 for r in reports if self.filter.filter(r) for v in self.value.get(r).values())
        raise ValueError(f"Unknown agg type {self.agg}")


class TestFilter(BaseModel):
    test_id: Optional[str] = None
    test_hash: Optional[int] = None
    test_args: Dict[str, Union[EvidentlyBaseModel, Any]] = {}

    def test_matched(self, test: Test) -> bool:
        if self.test_hash is not None and hash(test) == self.test_hash:
            return True
        if self.test_id is not None and self.test_id != test.get_id():
            return False
        for field, value in self.test_args.items():
            try:
                if getattr_nested(test, field.split(".")) != value:
                    return False
            except AttributeError:
                return False
        return True

    def get(self, test_suite: TestSuite) -> Dict[Test, TestStatus]:
        results = {}
        for test in test_suite._inner_suite.context.tests:
            if self.test_matched(test):
                try:
                    results[test] = test.get_result().status
                except AttributeError:
                    pass
        return results


tests_colors = {
    TestStatus.ERROR: "#6B8BA4",
    TestStatus.FAIL: "#ed0400",
    TestStatus.WARNING: "#ffad01",
    TestStatus.SUCCESS: "#0a5f38",
    TestStatus.SKIPPED: "#a00498",
}

tests_colors_order = {ts: i for i, ts in enumerate(tests_colors)}


def _get_test_hover(test: Test):
    params = [f"{k}: {v}" for k, v in _flatten_params(test).items()]
    params_join = "<br>".join(params)
    hover = f"<b>Timestamp: %{{x}}</b><br><b>{test.name}</b><br>{params_join}<br>"
    return hover


class TestSuitePanelType(Enum):
    AGGREGATE = "aggregate"
    DETAILED = "detailed"


class DashboardPanelTestSuite(DashboardPanel):
    test_filters: List[TestFilter] = []
    filter: ReportFilter = ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True)
    panel_type: TestSuitePanelType = TestSuitePanelType.AGGREGATE
    time_agg: Optional[str] = None

    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        self.filter.include_test_suites = True

        points: Dict[datetime.datetime, Dict[Test, TestStatus]] = defaultdict(dict)
        for report in reports:
            if not self.filter.filter(report):
                continue
            if not isinstance(report, TestSuite):
                continue
            ts = self._to_period(report.timestamp)
            if self.test_filters:
                for test_filter in self.test_filters:
                    points[ts].update(test_filter.get(report))
            else:
                points[ts].update(TestFilter().get(report))

        if self.panel_type == TestSuitePanelType.AGGREGATE:
            fig = self._create_aggregate_fig(points)
        elif self.panel_type == TestSuitePanelType.DETAILED:
            fig = self._create_detailed_fig(points)
        else:
            raise ValueError(f"Unknown panel type {self.panel_type}")

        return plotly_figure(title=self.title, figure=fig, size=self.size)

    def _create_aggregate_fig(self, points: Dict[datetime.datetime, Dict[Test, TestStatus]]):
        dates = list(sorted(points.keys()))
        bars = [Counter(points[d].values()) for d in dates]
        fig = go.Figure(
            data=[
                go.Bar(name=status.value, x=dates, y=[c[status] for c in bars], marker_color=color)
                for status, color in tests_colors.items()
            ],
            layout={"showlegend": True},
        )
        fig.update_layout(barmode="stack")
        return fig

    def _create_detailed_fig(self, points: Dict[datetime.datetime, Dict[Test, TestStatus]]):
        dates = list(sorted(points.keys()))
        tests = list(set(t for p in points.values() for t in p.keys()))
        fig = go.Figure(
            data=[
                go.Bar(
                    name=test.name,
                    x=dates,
                    y=[1 for _ in range(len(dates))],
                    marker_color=[tests_colors.get(points[d].get(test, TestStatus.SKIPPED)) for d in dates],
                    hovertemplate=_get_test_hover(test),
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
                for status, col in tests_colors.items()
            ],
            layout={"showlegend": True},
        )
        fig.update_layout(
            barmode="stack",
            bargap=0.01,
            barnorm="fraction",
        )
        return fig

    def _to_period(self, timestamp: datetime.datetime) -> datetime.datetime:
        if self.time_agg is None:
            return timestamp
        return pd.Series([timestamp], name="dt").dt.to_period(self.time_agg)[0]


class DashboardPanelTestSuiteCounter(DashboardPanel):
    agg: CounterAgg = CounterAgg.NONE
    filter: ReportFilter = ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True)
    test_filters: List[TestFilter] = []
    statuses: List[TestStatus] = [TestStatus.SUCCESS]

    def _iter_statuses(self, reports: Iterable[ReportBase]):
        for report in reports:
            if not self.filter.filter(report):
                continue
            if not isinstance(report, TestSuite):
                continue
            if self.test_filters:
                for test_filter in self.test_filters:
                    yield report.timestamp, test_filter.get(report).values()
            else:
                yield report.timestamp, TestFilter().get(report).values()

    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        if self.agg == CounterAgg.NONE:
            statuses, postfix = self._build_none(reports)
        elif self.agg == CounterAgg.LAST:
            statuses, postfix = self._build_last(reports)
        else:
            raise ValueError(f"TestSuite Counter does not support agg {self.agg}")

        total = sum(statuses.values())
        value = sum(statuses[s] for s in self.statuses)
        statuses_join = ", ".join(s.value for s in self.statuses)
        return counter(counters=[CounterData(f"{value}/{total} {statuses_join}{postfix}", self.title)], size=self.size)

    def _build_none(self, reports: Iterable[ReportBase]) -> Tuple[Counter, str]:
        statuses: typing.Counter[TestStatus] = Counter()
        for _, values in self._iter_statuses(reports):
            statuses.update(values)
        return statuses, ""

    def _build_last(self, reports: Iterable[ReportBase]) -> Tuple[Counter, str]:
        last_ts = None
        statuses: typing.Counter[TestStatus] = Counter()
        for ts, values in self._iter_statuses(reports):
            if last_ts is None or ts > last_ts:
                last_ts = ts
                statuses = Counter(values)
        return statuses, f" ({last_ts})"


class DashboardConfig(BaseModel):
    name: str
    panels: List[DashboardPanel]

    def build_dashboard_info(self, reports: Iterable[ReportBase]) -> DashboardInfo:
        return DashboardInfo(self.name, widgets=[self.build_widget(p, reports) for p in self.panels])

    def build_widget(self, panel: DashboardPanel, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        try:
            return panel.build_widget(reports)
        except Exception as e:
            traceback.print_exc()
            return counter(counters=[CounterData(f"{e.__class__.__name__}: {e.args[0]}", "Error")])

    def add_panel(self, panel: DashboardPanel):
        self.panels.append(panel)


class Dashboard(Display):
    def __init__(self, config: DashboardConfig):
        super().__init__()
        self.reports: List[Report] = []
        self.config = config

    def add_report(self, report: Report):
        self.reports.append(report)

    def as_dict(
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        raise NotImplementedError

    def _get_payload(self) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def _parse_payload(cls, payload: Dict) -> T:
        raise NotImplementedError

    def _build_dashboard_info(self):
        return "er_" + str(uuid.uuid4()).replace("-", ""), self.config.build_dashboard_info(self.reports), {}
