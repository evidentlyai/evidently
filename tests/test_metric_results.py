import glob
import os
from enum import Enum
from importlib import import_module
from typing import Dict
from typing import List
from typing import Set
from typing import Type

import pytest

import evidently
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import Field
from evidently._pydantic_compat import parse_obj_as
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.tests.base_test import EnumValueMixin


@pytest.fixture
def all_metric_results():
    path = os.path.dirname(evidently.__file__)

    metric_result_field_classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = "evidently." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not MetricResult and issubclass(value, MetricResult):
                metric_result_field_classes.add(value)
    return metric_result_field_classes


def test_metric_result_fields_config(all_metric_results: Set[Type[MetricResult]]):
    errors = []
    for cls in all_metric_results:
        field_names = set(cls.__fields__)
        for config_field in (
            "pd_name_mapping",
            "dict_include_fields",
            "dict_exclude_fields",
            "pd_include_fields",
            "pd_exclude_fields",
        ):
            field_value = getattr(cls.__config__, config_field)
            if field_value is None:
                continue
            for field_name in field_value:
                if field_name not in field_names:
                    errors.append((cls, config_field, field_name))

    assert len(errors) == 0, f"Wrong config for field classes: {errors}"


class SimpleField(MetricResult):
    class Config:
        alias_required = False

    f1: str


class ExcludeModel(MetricResult):
    class Config:
        alias_required = False
        dict_exclude_fields = {"simple"}

    simple: SimpleField


@pytest.mark.parametrize("obj, expected", [(ExcludeModel(simple=SimpleField(f1="a")), {})])
def test_default_json(obj: MetricResult, expected):
    assert obj.get_dict() == expected


class FieldExclude(MetricResult):
    class Config:
        alias_required = False
        dict_exclude_fields = {"f2"}

    f1: str
    f2: List[int]


class FieldInclude(MetricResult):
    class Config:
        alias_required = False
        dict_include_fields = {"f1"}

    f1: str
    f2: List[int]


class DictExclude(MetricResult):
    class Config:
        alias_required = False
        dict_include = False

    f1: List[int]
    f2: List[int]


class NestedExclude(MetricResult):
    class Config:
        alias_required = False

    f: str
    nested: DictExclude


class Model(MetricResult):
    class Config:
        alias_required = False

    no: NestedExclude = Field(..., include={"nested": {"f1"}})
    fe: FieldExclude
    feo: FieldExclude = Field(include={"f1", "f2"})
    fi: FieldInclude
    de: DictExclude
    deo: DictExclude = Field(..., include=True)
    n: NestedExclude


@pytest.fixture
def model():
    data = []

    fe = FieldExclude(f1="a", f2=data)
    fi = FieldInclude(f1="a", f2=data)
    de = DictExclude(f1=data, f2=data)
    n = NestedExclude(f="a", nested=de)
    m = Model(fe=fe, fi=fi, feo=fe, de=de, deo=de, n=n, no=n)
    return m


@pytest.mark.parametrize(
    "include,exclude,expected",
    [
        (
            None,
            None,
            {
                "fe": {"f1": "a"},
                "feo": {"f1": "a", "f2": []},
                "fi": {"f1": "a"},
                "deo": {"f1": [], "f2": []},
                "n": {"f": "a"},
                "no": {"nested": {"f1": []}},
            },
        ),
        ({"n": {"f"}}, None, {"n": {"f": "a"}}),
        (None, {"n", "no", "deo", "feo"}, {"fe": {"f1": "a"}, "fi": {"f1": "a"}}),
    ],
)
def test_include_exclude(model: Model, include, exclude, expected):
    assert model.get_dict(include=include, exclude=exclude) == expected


class DictModel(MetricResult):
    class Config:
        alias_required = False

    de: Dict[str, DictExclude]
    deo: Dict[str, DictExclude] = Field(..., include=True)
    # fe: Dict[str, FieldExclude]
    # feo: Dict[str, FieldExclude] = Field(include={"f1", "f2"})


@pytest.fixture()
def dict_model():
    data = []

    # fe = FieldExclude(f1="a", f2=data)
    # fi = FieldInclude(f1="a", f2=data)
    de = {"a": DictExclude(f1=data, f2=data)}
    # n = NestedExclude(f="a", nested=de)
    return DictModel(de=de, deo=de)


@pytest.mark.parametrize(
    "include,exclude,expected",
    [
        (
            None,
            None,
            {
                "deo": {"a": {"f1": [], "f2": []}},
            },
        ),
    ],
)
def test_include_exclude_dict(dict_model: DictModel, include, exclude, expected):
    assert dict_model.get_dict(include=include, exclude=exclude) == expected


def test_polymorphic():
    class Parent(MetricResult):
        class Config:
            alias_required = False

    class A(Parent):
        class Config:
            dict_include_fields = {"f1"}
            alias_required = False

        f1: str
        f2: str

    class B(Parent):
        class Config:
            dict_exclude_fields = {"b"}
            alias_required = False

        a: str
        b: str

    class PModel(MetricResult):
        class Config:
            alias_required = False

        vals: Dict[str, Parent]

    assert PModel(vals={"a": A(f1="a", f2="b"), "b": B(a="a", b="b")}).get_dict() == {
        "vals": {"a": {"f1": "a"}, "b": {"a": "a"}}
    }


def test_model_enum():
    class MyEnum(Enum):
        A = "a"
        B = "b"

    class Container(EnumValueMixin, BaseModel):
        value: MyEnum

    obj = Container(value=MyEnum.A)
    assert obj.value == MyEnum.A
    d = obj.dict()
    assert d == {"value": "a"}
    obj2 = parse_obj_as(Container, d)
    assert obj2.value == MyEnum.A
    assert obj2 == obj


def test_model_list():
    class SimpleField(MetricResult):
        class Config:
            alias_required = False

        field: str
        field2: str

    class Container(MetricResult):
        class Config:
            alias_required = False

        field: List[SimpleField]

    obj = Container(field=[SimpleField(field="a", field2="b")])
    assert obj.get_dict() == {"field": [{"field": "a", "field2": "b"}]}
