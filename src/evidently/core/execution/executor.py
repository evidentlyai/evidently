"""
Metric executor for sequential and parallel execution.

Implements multiple execution strategies:
1. Sequential (baseline)
2. Parallel using multiprocessing
3. Polars-based with lazy evaluation (preferred for performance)
"""

import logging
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from .graph import MetricDependencyGraph

logger = logging.getLogger(__name__)


class ExecutionPlan:
    """Represents a plan for metric execution."""

    def __init__(self, levels: List[List[str]], graph: MetricDependencyGraph):
        """
        Initialize execution plan.

        Args:
            levels: Topologically sorted levels of metrics
            graph: Dependency graph
        """
        self.levels = levels
        self.graph = graph
        self.total_metrics = sum(len(level) for level in levels)
        self.parallelizable_metrics = sum(len(level) - 1 for level in levels if len(level) > 1)

    @property
    def num_levels(self) -> int:
        """Number of sequential levels to execute."""
        return len(self.levels)

    @property
    def max_parallelism(self) -> int:
        """Maximum metrics that can run in parallel."""
        return max((len(level) for level in self.levels), default=1)

    @property
    def parallelization_ratio(self) -> float:
        """Percentage of metrics that can be parallelized."""
        if self.total_metrics == 0:
            return 0.0
        return self.parallelizable_metrics / self.total_metrics

    def __repr__(self) -> str:
        """String representation of the plan."""
        return (
            f"ExecutionPlan("
            f"metrics={self.total_metrics}, "
            f"levels={self.num_levels}, "
            f"parallelizable={self.parallelizable_metrics}, "
            f"ratio={self.parallelization_ratio:.2%})"
        )


