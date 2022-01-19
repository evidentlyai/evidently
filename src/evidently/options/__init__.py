from typing import TypeVar, Generic, Type, Dict, Any

from .data_drift import DataDriftOptions
from .quality_metrics import QualityMetricsOptions

TypeParam = TypeVar('TypeParam')


class OptionsProvider(Generic[TypeParam]):
    _options: Dict[Type, Any]

    def __init__(self):
        self._options = {}

    def add(self, options):
        self._options[type(options)] = options

    def get(self, options_type: Type[TypeParam]) -> TypeParam:
        return self._options.get(options_type, options_type())
