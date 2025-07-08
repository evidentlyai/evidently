from evidently.errors import EvidentlyError


class OptimizationError(EvidentlyError):
    """Custom exception for optimization errors."""

    pass


class OptimizationRuntimeError(OptimizationError):
    """Custom exception for optimization runtime errors."""


class OptimizationConfigurationError(OptimizationRuntimeError):
    """Custom exception for optimization configuration errors."""
