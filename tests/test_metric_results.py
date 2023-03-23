import glob
import os
from importlib import import_module
from typing import Set
from typing import Type

import pytest

import evidently
from evidently.base_metric import MetricResultField


@pytest.fixture
def all_metric_results():
    path = os.path.dirname(evidently.__file__)

    metric_result_field_classes = set()
    for mod in glob.glob(path + "/**/*.py", recursive=True):
        mod_path = os.path.relpath(mod, path)[:-3]
        mod_name = "evidently." + mod_path.replace("/", ".")
        if mod_name.endswith("__"):
            continue
        module = import_module(mod_name)
        for key, value in module.__dict__.items():
            if isinstance(value, type) and value is not MetricResultField and issubclass(value, MetricResultField):
                metric_result_field_classes.add(value)
    return metric_result_field_classes


def test_metric_result_fields_config(all_metric_results: Set[Type[MetricResultField]]):
    errors = []
    for cls in all_metric_results:
        field_names = set(cls.__fields__)
        for config_field in {
            "pd_name_mapping",
            "dict_include_fields",
            "dict_exclude_fields",
            "pd_include_fields",
            "pd_exclude_fields",
        }:
            field_value = getattr(cls.__config__, config_field)
            if field_value is None:
                continue
            for field_name in field_value:
                if field_name not in field_names:
                    errors.append((cls, config_field, field_name))

    assert len(errors) == 0, f"Wrong config for field classes: {errors}"
