import dataclasses
import datetime
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from evidently.base_metric import InputData
from evidently.base_metric import Metric as MetricV1
from evidently.base_metric import MetricResult as MetricResultV1
from evidently.core import new_id
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import Options
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.suite.base_suite import ContextPayload
from evidently.suite.base_suite import Snapshot as SnapshotV1
from evidently.tests.base_test import Test as TestV1
from evidently.tests.base_test import TestParameters
from evidently.tests.base_test import TestResult as TestResultV1
from evidently.ui.base import DataStorage
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.dashboards.base import PanelValue
from evidently.ui.dashboards.base import ReportFilter
from evidently.ui.dashboards.utils import PlotType
from evidently.ui.type_aliases import ProjectID
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric as MetricV2
from evidently.v2.metrics import MetricResult as MetricResultV2
from evidently.v2.metrics import SingleValue
from evidently.v2.report import Snapshot as SnapshotV2


class MetricResultV2Adapter(MetricResultV1):
    class Config:
        type_alias = "evidently:metric_result:MetricResultV2Adapter"

    widget: List[dict]


class SingleValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:SingleValueV1"

    value: Union[float, int, str]


def metric_result_v2_to_v1(metric_result: MetricResultV2) -> MetricResultV1:
    if isinstance(metric_result, SingleValue):
        return SingleValueV1(widget=[dataclasses.asdict(w) for w in metric_result.widget], value=metric_result.value)
    raise NotImplementedError(metric_result.__class__.__name__)


class MetricV2Adapter(MetricV1[MetricResultV2Adapter]):
    class Config:
        type_alias = "evidently:metric:MetricV2Adapter"

    def calculate(self, data: InputData) -> MetricResultV2Adapter:
        pass


@default_renderer(MetricV2Adapter)
class MetricV2AdapterRenderer(MetricRenderer):
    def render_html(self, obj: MetricV2Adapter) -> List[BaseWidgetInfo]:
        return [BaseWidgetInfo(**w) for w in obj.get_result().widget]


def metric_v2_to_v1(metric: MetricV2) -> MetricV1:
    return MetricV2Adapter(metric=metric)


def snapshot_v2_to_v1(snapshot: SnapshotV2) -> SnapshotV1:
    metrics: List[MetricV1] = []
    metric_results: List[MetricResultV1] = []
    tests: List[TestV1] = []
    test_results: List[TestResultV1] = []
    context = snapshot.context
    for metric_id, metric_result in context._metrics.items():
        metric = context.get_metric(metric_id)
        metrics.append(metric_v2_to_v1(metric))
        metric_results.append(metric_result_v2_to_v1(metric_result))

        for test in metric_result.tests or ():
            tests.append(TestV2Adapter())
            test_results.append(
                TestResultV1(
                    name=test.name,
                    description=test.description,
                    status=test.status,
                    group="",
                    parameters=TestV2Parameters(),
                )
            )

    return SnapshotV1(
        id=new_id(),
        name="",
        timestamp=datetime.datetime.now(),
        metadata={},
        tags=[],
        suite=ContextPayload(metrics=metrics, metric_results=metric_results, tests=tests, test_results=test_results),
        metrics_ids=list(range(len(metrics))) if not tests else [],
        test_ids=list(range(len(tests))),
        options=Options.from_any_options(None),
    )


class DashboardPanelV2(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelV2"


class SingleValueDashboardPanel(DashboardPanelV2):
    class Config:
        type_alias = "evidently:dashboard_panel:SingleValueDashboardPanel"

    title: str = ""
    filter: ReportFilter = ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True)
    metric_id: str

    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> BaseWidgetInfo:
        values = [PanelValue(field_path="value", metric_args={"metric.metric_id": self.metric_id})]
        panel = DashboardPanelPlot(values=values, plot_type=PlotType.LINE, filter=self.filter, title="")
        return await panel.build(data_storage, project_id, timestamp_start, timestamp_end)


class TestV2Adapter(TestV1):
    class Config:
        type_alias = "evidently:test:TestV2Adapter"

    name: ClassVar[str] = "TestV2Adapter"
    group: ClassVar[str] = "TestV2Adapter"

    def check(self) -> TestResultV1:
        raise NotImplementedError

    def groups(self) -> Dict[str, str]:
        return {}


class TestV2Parameters(TestParameters):
    class Config:
        type_alias = "evidently:test_parameters:TestV2Parameters"


def main():
    import pandas as pd

    from evidently.ui.workspace import Workspace
    from evidently.v2.metrics import column_mean
    from evidently.v2.report import Report as ReportV2
    from evidently.v2.tests.numerical_checks import le

    def create_snapshot(i):
        df = pd.DataFrame({"col": list(range(i + 5))})
        dataset = Dataset.from_pandas(df)
        report = ReportV2([column_mean("col", [le(4)])])
        snapshot_v2 = report.run(dataset, None)

        snapshot_v1 = snapshot_v2_to_v1(snapshot_v2)
        import uuid6

        snapshot_v1.id = uuid6.UUID(int=i, version=7)
        snapshot_v1.timestamp = datetime.datetime.now() - datetime.timedelta(days=1)
        return snapshot_v1

    ws = Workspace.create("./workspace")
    from evidently.ui.type_aliases import ZERO_UUID

    project = ws.get_project(ZERO_UUID)
    if project is None:
        from evidently.ui.base import Project

        project = ws.add_project(Project(id=ZERO_UUID, name="test proj"))

        project.dashboard.add_panel(SingleValueDashboardPanel(metric_id="mean:col"))
        project.save()

    snapshot_v1 = create_snapshot(0)
    snapshot_v1.save("snapshot_v1.json")
    SnapshotV1.load("snapshot_v1.json")

    for i in range(10):
        project.add_snapshot(create_snapshot(i))


if __name__ == "__main__":
    main()
