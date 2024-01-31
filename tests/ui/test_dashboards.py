import json
from typing import Dict

import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.base_metric import TResult
from evidently.descriptors import OOV
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards.utils import getattr_nested


class A(MetricResult):
    f: str


class B(MetricResult):
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
        arg: str

        def calculate(self, data: InputData) -> TResult:
            return A(f=self.arg)

    metric1 = MyMetric(arg="1")
    metric2 = MyMetric(arg="2")
    pv = PanelValue(field_path="value", metric_hash=metric1.get_object_hash())

    assert pv.metric_matched(metric1)
    assert not pv.metric_matched(metric2)