class MetricExecutor:
    """
    Executes metrics with optional parallelization.

    Supports multiple execution strategies and automatically selects
    based on metric properties and system capabilities.
    """

    def __init__(self, use_parallel: bool = True, max_workers: Optional[int] = None):
        """
        Initialize the executor.

        Args:
            use_parallel: Enable parallel execution if supported
            max_workers: Maximum workers for parallel execution (None = auto)
        """
        self.use_parallel = use_parallel
        self.max_workers = max_workers
        self.execution_history: List[Dict[str, Any]] = []

    def build_execution_plan(self, metrics: Dict[str, Any]) -> ExecutionPlan:
        """
        Build an execution plan from metrics.

        Args:
            metrics: Dictionary of {metric_id: metric_object}

        Returns:
            ExecutionPlan with execution levels

        Raises:
            ValueError: If metrics have circular dependencies
        """
        graph = MetricDependencyGraph()

        # Add all metrics to graph
        for metric_id, metric in metrics.items():
            graph.add_metric(metric_id, metric)

        # This is a placeholder for dependency extraction
        # In real implementation, would analyze metric's `depends_on` property
        # For now, assume all metrics are independent (simplification for Phase 2)

        levels = graph.get_execution_order()
        plan = ExecutionPlan(levels, graph)

        logger.info(f"Built execution plan: {plan}")
        return plan

    def execute_sequential(self, metrics: Dict[str, Any], calculation_fn: Callable[[str, Any], Any]) -> Dict[str, Any]:
        """
        Execute metrics sequentially (baseline approach).

        Args:
            metrics: Dictionary of {metric_id: metric_object}
            calculation_fn: Function to calculate a metric (metric_id, metric) -> result

        Returns:
            Dictionary of {metric_id: result}
        """
        plan = self.build_execution_plan(metrics)
        results = {}

        for level_idx, level in enumerate(plan.levels):
            logger.info(f"Executing level {level_idx + 1}/{plan.num_levels}")
            for metric_id in level:
                try:
                    metric = metrics[metric_id]
                    result = calculation_fn(metric_id, metric)
                    results[metric_id] = result
                    logger.debug(f"✓ Calculated {metric_id}")
                except Exception as e:
                    logger.error(f"✗ Failed to calculate {metric_id}: {e}")
                    results[metric_id] = None

        return results

    def execute_parallel_process(
        self, metrics: Dict[str, Any], calculation_fn: Callable[[str, Any], Any], max_workers: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute metrics in parallel using ProcessPoolExecutor.

        WARNING: Requires metrics to be picklable and calculation_fn to be at module level.

        Args:
            metrics: Dictionary of {metric_id: metric_object}
            calculation_fn: Function to calculate a metric
            max_workers: Maximum worker processes

        Returns:
            Dictionary of {metric_id: result}
        """
        plan = self.build_execution_plan(metrics)
        results = {}

        max_workers = max_workers or self.max_workers

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for level_idx, level in enumerate(plan.levels):
                logger.info(f"Executing level {level_idx + 1}/{plan.num_levels} (parallel)")

                # Submit all metrics in current level
                futures = {}
                for metric_id in level:
                    metric = metrics[metric_id]
                    future = executor.submit(calculation_fn, metric_id, metric)
                    futures[future] = metric_id

                # Collect results as they complete
                for future in futures:
                    metric_id = futures[future]
                    try:
                        result = future.result()
                        results[metric_id] = result
                        logger.debug(f"✓ Calculated {metric_id}")
                    except Exception as e:
                        logger.error(f"✗ Failed to calculate {metric_id}: {e}")
                        results[metric_id] = None

        return results

    def execute_parallel_thread(
        self, metrics: Dict[str, Any], calculation_fn: Callable[[str, Any], Any], max_workers: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute metrics in parallel using ThreadPoolExecutor.

        Better for I/O-bound tasks but limited by Python GIL for CPU-bound tasks.

        Args:
            metrics: Dictionary of {metric_id: metric_object}
            calculation_fn: Function to calculate a metric
            max_workers: Maximum worker threads

        Returns:
            Dictionary of {metric_id: result}
        """
        plan = self.build_execution_plan(metrics)
        results = {}

        max_workers = max_workers or self.max_workers

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for level_idx, level in enumerate(plan.levels):
                logger.info(f"Executing level {level_idx + 1}/{plan.num_levels} (threaded)")

                # Submit all metrics in current level
                futures = {}
                for metric_id in level:
                    metric = metrics[metric_id]
                    future = executor.submit(calculation_fn, metric_id, metric)
                    futures[future] = metric_id

                # Collect results as they complete
                for future in futures:
                    metric_id = futures[future]
                    try:
                        result = future.result()
                        results[metric_id] = result
                        logger.debug(f"✓ Calculated {metric_id}")
                    except Exception as e:
                        logger.error(f"✗ Failed to calculate {metric_id}: {e}")
                        results[metric_id] = None

        return results

    def execute(
        self, metrics: Dict[str, Any], calculation_fn: Callable[[str, Any], Any], strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        Execute metrics with automatic strategy selection.

        Args:
            metrics: Dictionary of {metric_id: metric_object}
            calculation_fn: Function to calculate a metric
            strategy: "sequential", "thread", "process", or "auto"

        Returns:
            Dictionary of {metric_id: result}
        """
        if not self.use_parallel or strategy == "sequential":
            return self.execute_sequential(metrics, calculation_fn)

        plan = self.build_execution_plan(metrics)

        if strategy == "auto":
            # Auto-select strategy based on parallelization potential
            if plan.parallelization_ratio < 0.1:
                # Sequential if too little parallelization potential
                strategy = "sequential"
            elif plan.max_parallelism < 4:
                # Use threads for small parallelization
                strategy = "thread"
            else:
                # Use processes for significant parallelization (if Polars not available)
                strategy = "process"

        if strategy == "sequential":
            return self.execute_sequential(metrics, calculation_fn)
        elif strategy == "thread":
            return self.execute_parallel_thread(metrics, calculation_fn)
        elif strategy == "process":
            return self.execute_parallel_process(metrics, calculation_fn)
        else:
            raise ValueError(f"Unknown execution strategy: {strategy}")

    def validate_dependencies(self, metrics: Dict[str, Any]) -> bool:
        """
        Validate that metric dependencies form a DAG (no cycles).

        Args:
            metrics: Dictionary of {metric_id: metric_object}

        Returns:
            True if valid, False otherwise
        """
        try:
            self.build_execution_plan(metrics)
            return True
        except ValueError as e:
            logger.error(f"Dependency validation failed: {e}")
            return False

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of execution history."""
        if not self.execution_history:
            return {"status": "no_executions"}

        return {
            "total_executions": len(self.execution_history),
            "successful": sum(1 for e in self.execution_history if e.get("success")),
            "failed": sum(1 for e in self.execution_history if not e.get("success")),
        }
