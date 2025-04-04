import json
from typing import List

import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.metric_results import Distribution
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.report import Report


class MockMetricResult(MetricResult):
    class Config:
        alias_required = False
        dict_exclude_fields = {"series"}

    value: str
    series: pd.Series
    distribution: Distribution


class MockMetric(Metric[MockMetricResult]):
    class Config:
        alias_required = False

    def calculate(self, data: InputData) -> MockMetricResult:
        return MockMetricResult(value="a", series=pd.Series([0]), distribution=Distribution(x=[1, 1], y=[0, 0]))


@default_renderer(wrap_type=MockMetric)
class MockMetricRenderer(MetricRenderer):
    def render_html(self, obj) -> List[BaseWidgetInfo]:
        # todo?
        return []


def test_as_dict():
    report = Report(metrics=[MockMetric()])
    report.run(reference_data=pd.DataFrame(), current_data=pd.DataFrame())
    assert report.as_dict() == {"metrics": [{"metric": "MockMetric", "result": {"value": "a"}}]}
    include_series = report.as_dict(include={"MockMetric": {"value", "series"}})["metrics"][0]["result"]
    assert "series" in include_series
    assert (pd.Series([0]) == include_series["series"]).all()
    assert "distribution" not in include_series

    include_render = report.as_dict(include_render=True)["metrics"][0]["result"]

    assert "distribution" in include_render


def test_json():
    report = Report(metrics=[MockMetric()])
    report.run(reference_data=pd.DataFrame(), current_data=pd.DataFrame())
    default = json.loads(report.json())["metrics"]
    assert default == [{"metric": "MockMetric", "result": {"value": "a"}}]

    include_series = json.loads(report.json(include={"MockMetric": {"value", "series"}}))["metrics"]
    assert include_series == [{"metric": "MockMetric", "result": {"value": "a", "series": [0]}}]


def test_multirun_json():
    report = Report(metrics=[MockMetric()])
    report.run(reference_data=pd.DataFrame(), current_data=pd.DataFrame())
    report.run(reference_data=pd.DataFrame(), current_data=pd.DataFrame())  # 2nd run to check that report isn't changed
    default = json.loads(report.json())["metrics"]
    assert default == [{"metric": "MockMetric", "result": {"value": "a"}}]

    include_series = json.loads(report.json(include={"MockMetric": {"value", "series"}}))["metrics"]
    assert include_series == [{"metric": "MockMetric", "result": {"value": "a", "series": [0]}}]
