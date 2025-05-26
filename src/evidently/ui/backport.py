import datetime
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

from uuid6 import uuid7

from evidently.core.base_types import Label
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.metric_types import BoundTest
from evidently.core.metric_types import ByLabelCountValue
from evidently.core.metric_types import ByLabelValue
from evidently.core.metric_types import CountValue
from evidently.core.metric_types import MeanStdValue
from evidently.core.metric_types import Metric as MetricV2
from evidently.core.metric_types import MetricCalculationBase
from evidently.core.metric_types import MetricResult as MetricResultV2
from evidently.core.metric_types import MetricTestResult
from evidently.core.metric_types import SingleValue
from evidently.core.metric_types import TResult
from evidently.core.report import Context
from evidently.core.report import Snapshot as SnapshotV2
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric as MetricV1
from evidently.legacy.base_metric import MetricResult as MetricResultV1
from evidently.legacy.core import ColumnType
from evidently.legacy.core import new_id
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.options.base import Options
from evidently.legacy.pipeline.column_mapping import RecomType
from evidently.legacy.pipeline.column_mapping import TargetNames
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.suite.base_suite import ContextPayload
from evidently.legacy.suite.base_suite import RunMetadata
from evidently.legacy.suite.base_suite import Snapshot as SnapshotV1
from evidently.legacy.tests.base_test import Test as TestV1
from evidently.legacy.tests.base_test import TestParameters
from evidently.legacy.tests.base_test import TestResult as TestResultV1
from evidently.legacy.ui.dashboards import DashboardPanelPlot
from evidently.legacy.ui.dashboards.base import DashboardPanel
from evidently.legacy.ui.dashboards.base import PanelValue
from evidently.legacy.ui.dashboards.base import ReportFilter
from evidently.legacy.ui.dashboards.utils import PlotType
from evidently.legacy.ui.errors import EvidentlyServiceError
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.utils.data_preprocessing import ColumnDefinition
from evidently.legacy.utils.data_preprocessing import DataDefinition as DataDefinitionV1
from evidently.legacy.utils.data_preprocessing import FeatureDefinition
from evidently.legacy.utils.data_preprocessing import PredictionColumns
from evidently.pydantic_utils import Fingerprint
from evidently.pydantic_utils import IncludeTags

if TYPE_CHECKING:
    from evidently.legacy.ui.base import DataStorage


class MetricResultV2Adapter(MetricResultV1):
    class Config:
        type_alias = "evidently:metric_result:MetricResultV2Adapter"

    widget: List[dict]


class PresetMetricValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:PresetMetricValueV1"


class SingleValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:SingleValueV1"

    value: Union[float, int, str]


class ByLabelValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:ByLabelValueV1"
        field_tags = {"values": {IncludeTags.Render}}

    values: Dict[Label, Union[float, int, bool, str]]


class ByLabelCountValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:ByLabelCountValueV1"
        field_tags = {"values": {IncludeTags.Render}}

    counts: Dict[Label, int]
    shares: Dict[Label, float]


class CountValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:CountValueV1"

    count: int
    share: float


class MeanStdValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:MeanStdValueV1"

    mean: float
    std: float


def _create_metric_result_widget(metric_result: MetricResultV2, ignore_widget: bool) -> List[dict]:
    if ignore_widget:
        return []
    widgets = list(metric_result.get_widgets())
    return [w.dict() for w in widgets]


def metric_result_v2_to_v1(metric_result: MetricResultV2, ignore_widget: bool = False) -> MetricResultV1:
    if isinstance(metric_result, SingleValue):
        return SingleValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            value=metric_result.value,
        )
    if isinstance(metric_result, ByLabelValue):
        return ByLabelValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            values={k: v.value for k, v in metric_result.values.items()},
        )
    if isinstance(metric_result, ByLabelCountValue):
        return ByLabelCountValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            counts={k: v.value for k, v in metric_result.counts.items()},
            shares={k: v.value for k, v in metric_result.shares.items()},
        )
    if isinstance(metric_result, CountValue):
        return CountValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            count=metric_result.count.value,
            share=metric_result.share.value,
        )
    if isinstance(metric_result, MeanStdValue):
        return MeanStdValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            mean=metric_result.mean.value,
            std=metric_result.std.value,
        )
    raise NotImplementedError(metric_result.__class__.__name__)


