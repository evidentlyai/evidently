import datetime
import traceback
import uuid
from collections import defaultdict
from functools import wraps
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import validator
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
from evidently.report import Report
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import ReportBase
from evidently.test_suite import TestSuite
from evidently.ui.dashboard.utils import getattr_nested

if TYPE_CHECKING:
    from evidently.ui.base import DataStorage


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


def assign_panel_id(f):
    @wraps(f)
    def inner(self: "DashboardPanel", *args, **kwargs) -> BaseWidgetInfo:
        r = f(self, *args, **kwargs)
        r.id = str(self.id)
        return r

    return inner


class DashboardPanel(EnumValueMixin, PolymorphicModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    filter: ReportFilter
    size: WidgetSize = WidgetSize.FULL

    # deprecated
    def build_widget(self, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        raise NotImplementedError

    def build(
        self,
        data_storage: "DataStorage",
        project_id: uuid.UUID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ):
        raise NotImplementedError


class DashboardTab(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: Optional[str] = "Untitled"


class DashboardConfig(BaseModel):
    name: str
    panels: List[DashboardPanel]
    tabs: List[DashboardTab] = []
    tab_id_to_panel_ids: Dict[str, List[str]] = defaultdict(list)

    def build_dashboard_info(self, reports: Iterable[ReportBase]) -> DashboardInfo:
        return DashboardInfo(self.name, widgets=[self.build_widget(p, reports) for p in self.panels])

    def build_widget(self, panel: DashboardPanel, reports: Iterable[ReportBase]) -> BaseWidgetInfo:
        try:
            return panel.build_widget(reports)
        except Exception as e:
            traceback.print_exc()
            return counter(counters=[CounterData(f"{e.__class__.__name__}: {e.args[0]}", "Error")])

    def add_panel(
        self,
        panel: DashboardPanel,
        *,
        tab: Optional[Union[str, uuid.UUID, DashboardTab]] = None,
        create_if_not_exists=True,
    ):
        self.panels.append(panel)

        if tab is None:
            return

        result_tab = self._get_or_create_tab(tab, create_if_not_exists)

        tab_id_str = str(result_tab.id)
        panel_id_str = str(panel.id)

        tab_panel_ids = self.tab_id_to_panel_ids[tab_id_str]

        if panel_id_str not in tab_panel_ids:
            tab_panel_ids.append(panel_id_str)

    def create_tab(self, title) -> DashboardTab:
        return self._get_or_create_tab(title)

    def _raise_if_tab_title_exists(self, tab_title: Optional[str]):
        if any(tab.title == tab_title for tab in self.tabs):
            raise ValueError(f"""tab with title "{tab_title}" already exists""")

    def _find_tab_by_id(self, tab_id: uuid.UUID) -> Optional[DashboardTab]:
        tabs = [t for t in self.tabs if t.id == tab_id]
        if len(tabs) == 0:
            return None
        return tabs[1]

    def _find_tab_by_title(self, title: str) -> Optional[DashboardTab]:
        tabs = [t for t in self.tabs if t.title == title]
        if len(tabs) == 0:
            return None
        return tabs[1]

    def _get_or_create_tab(
        self,
        tab_descriptor: Union[DashboardTab, uuid.UUID, str],
        create_if_not_exists=True,
    ) -> DashboardTab:
        tab: Optional[DashboardTab] = None
        to_create: Optional[DashboardTab] = None
        if isinstance(tab_descriptor, DashboardTab):
            tab = self._find_tab_by_id(tab_descriptor.id)
            to_create = tab_descriptor
        if isinstance(tab_descriptor, str):
            try:
                tab = self._find_tab_by_id(uuid.UUID(tab_descriptor))
            except ValueError:
                tab = self._find_tab_by_title(tab_descriptor)
                to_create = DashboardTab(title=tab_descriptor)
        if isinstance(tab_descriptor, uuid.UUID):
            tab = self._find_tab_by_id(tab_descriptor)

        if tab is not None:
            return tab

        if not create_if_not_exists or to_create is None:
            raise ValueError(f"""tab "{tab_descriptor}" not found""")

        self.tabs.append(to_create)
        return to_create


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
    def _parse_payload(cls, payload: Dict):
        raise NotImplementedError

    def _build_dashboard_info(self):
        return (
            "er_" + str(uuid.uuid4()).replace("-", ""),
            self.config.build_dashboard_info(self.reports),
            {},
        )


def build_dashboard(
    dashboard: DashboardConfig,
    data_storage: "DataStorage",
    project_id: uuid.UUID,
    timestamp_start: Optional[datetime.datetime],
    timestamp_end: Optional[datetime.datetime],
    reports_tmp,
) -> DashboardInfo:
    widgets = [
        build_panel_widget(p, data_storage, project_id, timestamp_start, timestamp_end)
        if isinstance(p, DashboardPanel)
        else p.build_widget(reports_tmp)
        for p in dashboard.panels
    ]

    return DashboardInfo(name=dashboard.name, widgets=widgets)


def build_panel_widget(
    panel: DashboardPanel,
    data_storage: "DataStorage",
    project_id: uuid.UUID,
    timestamp_start: Optional[datetime.datetime],
    timestamp_end: Optional[datetime.datetime],
) -> BaseWidgetInfo:
    try:
        return panel.build(data_storage, project_id, timestamp_start, timestamp_end)
    except Exception as e:
        traceback.print_exc()
        return counter(counters=[CounterData(f"{e.__class__.__name__}: {e.args[0]}", "Error")])
