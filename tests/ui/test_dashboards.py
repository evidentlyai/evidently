from typing import Dict

import pytest

from evidently.base_metric import MetricResult
from evidently.ui.dashboards import getattr_nested


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
