import json
from inspect import isabstract
from typing import List

import pytest

from evidently._pydantic_compat import import_string
from evidently._pydantic_compat import parse_obj_as
from evidently.core.container import MetricContainer
from evidently.generators import ColumnMetricGenerator
from evidently.metrics import MinValue
from evidently.metrics.group_by import GroupBy
from evidently.presets import ClassificationDummyQuality
from evidently.presets import ClassificationPreset
from evidently.presets import ClassificationQuality
from evidently.presets import ClassificationQualityByLabel
from evidently.presets import DataDriftPreset
from evidently.presets import DatasetStats
from evidently.presets import DataSummaryPreset
from evidently.presets import RegressionDummyQuality
from evidently.presets import RegressionPreset
from evidently.presets import RegressionQuality
from evidently.presets import TextEvals
from evidently.pydantic_utils import TYPE_ALIASES


def load_all_preset_types():
    classpaths = [
        cp for (base, _), cp in TYPE_ALIASES.items() if isinstance(base, type) and issubclass(base, MetricContainer)
    ]
    for cp in classpaths:
        try:
            import_string(cp)
        except ImportError as e:
            raise ImportError(f"Cannot import preset type {cp}") from e


load_all_preset_types()

all_presets: List[MetricContainer] = [
    ClassificationPreset(),
    ClassificationQuality(),
    DatasetStats(),
    DataSummaryPreset(),
    RegressionDummyQuality(),
    ColumnMetricGenerator(metric_type=MinValue),
    ClassificationDummyQuality(),
    RegressionQuality(),
    DataDriftPreset(),
    TextEvals(),
    ClassificationQualityByLabel(),
    RegressionPreset(),
    GroupBy(metric=MinValue(column="a"), column_name="b"),
]


def test_all_presets_tested():
    tested_types_set = {type(p) for p in all_presets}
    all_preset_types = set(s for s in MetricContainer.__subclasses__() if not isabstract(s))
    assert tested_types_set == all_preset_types, "Missing tests for presets " + ", ".join(
        f"{t.__name__}()" for t in all_preset_types - tested_types_set
    )


@pytest.mark.parametrize("preset", all_presets, ids=lambda p: p.__class__.__name__)
def test_all_presets_json_serialization(preset):
    payload = json.loads(preset.json())
    preset2 = parse_obj_as(MetricContainer, payload)
    assert preset2 == preset
