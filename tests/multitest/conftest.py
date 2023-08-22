import abc
import glob
import json
import os
from importlib import import_module
from inspect import isabstract
from typing import Any
from typing import Callable
from typing import Dict
from typing import Type

import evidently
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.report import Report
from tests.conftest import smart_assert_equal


class TestOutcome:
    @abc.abstractmethod
    def check(self, report: Report):
        raise NotImplementedError


class Error(TestOutcome):
    def __init__(self, exception_type: Type[Exception]):
        self.exception_type = exception_type

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
    def __init__(self, metric: Metric, result: MetricResult):
        self.metric = metric
        self.result = result

    def check(self, report: Report):
        result = report._inner_suite.context.metric_results[self.metric]
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