class MetricV2Adapter(MetricV1[MetricResultV2Adapter]):
    class Config:
        type_alias = "evidently:metric:MetricV2Adapter"

    metric: Union[MetricV2, dict]
    fingerprint: Fingerprint = ""

    def calculate(self, data: InputData) -> MetricResultV2Adapter:
        raise NotImplementedError()

    def get_fingerprint(self) -> Fingerprint:
        if self.fingerprint != "":
            return self.fingerprint
        assert isinstance(self.metric, MetricV2), "fingerprint should be present for unknown metrics"
        return self.metric.get_fingerprint()


class MetricV2PresetAdapter(MetricV1[MetricResultV2Adapter]):
    class Config:
        type_alias = "evidently:metric:MetricV2PresetAdapter"

    id: str

    def calculate(self, data: InputData) -> MetricResultV2Adapter:
        raise NotImplementedError()


@default_renderer(MetricV2PresetAdapter)
class MetricV2PresetAdapterRenderer(MetricRenderer):
    def render_html(self, obj: MetricV2PresetAdapter) -> List[BaseWidgetInfo]:
        return [BaseWidgetInfo.parse_obj(w) for w in obj.get_result().widget]


@default_renderer(MetricV2Adapter)
class MetricV2AdapterRenderer(MetricRenderer):
    def render_html(self, obj: MetricV2Adapter) -> List[BaseWidgetInfo]:
        return [BaseWidgetInfo.parse_obj(w) for w in obj.get_result().widget]


def metric_v2_to_v1(metric: MetricV2) -> MetricV1:
    return MetricV2Adapter(metric=metric, fingerprint=metric.get_fingerprint())


def data_definition_v2_to_v1(dd: DataDefinition, reference_present: bool) -> DataDefinitionV1:
    """For now, only columns field is used"""
    columns: Dict[str, ColumnDefinition] = {
        **{col: ColumnDefinition(col, ColumnType.Numerical) for col in (dd.numerical_columns or [])},
        **{col: ColumnDefinition(col, ColumnType.Text) for col in (dd.text_columns or [])},
        **{col: ColumnDefinition(col, ColumnType.Categorical) for col in (dd.categorical_columns or [])},
    }
    target: Optional[ColumnDefinition] = None
    prediction_columns: Optional[PredictionColumns] = None
    id_column: Optional[ColumnDefinition] = None
    datetime_column: Optional[ColumnDefinition] = None
    embeddings: Optional[Dict[str, List[str]]] = None
    user_id: Optional[ColumnDefinition] = None
    item_id: Optional[ColumnDefinition] = None

    task: Optional[str] = None
    classification_labels: Optional[TargetNames] = None
    recommendations_type: Optional[RecomType] = None
    return DataDefinitionV1(
        columns=columns,
        target=target,
        prediction_columns=prediction_columns,
        id_column=id_column,
        datetime_column=datetime_column,
        embeddings=embeddings,
        user_id=user_id,
        item_id=item_id,
        task=task,
        classification_labels=classification_labels,
        reference_present=reference_present,
        recommendations_type=recommendations_type,
    )


