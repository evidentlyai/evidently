import abc
import glob
import json
import os
from importlib import import_module
from inspect import isabstract
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import evidently
from evidently._pydantic_compat import BaseModel
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.report import Report
from evidently.legacy.utils.types import ApproxValue
from evidently.pydantic_utils import PolymorphicModel
from tests.conftest import smart_assert_equal


class TestOutcome:
    @abc.abstractmethod
    def check(self, report: Report):
        raise NotImplementedError


class Error(TestOutcome):
    def __init__(self, exception_type: Type[Exception], match: str = None):
        self.exception_type = exception_type
        self.match = match

    def check(self, report: Report):
        pass


class AssertResultFields(TestOutcome):
    def __init__(self, values: Dict[str, Any]):
        # todo: nested keys
        self.values = values

    def check(self, report: Report):
        result_json = report.json()
        result = json.loads(result_json)["metrics"][0]["result"]

        for key, value in self.values.items():
            assert result[key] == value


class AssertExpectedResult(TestOutcome):
    def __init__(self, result: MetricResult, metric: Optional[Metric] = None):
        self.metric = metric
        self.result = result

    def check(self, report: Report):
        if self.metric is None:
            metrics = list(report._inner_suite.context.metric_results.keys())
            if len(metrics) != 1:
                raise ValueError(
                    f"Metric is not specified for AssertExpectedResult and context does not contain exactly 1 metric: {metrics}"
                )
            metric = metrics[0]
        else:
            metric = self.metric
        result = report._inner_suite.context.metric_results[metric]
        smart_assert_equal(result, self.result)


class CustomAssert(TestOutcome):
    def __init__(self, custom_check: Callable[[Report], None]):
        self.custom_check = custom_check

    def check(self, report: Report):
        self.custom_check(report)


class NoopOutcome(TestOutcome):
    def check(self, report: Report):
        pass


def find_all_subclasses(
    base: Type,
    base_module: str = "evidently",
    path: str = os.path.dirname(evidently.__file__),
    include_abstract: bool = False,
):
    classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = f"{base_module}." + mod_path.replace("/", ".").replace("\\", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not base and issubclass(value, base):
                if not isabstract(value) or include_abstract:
                    classes.add(value)

    return classes


T = TypeVar("T", bound=BaseModel)


def make_approx_type(cls: Type[T], ignore_not_set: bool = False) -> Type[T]:
    class ApproxFields(cls):
        class Config:
            alias_required = False

        __ignore_not_set__ = ignore_not_set
        __annotations__ = {
            k: Union[ApproxValue, f.type_]
            if not isinstance(f.type_, type) or not issubclass(f.type_, BaseModel)
            else make_approx_type(f.type_)
            for k, f in cls.__fields__.items()
        }
        locals().update({k: f.default for k, f in cls.__fields__.items()})

        def __eq__(self, other):
            if ignore_not_set:
                d = {k: v for k, v in self.dict().items() if v is not None}
                d2 = {k: v for k, v in other.dict().items() if k in d}
                return d == d2
            return super().__eq__(other)

    if issubclass(cls, PolymorphicModel):
        ApproxFields.__fields__["type"].default = cls.__fields__["type"].default

    ApproxFields.__name__ = f"Approx{cls.__name__}"
    return ApproxFields
