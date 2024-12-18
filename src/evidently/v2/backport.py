import datetime
from typing import List
from typing import Union

import pandas as pd

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
from evidently.tests.base_test import TestResult as TestResultV1
from evidently.v2.datasets import Dataset
from evidently.v2.metrics import Metric as MetricV2
from evidently.v2.metrics import MetricResult as MetricResultV2
from evidently.v2.metrics import SingleValue
from evidently.v2.metrics import column_mean
from evidently.v2.report import Report as ReportV2
from evidently.v2.report import Snapshot as SnapshotV2


class MetricResultV2Adapter(MetricResultV1):
    class Config:
        type_alias = "evidently:metric_result:MetricResultV2Adapter"

    widget: List[BaseWidgetInfo]


class SingleValueV1(MetricResultV2Adapter):
    class Config:
        type_alias = "evidently:metric_result:SingleValueV1"

    value: Union[float, int, str]


def metric_result_v2_to_v1(metric_result: MetricResultV2) -> MetricResultV1:
    if isinstance(metric_result, SingleValue):
        return SingleValueV1(widget=metric_result.widget, value=metric_result.value)
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
        return obj.get_result().widget


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
        metrics_ids=[],
        test_ids=[],
        options=Options.from_any_options(None),
    )


def main():
    df = pd.DataFrame({"col": [1, 2, 3]})
    dataset = Dataset.from_pandas(df)
    report = ReportV2([column_mean("col")])
    snapshot_v2 = report.run(dataset, None)

    snapshot_v1 = snapshot_v2_to_v1(snapshot_v2)
    snapshot_v1.save("snapshot_v1.json")

    snapshot_v1 = SnapshotV1.load("snapshot_v1.json")


if __name__ == "__main__":
    main()