def snapshot_v2_to_v1(snapshot: SnapshotV2) -> SnapshotV1:
    metrics: List[MetricV1] = []
    metric_results: List[MetricResultV1] = []
    tests: List[TestV1] = []
    tests_v2: List[MetricTestResult] = []
    test_results: List[TestResultV1] = []
    context = snapshot.context
    saved_metrics = set()
    calculation: MetricCalculationBase
    for item in snapshot._snapshot_item:
        if item.metric_id is not None:
            calculation = context.get_metric(item.metric_id)
            metric = calculation.to_metric()
            metric_result = context.get_metric_result(item.metric_id)
            metrics.append(metric_v2_to_v1(metric))
            metric_results.append(metric_result_v2_to_v1(metric_result))
            saved_metrics.add(item.metric_id)

            for test_result in metric_result.tests or []:
                tests_v2.append(test_result)
                tests.append(TestV2Adapter(test=test_result.bound_test))
                test_results.append(
                    TestResultV1(
                        name=test_result.name,
                        description=test_result.description,
                        status=test_result.status,
                        group="",
                        parameters=TestV2Parameters(),
                    )
                )
        else:  # metric preset wrapper
            adapter = MetricV2PresetAdapter(id=str(uuid7()))
            metrics.append(adapter)
            metric_results.append(PresetMetricValueV1(widget=[w.dict() for w in item.widgets]))

    for metric_id, metric_result in context._metrics.items():
        if metric_id in saved_metrics:
            continue
        calculation = context.get_metric(metric_id)
        metric = calculation.to_metric()
        metrics.append(metric_v2_to_v1(metric))
        metric_results.append(metric_result_v2_to_v1(metric_result, ignore_widget=True))

        for test_result in metric_result.tests or []:
            tests_v2.append(test_result)
            tests.append(TestV2Adapter(test=test_result.bound_test))
            test_results.append(
                TestResultV1(
                    name=test_result.name,
                    description=test_result.description,
                    status=test_result.status,
                    group="",
                    parameters=TestV2Parameters(),
                )
            )

    descriptors = {
        x: FeatureDefinition(
            feature_name=x,
            display_name=x,
            feature_type=ColumnType.Categorical,
            feature_class="",
        )
        for x in context.data_definition.categorical_descriptors
    }
    descriptors.update(
        {
            x: FeatureDefinition(
                feature_name=x,
                display_name=x,
                feature_type=ColumnType.Numerical,
                feature_class="",
            )
            for x in context.data_definition.numerical_descriptors
        }
    )
    snapshot_v1 = SnapshotV1(
        id=new_id(),
        name="",
        timestamp=snapshot._timestamp,
        metadata=dict(snapshot._metadata),
        tags=snapshot._tags,
        suite=ContextPayload(
            metrics=metrics,
            metric_results=metric_results,
            tests=tests,
            test_results=test_results,
            data_definition=data_definition_v2_to_v1(context.data_definition, context._input_data[1] is not None),
            run_metadata=RunMetadata(descriptors=descriptors),
        ),
        metrics_ids=list(range(len(metrics))),
        test_ids=[],
        options=Options.from_any_options(None),
    )
    snapshot_v1.metadata["version"] = "2"
    if len(tests) > 0:
        test_widgets = snapshot_v1.as_test_suite()._build_dashboard_info()[1].widgets
        tests_config = TestsConfig(tests=[v.test_config for v in tests_v2])
        snapshot_v1.suite.metrics.append(
            MetricV2Adapter(metric=tests_config, fingerprint=tests_config.get_fingerprint())
        )
        widgets_dict = [w.dict() for w in test_widgets]
        for wd in widgets_dict:
            params = wd.get("params", {})
            params["v2_test"] = True
            wd["params"] = params
        snapshot_v1.suite.metric_results.append(SingleValueV1(widget=widgets_dict, value=0))
        snapshot_v1.metrics_ids.append(len(metrics))

    return snapshot_v1


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
    # fixme: needed for deduplication
    test: BoundTest

    def check(self) -> TestResultV1:
        raise NotImplementedError

    def groups(self) -> Dict[str, str]:
        return {}


class TestV2Parameters(TestParameters):
    class Config:
        type_alias = "evidently:test_parameters:TestV2Parameters"


class TestsConfig(MetricV2):
    tests: List[dict] = []

    def to_calculation(self):
        raise NotImplementedError

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        raise NotImplementedError

    def get_bound_tests(self, context: Context) -> List[BoundTest]:
        raise NotImplementedError


def main():
    import pandas as pd

    from evidently.core.report import Report as ReportV2
    from evidently.legacy.ui.workspace import Workspace
    from evidently.metrics import MeanValue
    from evidently.tests import lte

    def create_snapshot(i):
        df = pd.DataFrame({"col": list(range(i + 5))})
        dataset = Dataset.from_pandas(
            df,
            data_definition=DataDefinition(numerical_columns=["col"]),
        )
        report = ReportV2([MeanValue(column="col", tests=[lte(4)])])
        snapshot_v2 = report.run(dataset, None, timestamp=datetime.datetime.now() - datetime.timedelta(days=1))

        return snapshot_v2

    # ws = RemoteWorkspace("http://127.0.0.1:8000")
    ws = Workspace.create("./workspace")
    from evidently.legacy.ui.type_aliases import ZERO_UUID

    try:
        project = ws.get_project(ZERO_UUID)
    except EvidentlyServiceError:
        project = None
    if project is None:
        from evidently.legacy.ui.base import Project

        project = ws.add_project(Project(id=ZERO_UUID, name="test proj"))

        project.dashboard.add_panel(SingleValueDashboardPanel(metric_id="mean:col"))
        project.save()

    # snapshot_v1 = create_snapshot(0)
    # snapshot_v1.save("snapshot_v1.json")
    # SnapshotV1.load("snapshot_v1.json")

    for i in range(10):
        project.add_snapshot(create_snapshot(i))


if __name__ == "__main__":
    main()
