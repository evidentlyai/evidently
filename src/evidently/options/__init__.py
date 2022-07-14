from typing import TypeVar, Generic, Type, Dict, Any

from .color_scheme import (
    ColorOptions,
    KARACHI_SUNRISE_COLOR_OPTIONS,
    SOLARIZED_COLOR_OPTIONS,
    BERLIN_AUTUMN_COLOR_OPTIONS,
    NIGHTOWL_COLOR_OPTIONS,
)
from .data_drift import DataDriftOptions
from .quality_metrics import QualityMetricsOptions

TypeParam = TypeVar("TypeParam")


class OptionsProvider(Generic[TypeParam]):
    _options: Dict[Type, Any]

    def __init__(self):
        self._options = {}

    def add(self, options):
        self._options[type(options)] = options

    def get(self, options_type: Type[TypeParam]) -> TypeParam:
        return self._options.get(options_type, options_type())
