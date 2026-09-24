"""
Metric dependency graph for analyzing metric execution order and parallelization.

This module builds a directed acyclic graph (DAG) of metric dependencies,
enabling identification of independent metrics that can run in parallel.
"""

from typing import Any
from typing import Dict
from typing import List
from typing import Set


class MetricDependencyGraph:
    """
    Represents dependencies between metrics for parallel execution planning.

    Key concepts:
    - Some metrics depend on others (e.g., DriftedColumnsCount depends on ValueDrift)
    - Independent metrics can run in parallel
    - This class resolves execution order and parallelization groups
    """

    def __init__(self) -> None:
        """Initialize an empty dependency graph."""
        self.nodes: Dict[str, Any] = {}  # {metric_id: metric_object}
        self.edges: Dict[str, Set[str]] = {}  # {metric_id: set of dependent metric_ids}
        self.reverse_edges: Dict[str, Set[str]] = {}  # {metric_id: set of metrics that depend on it}

    def add_metric(self, metric_id: str, metric: Any) -> None:
        """
        Add a metric node to the graph.

        Args:
            metric_id: Unique identifier for the metric
            metric: The metric object
        """
        self.nodes[metric_id] = metric
        if metric_id not in self.edges:
            self.edges[metric_id] = set()
        if metric_id not in self.reverse_edges:
            self.reverse_edges[metric_id] = set()

    def add_dependency(self, metric_id: str, depends_on: str) -> None:
        """
        Add a dependency: metric_id depends on depends_on.

        Args:
            metric_id: The metric that depends on another
            depends_on: The metric that must run first
        """
        if metric_id not in self.edges:
            self.edges[metric_id] = set()
        if depends_on not in self.reverse_edges:
            self.reverse_edges[depends_on] = set()

        self.edges[metric_id].add(depends_on)
        self.reverse_edges[depends_on].add(metric_id)

    def get_execution_order(self) -> List[List[str]]:
        """
        Compute execution order respecting dependencies.

        Returns a list of lists, where each inner list represents metrics that
        can run in parallel (same level). Levels are ordered such that all
        dependencies are satisfied before a metric's level.

        Returns:
            List[List[str]]: Execution levels. Each level contains metrics that
                           can run in parallel.

        Raises:
            ValueError: If a circular dependency is detected
        """
        # Check for cycles
        if self._has_cycle():
            raise ValueError("Circular dependency detected in metric graph")

        # Topological sort with level tracking
        visited: Set[str] = set()
        levels: List[List[str]] = []
        in_degree: Dict[str, int] = {}

        # Count in-degrees
        for metric_id in self.nodes:
            in_degree[metric_id] = len(self.edges[metric_id])

        # BFS-based topological sort with levels
        current_level: List[str] = []
        for metric_id in self.nodes:
            if in_degree[metric_id] == 0:
                current_level.append(metric_id)

        while current_level:
            levels.append(current_level)
            next_level: List[str] = []

            for metric_id in current_level:
                visited.add(metric_id)
                # Process dependents
                for dependent in self.reverse_edges[metric_id]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_level.append(dependent)

            current_level = next_level

        if len(visited) != len(self.nodes):
            raise ValueError("Circular dependency detected or unreachable metrics")

        return levels

    def get_independent_metrics(self) -> Set[str]:
        """
        Get metrics with no dependencies (can run first).

        Returns:
            Set of metric IDs with no dependencies
        """
        independent = set()
        for metric_id, deps in self.edges.items():
            if not deps:
                independent.add(metric_id)
        return independent

    def get_dependents(self, metric_id: str) -> Set[str]:
        """
        Get all metrics that depend (directly or transitively) on a metric.

        Args:
            metric_id: The metric ID

        Returns:
            Set of dependent metric IDs
        """
        dependents: Set[str] = set()
        to_process: List[str] = [metric_id]

        while to_process:
            current = to_process.pop(0)
            for dependent in self.reverse_edges.get(current, set()):
                if dependent not in dependents:
                    dependents.add(dependent)
                    to_process.append(dependent)

        return dependents

    def get_dependencies(self, metric_id: str) -> Set[str]:
        """
        Get all dependencies (direct and transitive) for a metric.

        Args:
            metric_id: The metric ID

        Returns:
            Set of dependency metric IDs
        """
        dependencies: Set[str] = set()
        to_process: List[str] = [metric_id]

        while to_process:
            current = to_process.pop(0)
            for dep in self.edges.get(current, set()):
                if dep not in dependencies:
                    dependencies.add(dep)
                    to_process.append(dep)

        return dependencies

    def is_independent_from(self, metric_id1: str, metric_id2: str) -> bool:
        """
        Check if two metrics are independent (can run in parallel).

        Args:
            metric_id1: First metric
            metric_id2: Second metric

        Returns:
            True if metrics can run in parallel
        """
        deps1 = self.get_dependencies(metric_id1)
        deps2 = self.get_dependencies(metric_id2)

        # Independent if neither depends on the other
        return (metric_id2 not in deps1) and (metric_id1 not in deps2)

    def _has_cycle(self) -> bool:
        """
        Detect if the graph has a cycle using DFS.

        Returns:
            True if cycle exists
        """
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.edges.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def summary(self) -> Dict[str, Any]:
        """
        Get a summary of the graph.

        Returns:
            Dictionary with graph statistics
        """
        try:
            levels = self.get_execution_order()
            max_parallelism = max(len(level) for level in levels) if levels else 0
        except ValueError:
            levels = []
            max_parallelism = 0

        return {
            "num_metrics": len(self.nodes),
            "num_dependencies": sum(len(deps) for deps in self.edges.values()),
            "independent_metrics": len(self.get_independent_metrics()),
            "execution_levels": len(levels),
            "max_parallelism": max_parallelism,
            "has_cycle": self._has_cycle(),
        }

    def __repr__(self) -> str:
        """String representation of the graph."""
        summary = self.summary()
        return (
            f"MetricDependencyGraph("
            f"metrics={summary['num_metrics']}, "
            f"deps={summary['num_dependencies']}, "
            f"levels={summary['execution_levels']}, "
            f"max_parallel={summary['max_parallelism']})"
        )
