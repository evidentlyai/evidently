import glob
import os
from importlib import import_module
from inspect import isabstract
from typing import Set
from typing import Type
from typing import TypeVar

import pytest

import evidently
from evidently._pydantic_compat import import_string
from evidently.base_metric import BasePreset
from evidently.base_metric import ColumnName
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.collector.config import CollectorTrigger
from evidently.collector.storage import CollectorStorage
from evidently.experimental.dataset_generators.base import BaseDatasetGenerator
from evidently.experimental.dataset_generators.llm.index import DataCollectionProvider
from evidently.experimental.dataset_generators.llm.splitter import Splitter
from evidently.features.generated_features import BaseDescriptor
from evidently.features.generated_features import GeneratedFeatures
from evidently.features.llm_judge import BaseLLMPromptTemplate
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.pydantic_utils import TYPE_ALIASES
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import WithTestAndMetricDependencies
from evidently.pydantic_utils import get_base_class
from evidently.pydantic_utils import is_not_abstract
from evidently.test_preset.test_preset import TestPreset
from evidently.tests.base_test import Test
from evidently.tests.base_test import TestParameters
from evidently.ui.components.base import Component
from evidently.ui.dashboards.base import DashboardPanel
from evidently.utils.llm.prompts import PromptBlock
from evidently.utils.llm.prompts import PromptTemplate

T = TypeVar("T")


# todo: deduplicate code
def find_all_subclasses(
    base: Type[T],
    base_module: str = "evidently",
    path: str = os.path.dirname(evidently.__file__),
    include_abstract: bool = False,
) -> Set[Type[T]]:
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


def test_all_aliases_registered():
    not_registered = []

    for cls in find_all_subclasses(PolymorphicModel, include_abstract=True):
        if cls.__is_base_type__():
            continue
        classpath = cls.__get_classpath__()
        typename = cls.__get_type__()
        if classpath == typename:
            # no typename
            continue
        key = (get_base_class(cls), typename)
        if key not in TYPE_ALIASES or TYPE_ALIASES[key] != classpath:
            not_registered.append(cls)

    msg = "\n".join(
        f'register_type_alias({get_base_class(cls).__name__}, "{cls.__get_classpath__()}", "{cls.__get_type__()}")'
        for cls in sorted(not_registered, key=lambda c: get_base_class(c).__name__ + " " + c.__get_classpath__())
    )
    print(msg)
    assert len(not_registered) == 0, "Not all aliases registered"


@pytest.mark.parametrize("classpath", list(TYPE_ALIASES.values()))
def test_all_registered_classpath_exist(classpath):
    try:
        import_string(classpath)
    except ImportError:
        assert False, f"wrong classpath registered '{classpath}'"


def test_all_aliases_correct():
    base_class_type_mapping = {
        Metric: "metric",
        Test: "test",
        GeneratedFeatures: "feature",
        BaseDescriptor: "descriptor",
        MetricPreset: "metric_preset",
        TestPreset: "test_preset",
        MetricResult: "metric_result",
        DriftMethod: "drift_method",
        TestParameters: "test_parameters",
        ColumnName: "base",
        CollectorTrigger: "collector_trigger",
        CollectorStorage: "collector_storage",
        BaseLLMPromptTemplate: "prompt_template",
        DashboardPanel: "dashboard_panel",
        BaseDatasetGenerator: "dataset_generator",
        Splitter: "splitter",
        DataCollectionProvider: "data_collecton_provider",
        PromptBlock: "prompt_block",
        PromptTemplate: "prompt_template",
    }
    skip = [Component]
    skip_literal = [EvidentlyBaseModel, WithTestAndMetricDependencies, BasePreset]
    for cls in find_all_subclasses(PolymorphicModel, include_abstract=True):
        if cls in skip_literal or any(issubclass(cls, s) for s in skip) or not is_not_abstract(cls):
            continue
        for base_class, base_type in base_class_type_mapping.items():
            if issubclass(cls, base_class):
                alias = getattr(cls.__config__, "type_alias")
                assert alias is not None, f"{cls.__name__} has no alias ({alias})"
                assert alias == f"evidently:{base_type}:{cls.__name__}", f"wrong alias for {cls.__name__}"
                break
        else:
            assert False, f"No base class type mapping for {cls}"
