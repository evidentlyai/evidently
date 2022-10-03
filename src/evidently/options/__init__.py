from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from .color_scheme import BERLIN_AUTUMN_COLOR_OPTIONS
from .color_scheme import KARACHI_SUNRISE_COLOR_OPTIONS
from .color_scheme import NIGHTOWL_COLOR_OPTIONS
from .color_scheme import SOLARIZED_COLOR_OPTIONS
from .color_scheme import ColorOptions
from .data_drift import DataDriftOptions
from .quality_metrics import QualityMetricsOptions

TypeParam = TypeVar("TypeParam")


class OptionsProvider:
    _options: Dict[Type, Any]

    def __init__(self):
        self._options = {}

    def add(self, options):
        self._options[type(options)] = options

    def get(self, options_type: Type[TypeParam]) -> TypeParam:
        return self._options.get(options_type, options_type())
