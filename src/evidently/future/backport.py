import dataclasses
import datetime
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

from uuid6 import uuid7

from evidently.base_metric import InputData
from evidently.base_metric import Metric as MetricV1
from evidently.base_metric import MetricResult as MetricResultV1
from evidently.core import ColumnType
from evidently.core import new_id
from evidently.future.datasets import DataDefinition
from evidently.future.datasets import Dataset
from evidently.future.metric_types import BoundTest
from evidently.future.metric_types import ByLabelValue
from evidently.future.metric_types import CountValue
from evidently.future.metric_types import MeanStdValue
from evidently.future.metric_types import Metric as MetricV2
from evidently.future.metric_types import MetricCalculationBase
from evidently.future.metric_types import MetricResult as MetricResultV2
from evidently.future.metric_types import MetricTestResult
from evidently.future.metric_types import SingleValue
from evidently.future.metric_types import TResult
from evidently.future.report import Context
from evidently.future.report import Snapshot as SnapshotV2
from evidently.metric_results import Label
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import PlotlyGraphInfo
from evidently.options.base import Options
from evidently.pipeline.column_mapping import RecomType
from evidently.pipeline.column_mapping import TargetNames
from evidently.pydantic_utils import Fingerprint
from evidently.pydantic_utils import IncludeTags
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.suite.base_suite import ContextPayload
from evidently.suite.base_suite import RunMetadata
from evidently.suite.base_suite import Snapshot as SnapshotV1
from evidently.tests.base_test import Test as TestV1
from evidently.tests.base_test import TestParameters
from evidently.tests.base_test import TestResult as TestResultV1
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.dashboards.base import PanelValue
from evidently.ui.dashboards.base import ReportFilter
from evidently.ui.dashboards.utils import PlotType
from evidently.ui.errors import EvidentlyServiceError
from evidently.ui.type_aliases import ProjectID
from evidently.utils.data_preprocessing import ColumnDefinition
from evidently.utils.data_preprocessing import DataDefinition as DataDefinitionV1
from evidently.utils.data_preprocessing import FeatureDefinition
from evidently.utils.data_preprocessing import PredictionColumns

if TYPE_CHECKING:
    from evidently.ui.base import DataStorage


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
    widgets = list(metric_result.widget)
    return [dataclasses.asdict(w) for w in widgets]


def metric_result_v2_to_v1(metric_result: MetricResultV2, ignore_widget: bool = False) -> MetricResultV1:
    if isinstance(metric_result, SingleValue):
        return SingleValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            value=metric_result.value,
        )
    if isinstance(metric_result, ByLabelValue):
        return ByLabelValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            values=metric_result.values,
        )
    if isinstance(metric_result, CountValue):
        return CountValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            count=metric_result.count,
            share=metric_result.share,
        )
    if isinstance(metric_result, MeanStdValue):
        return MeanStdValueV1(
            widget=_create_metric_result_widget(metric_result, ignore_widget),
            mean=metric_result.mean,
            std=metric_result.std,
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


def _unwrap_widget_info(data: dict) -> BaseWidgetInfo:
    base_version = BaseWidgetInfo(**data)
    if base_version.widgets is not None and isinstance(base_version.widgets, list):
        for idx, item in enumerate(base_version.widgets):
            base_version.widgets[idx] = _unwrap_widget_info(item)
    if base_version.additionalGraphs is not None and isinstance(base_version.additionalGraphs, list):
        for idx, item in enumerate(base_version.additionalGraphs):
            if "type" in item:
                base_version.additionalGraphs[idx] = _unwrap_widget_info(item)
            elif "data" in item:
                base_version.additionalGraphs[idx] = PlotlyGraphInfo(**item)
            else:
                base_version.additionalGraphs[idx] = AdditionalGraphInfo(**item)
    return base_version


@default_renderer(MetricV2PresetAdapter)
class MetricV2PresetAdapterRenderer(MetricRenderer):
    def render_html(self, obj: MetricV2PresetAdapter) -> List[BaseWidgetInfo]:
        return [_unwrap_widget_info(w) for w in obj.get_result().widget]


@default_renderer(MetricV2Adapter)
class MetricV2AdapterRenderer(MetricRenderer):
    def render_html(self, obj: MetricV2Adapter) -> List[BaseWidgetInfo]:
        return [_unwrap_widget_info(w) for w in obj.get_result().widget]


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
    tests_v2: List[BoundTest] = []
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

            for test_config, test_result in (metric_result._tests or {}).items():
                tests_v2.append(test_config)
                tests.append(TestV2Adapter(test=test_config))
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
            metric_results.append(PresetMetricValueV1(widget=[dataclasses.asdict(w) for w in item.widgets]))

    for metric_id, metric_result in context._metrics.items():
        if metric_id in saved_metrics:
            continue
        calculation = context.get_metric(metric_id)
        metric = calculation.to_metric()
        metrics.append(metric_v2_to_v1(metric))
        metric_results.append(metric_result_v2_to_v1(metric_result, ignore_widget=True))

        for test_config, test_result in (metric_result._tests or {}).items():
            tests_v2.append(test_config)
            tests.append(TestV2Adapter(test=test_config))
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
    snapshot = SnapshotV1(
        id=new_id(),
        name="",
        timestamp=snapshot.report._timestamp,
        metadata=dict(snapshot.report.metadata),
        tags=snapshot.report.tags,
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
    snapshot.metadata["version"] = "2"
    if len(tests) > 0:
        test_widgets = snapshot.as_test_suite()._build_dashboard_info()[1].widgets
        tests_config = TestsConfig(tests=tests_v2)
        snapshot.suite.metrics.append(MetricV2Adapter(metric=tests_config, fingerprint=tests_config.get_fingerprint()))
        widgets_dict = [dataclasses.asdict(w) for w in test_widgets]
        for wd in widgets_dict:
            params = wd.get("params", {})
            params["v2_test"] = True
            wd["params"] = params
        snapshot.suite.metric_results.append(SingleValueV1(widget=widgets_dict, value=0))
        snapshot.metrics_ids.append(len(metrics))

    return snapshot


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
    tests: List[BoundTest] = []

    def to_calculation(self):
        raise NotImplementedError

    def get_tests(self, value: TResult) -> Generator[MetricTestResult, None, None]:
        raise NotImplementedError

    def get_bound_tests(self, context: Context) -> List[BoundTest]:
        return self.tests


def main():
    import pandas as pd

    from evidently.future.metrics import MeanValue
    from evidently.future.report import Report as ReportV2
    from evidently.future.tests import lte
    from evidently.ui.workspace import Workspace

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
    from evidently.ui.type_aliases import ZERO_UUID

    try:
        project = ws.get_project(ZERO_UUID)
    except EvidentlyServiceError:
        project = None
    if project is None:
        from evidently.ui.base import Project

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
