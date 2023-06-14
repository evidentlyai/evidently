import glob
import os
from importlib import import_module
from inspect import isabstract
from typing import Type

import evidently


class TestOutcome:
    pass


class Error(TestOutcome):
    def __init__(self, exception_type: Type[Exception]):
        self.exception_type = exception_type


def find_all_subclasses(
    base: Type,
    base_module: str = "evidently",
    path: str = os.path.dirname(evidently.__file__),
    include_abstract: bool = False,
):
    classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = f"{base_module}." + mod_path.replace("/", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not base and issubclass(value, base):
                if not isabstract(value) or include_abstract:
                    classes.add(value)

    return classes
