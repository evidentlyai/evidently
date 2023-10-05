import json
from typing import Dict

import pytest

from evidently._pydantic_compat import parse_obj_as
from evidently.base_metric import MetricResult
from evidently.descriptors import OOV
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import getattr_nested


class A(MetricResult):
    f: str


class B(MetricResult):
    f: Dict[str, A]
    f1: A


@pytest.mark.parametrize(
    "obj,path,value",
    [
        (A(f="a"), "f", "a"),
        (B(f={}, f1=A(f="a")), "f1.f", "a"),
        (B(f={"a": A(f="a")}, f1=A(f="b")), "f.a.f", "a"),
    ],
)
def test_getattr_nested(obj, path: str, value):
    assert getattr_nested(obj, path.split(".")) == value


def test_panel_value_metric_args_ser():
    pv = PanelValue(
        field_path="",
        metric_args={"col": OOV(display_name="OOV").for_column("Review_Text")},
    )

    pl = json.dumps(pv.dict())
    pv2 = parse_obj_as(PanelValue, json.loads(pl))

    assert pv2 == pv
