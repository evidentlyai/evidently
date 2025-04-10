import json
from typing import Dict

import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.base_metric import ColumnName
from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.base_metric import TResult
from evidently.legacy.descriptors import OOV
from evidently.legacy.ui.dashboards import PanelValue
from evidently.legacy.ui.dashboards.utils import _get_hover_params
from evidently.legacy.ui.dashboards.utils import getattr_nested
from evidently.pydantic_utils import EvidentlyBaseModel


class A(MetricResult):
    class Config:
        alias_required = False

    f: str


class B(MetricResult):
    class Config:
        alias_required = False

    f: Dict[str, A]
    f1: A


@pytest.mark.parametrize(
    "obj,path,value",
    [(A(f="a"), "f", "a"), (B(f={}, f1=A(f="a")), "f1.f", "a"), (B(f={"a": A(f="a")}, f1=A(f="b")), "f.a.f", "a")],
)
def test_getattr_nested(obj, path: str, value):
    assert getattr_nested(obj, path.split(".")) == value


def test_panel_value_metric_args_ser():
    pv = PanelValue(field_path="", metric_args={"col": OOV(display_name="OOV").for_column("Review_Text")})

    pl = json.dumps(pv.dict())
    pv2 = parse_obj_as(PanelValue, json.loads(pl))

    assert pv2 == pv


def test_panel_value_methic_hash_filter():
    class MyMetric(Metric[A]):
        class Config:
            alias_required = False

        arg: str

        def calculate(self, data: InputData) -> TResult:
            return A(f=self.arg)

    metric1 = MyMetric(arg="1")
    metric2 = MyMetric(arg="2")
    pv = PanelValue(field_path="value", metric_fingerprint=metric1.get_fingerprint())

    assert pv.metric_matched(metric1)
    assert not pv.metric_matched(metric2)


def test_metric_hover_template():
    class Nested(EvidentlyBaseModel):
        class Config:
            alias_required = False

        f: str

    class MyMetric(Metric[A]):
        class Config:
            alias_required = False

        arg: str
        n: Nested

        def calculate(self, data: InputData) -> TResult:
            return A(f=self.arg)

    m1 = MyMetric(arg="1", n=Nested(f="1"))
    m2 = MyMetric(arg="1", n=Nested(f="2"))
    m3 = MyMetric(arg="2", n=Nested(f="1"))

    assert _get_hover_params({m1}) == {m1: []}
    assert _get_hover_params({m1, m2}) == {m1: ["n.f: 1"], m2: ["n.f: 2"]}
    triple = _get_hover_params({m1, m2, m3})
    assert {m: set(lines) for m, lines in triple.items()} == {
        m1: {
            "n.f: 1",
            "arg: 1",
        },
        m2: {
            "n.f: 2",
            "arg: 1",
        },
        m3: {
            "n.f: 1",
            "arg: 2",
        },
    }


def test_metric_hover_template_column_name():
    class MyMetric(Metric[A]):
        class Config:
            alias_required = False

        column_name: ColumnName

        def calculate(self, data: InputData) -> TResult:
            return A(f="")

    m1 = MyMetric(column_name=ColumnName.from_any("col1"))
    m2 = MyMetric(column_name=ColumnName.from_any("col2"))

    assert _get_hover_params({m1, m2}) == {m1: ["column_name: col1"], m2: ["column_name: col2"]}
