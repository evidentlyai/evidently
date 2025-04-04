from .core import registries as future_registry
from .legacy import _registry as legacy_registry

__all__ = ["future_registry", "legacy_registry"]
