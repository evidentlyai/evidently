import dataclasses
import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from evidently import ColumnMapping
from evidently.base_metric import InputData
from evidently.base_metric import Metric as MetricV1
from evidently.base_metric import MetricResult as MetricResultV1
from evidently.core import ColumnType
from evidently.core import new_id
from evidently.model.widget import BaseWidgetInfo
from evidently.options.base import Options
from evidently.pydantic_utils import FieldPath
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.suite.base_suite import ContextPayload
from evidently.suite.base_suite import Snapshot as SnapshotV1
from evidently.tests.base_test import Test as TestV1
from evidently.tests.base_test import TestResult as TestResultV1
from evidently.ui.base import DataStorage
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.dashboards.base import PanelValue
from evidently.ui.dashboards.base import ReportFilter
from evidently.ui.dashboards.utils import PlotType
from evidently.ui.dashboards.utils import getattr_nested
from evidently.ui.type_aliases import ProjectID
from evidently.utils.data_preprocessing import ColumnDefinition
from evidently.utils.data_preprocessing import DataDefinition as DataDefinitionV1
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric as MetricV2
from evidently.v2.metrics import MetricResult as MetricResultV2
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics.base import Check
from evidently.v2.metrics.base import MetricId
from evidently.v2.metrics.base import SingleValueCheck
from evidently.v2.metrics.base import TResult
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

    metric: MetricV2

    def calculate(self, data: InputData) -> MetricResultV2Adapter:
        raise NotImplementedError


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

    return SnapshotV1(
        id=new_id(),
        name="",
        timestamp=datetime.datetime.now(),
        metadata={},
        tags=[],
        suite=ContextPayload(metrics=metrics, metric_results=metric_results, tests=tests, test_results=test_results),
        metrics_ids=list(range(len(metrics))),
        test_ids=[],
        options=Options.from_any_options(None),
    )


class DashboardPanelV2(DashboardPanel):
    class Config:
        type_alias = "evidently.v2.backport.DashboardPanelV2"


class SingleValueDashboardPanel(DashboardPanelV2):
    class Config:
        type_alias = "evidently.v2.backport.SingleValueDashboardPanel"

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


V1Result = TypeVar("V1Result", bound=MetricResultV1)


class MetricV1Adapter(MetricV2[TResult]):
    metric: MetricV1[V1Result]

    def calculate(self, current_data: Dataset, reference_data: Optional[Dataset]) -> TResult:
        # fixme
        # columns: Dict[str, ColumnDefinition] = {k: ColumnDefinition(k, v.type) for k, v in current_data._data_definition._columns.items()}
        columns: Dict[str, ColumnDefinition] = {
            k: ColumnDefinition(k, ColumnType.Numerical) for k, _ in current_data._data_definition._columns.items()
        }
        dd = DataDefinitionV1(columns=columns, reference_present=reference_data is not None)
        data = InputData(
            reference_data=reference_data.as_dataframe() if reference_data is not None else None,
            current_data=current_data.as_dataframe(),
            additional_data={},
            column_mapping=ColumnMapping(),
            data_definition=dd,
        )
        result = self.metric.calculate(data)  # todo: need cache/deduplication
        return self.extract_value(result)

    def extract_value(self, result: V1Result) -> TResult:
        raise NotImplementedError

    def display_name(self) -> str:
        return self.metric.get_id()  # todo


class SingleValueMetricV1Adapter(MetricV1Adapter[SingleValue]):
    class Config:
        type_alias = "evidently:metric2:SingleValueMetricV1Adapter"

    field_path: Union[str, FieldPath]

    def __init__(
        self, metric_id: MetricId, metric: MetricV1, field_path: FieldPath, checks: Optional[List[Check]] = None, **data
    ) -> None:
        self.field_path = field_path
        self.metric = metric
        super().__init__(metric_id, checks)

    def extract_value(self, result: V1Result) -> SingleValue:
        value = getattr_nested(result, self.field_path_str.split("."))
        return SingleValue(value)

    @property
    def field_path_str(self) -> str:
        if isinstance(self.field_path, str):
            return self.field_path
        return self.field_path.get_path()


def column_mean_v1(column: str, checks: Optional[List[SingleValueCheck]] = None):
    from evidently.metrics import ColumnSummaryMetric

    return SingleValueMetricV1Adapter(
        metric_id="column_mean_v1",
        metric=ColumnSummaryMetric(column),
        field_path=FieldPath("current_characteristics.mean".split("."), ColumnSummaryMetric.result_type()),
    )


def main():
    import pandas as pd

    from evidently.ui.workspace import Workspace
    from evidently.v2.datasets import Dataset
    from evidently.v2.metrics import column_mean
    from evidently.v2.report import Report as ReportV2

    def create_snapshot(i):
        df = pd.DataFrame({"col": list(range(i + 5))})
        dataset = Dataset.from_pandas(df)
        report = ReportV2([column_mean("col"), column_mean_v1("col")])
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
