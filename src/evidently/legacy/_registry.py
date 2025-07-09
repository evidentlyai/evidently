from .descriptors import _registry as descriptors_registry
from .features import _registry as features_registry
from .metric_preset import _registry as metric_preset_registry
from .metrics import _registry as metrics_registry
from .test_preset import _registry as test_preset_registry
from .tests import _registry as tests_registry

__all__ = [
    "tests_registry",
    "metrics_registry",
    "descriptors_registry",
    "features_registry",
    "metric_preset_registry",
    "test_preset_registry",
]
