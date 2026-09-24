"""
Benchmark suite for measuring metric and test execution performance.

This module provides baseline measurements for optimization work on Issue #1034.
Tracks: execution time, memory usage, CPU utilization across various dataset sizes.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
import psutil
import pytest

from evidently import BinaryClassification
from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.metrics import DriftedColumnsCount
from evidently.metrics import ValueDrift
from evidently.presets import ClassificationPreset
from evidently.presets import DataDriftPreset


class BenchmarkResult:
    """Stores and exports benchmark measurements."""

    def __init__(self, test_name: str, dataset_size: int, num_metrics: int):
        self.test_name = test_name
        self.dataset_size = dataset_size
        self.num_metrics = num_metrics
        self.start_time = None
        self.end_time = None
        self.execution_time_seconds = None
        self.peak_memory_mb = None
        self.avg_memory_mb = None
        self.initial_memory_mb = None
        self.timestamp = datetime.now().isoformat()

    def record_execution(self) -> None:
        """Record execution time."""
        if self.start_time and self.end_time:
            self.execution_time_seconds = self.end_time - self.start_time

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "test_name": self.test_name,
            "dataset_size": self.dataset_size,
            "num_metrics": self.num_metrics,
            "execution_time_seconds": self.execution_time_seconds,
            "peak_memory_mb": self.peak_memory_mb,
            "avg_memory_mb": self.avg_memory_mb,
            "initial_memory_mb": self.initial_memory_mb,
            "timestamp": self.timestamp,
        }

    def metrics_per_second(self) -> Optional[float]:
        """Calculate metrics calculated per second."""
        if self.num_metrics > 0 and self.execution_time_seconds:
            return self.num_metrics / self.execution_time_seconds
        return None

    def __repr__(self) -> str:
        return (
            f"BenchmarkResult("
            f"test={self.test_name}, "
            f"size={self.dataset_size}, "
            f"metrics={self.num_metrics}, "
            f"time={self.execution_time_seconds:.2f}s, "
            f"memory={self.peak_memory_mb:.1f}MB, "
            f"metrics/sec={self.metrics_per_second():.2f})"
        )


class BenchmarkSuite:
    """Manages benchmark execution and result collection."""

    BASELINE_DIR = Path(__file__).parent / "baselines"

    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.BASELINE_DIR.mkdir(exist_ok=True)

    def save_baseline(self, results: List[BenchmarkResult], filename: str = "baseline.json") -> Path:
        """Save benchmark results as baseline for future comparisons."""
        output_file = self.BASELINE_DIR / filename
        with open(output_file, "w") as f:
            json.dump([r.to_dict() for r in results], f, indent=2)
        return output_file

    def load_baseline(self, filename: str = "baseline.json") -> Optional[List[BenchmarkResult]]:
        """Load baseline results for comparison."""
        baseline_file = self.BASELINE_DIR / filename
        if not baseline_file.exists():
            return None
        with open(baseline_file, "r") as f:
            data = json.load(f)
        results = []
        for entry in data:
            result = BenchmarkResult(entry["test_name"], entry["dataset_size"], entry["num_metrics"])
            result.execution_time_seconds = entry["execution_time_seconds"]
            result.peak_memory_mb = entry["peak_memory_mb"]
            result.avg_memory_mb = entry["avg_memory_mb"]
            result.initial_memory_mb = entry["initial_memory_mb"]
            results.append(result)
        return results

    def compare_with_baseline(self, current: List[BenchmarkResult], baseline: Optional[List[BenchmarkResult]]) -> Dict:
        """Compare current results with baseline, report performance change."""
        if not baseline:
            return {"status": "no_baseline", "message": "No baseline available for comparison"}

        comparison = {"status": "compared", "results": []}
        for current_result in current:
            matching_baseline = next(
                (
                    b
                    for b in baseline
                    if b.test_name == current_result.test_name and b.dataset_size == current_result.dataset_size
                ),
                None,
            )
            if matching_baseline:
                baseline_time = matching_baseline.execution_time_seconds
                current_time = current_result.execution_time_seconds
                time_change = (current_time - baseline_time) / baseline_time * 100
                baseline_mem = matching_baseline.peak_memory_mb
                current_mem = current_result.peak_memory_mb
                memory_change = (current_mem - baseline_mem) / baseline_mem * 100
                comparison["results"].append(
                    {
                        "test": current_result.test_name,
                        "size": current_result.dataset_size,
                        "time_change_percent": round(time_change, 2),
                        "memory_change_percent": round(memory_change, 2),
                        "baseline_time": matching_baseline.execution_time_seconds,
                        "current_time": current_result.execution_time_seconds,
                    }
                )
        return comparison


def create_synthetic_classification_data(
    n_rows: int = 1000, n_features: int = 20, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Create synthetic classification dataset with reference and current data."""
    np.random.seed(random_state)

    # Reference data
    X_ref = np.random.randn(n_rows, n_features)
    y_ref = np.random.choice([0, 1], size=n_rows, p=[0.6, 0.4])
    proba_ref = np.random.rand(n_rows)

    ref_df = pd.DataFrame(X_ref, columns=[f"feature_{i}" for i in range(n_features)])
    ref_df["target"] = y_ref
    ref_df["predictions"] = (proba_ref > 0.5).astype(int)
    ref_df["pred_proba"] = proba_ref
    ref_df = Dataset.from_pandas(
        ref_df,
        data_definition=DataDefinition(
            classification=[BinaryClassification(target="target", prediction_labels="predictions")],
            categorical_columns=["target", "predictions"],
        ),
    )

    # Current data (slight distribution shift)
    X_current = np.random.randn(n_rows, n_features) + 0.1
    y_current = np.random.choice([0, 1], size=n_rows, p=[0.55, 0.45])
    proba_current = np.random.rand(n_rows)

    current_df = pd.DataFrame(X_current, columns=[f"feature_{i}" for i in range(n_features)])
    current_df["target"] = y_current
    current_df["predictions"] = (proba_current > 0.5).astype(int)
    current_df["pred_proba"] = proba_current
    current_df = Dataset.from_pandas(
        current_df,
        data_definition=DataDefinition(
            classification=[BinaryClassification(target="target", prediction_labels="predictions")],
            categorical_columns=["target", "predictions"],
        ),
    )

    return ref_df, current_df


def create_synthetic_drift_data(
    n_rows: int = 1000, n_features: int = 20, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Create synthetic data for drift detection testing."""
    np.random.seed(random_state)

    # Reference data
    ref_df = pd.DataFrame(np.random.randn(n_rows, n_features), columns=[f"feature_{i}" for i in range(n_features)])

    # Current data (with introduced drift)
    current_df = pd.DataFrame(
        np.random.randn(n_rows, n_features) + 0.5,  # Shift in distribution
        columns=[f"feature_{i}" for i in range(n_features)],
    )

    return ref_df, current_df


def measure_memory(func, *args, **kwargs) -> Tuple[Any, float, float]:
    """
    Execute function and measure memory usage.
    Returns: (result, peak_memory_mb, avg_memory_mb)
    """
    process = psutil.Process(os.getpid())

    # Get initial memory
    process.memory_info()

    # Measure during execution
    start_memory = process.memory_info().rss / 1024 / 1024

    result = func(*args, **kwargs)

    end_memory = process.memory_info().rss / 1024 / 1024
    peak_memory = max(start_memory, end_memory)
    avg_memory = (start_memory + end_memory) / 2

    return result, peak_memory, avg_memory


# ==================== CLASSIFICATION BENCHMARKS ====================


@pytest.mark.benchmark
@pytest.mark.slow
class TestClassificationBenchmarks:
    """Benchmarks for classification metrics."""

    @pytest.fixture
    def suite(self):
        return BenchmarkSuite()

    def test_classify_small_dataset(self, suite):
        """Benchmark ClassificationPreset with 1k rows, 20 features."""
        ref_df, current_df = create_synthetic_classification_data(n_rows=1_000, n_features=20)

        result = BenchmarkResult("classify_small", dataset_size=1_000, num_metrics=7)
        preset = ClassificationPreset()

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")

    def test_classify_medium_dataset(self, suite):
        """Benchmark ClassificationPreset with 10k rows."""
        ref_df, current_df = create_synthetic_classification_data(n_rows=10_000, n_features=20)

        result = BenchmarkResult("classify_medium", dataset_size=10_000, num_metrics=7)
        preset = ClassificationPreset()

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")

    def test_classify_large_dataset(self, suite):
        """Benchmark ClassificationPreset with 100k rows."""
        ref_df, current_df = create_synthetic_classification_data(n_rows=100_000, n_features=20)

        result = BenchmarkResult("classify_large", dataset_size=100_000, num_metrics=7)
        preset = ClassificationPreset()

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")


# ==================== DRIFT DETECTION BENCHMARKS ====================


@pytest.mark.benchmark
@pytest.mark.slow
class TestDriftBenchmarks:
    """Benchmarks for drift detection metrics."""

    @pytest.fixture
    def suite(self):
        return BenchmarkSuite()

    def test_drift_small_dataset(self, suite):
        """Benchmark DataDriftPreset with 1k rows, 20 features."""
        ref_df, current_df = create_synthetic_drift_data(n_rows=1_000, n_features=20)

        result = BenchmarkResult("drift_small", dataset_size=1_000, num_metrics=21)  # 1 + 20
        preset = DataDriftPreset(include_tests=False)

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")

    def test_drift_medium_dataset(self, suite):
        """Benchmark DataDriftPreset with 10k rows."""
        ref_df, current_df = create_synthetic_drift_data(n_rows=10_000, n_features=20)

        result = BenchmarkResult("drift_medium", dataset_size=10_000, num_metrics=21)
        preset = DataDriftPreset(include_tests=False)

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")

    def test_drift_large_dataset(self, suite):
        """Benchmark DataDriftPreset with 100k rows."""
        ref_df, current_df = create_synthetic_drift_data(n_rows=100_000, n_features=20)

        result = BenchmarkResult("drift_large", dataset_size=100_000, num_metrics=21)
        preset = DataDriftPreset(include_tests=False)

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report([preset])
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")


# ==================== MULTI-METRIC SCALING BENCHMARKS ====================


@pytest.mark.benchmark
@pytest.mark.slow
class TestMultiMetricScaling:
    """Benchmarks to measure performance as number of metrics increases."""

    @pytest.fixture
    def suite(self):
        return BenchmarkSuite()

    def test_100_metrics_small_data(self, suite):
        """Benchmark with 100 metrics on 1k rows."""
        ref_df, current_df = create_synthetic_drift_data(n_rows=1_000, n_features=10)

        # Create many duplicate metrics to simulate real load
        metrics = [ValueDrift(column=f"feature_{i % 10}") for i in range(100)]
        metrics.append(DriftedColumnsCount(columns=[f"feature_{i}" for i in range(10)]))

        result = BenchmarkResult("metrics_100_small", dataset_size=1_000, num_metrics=101)

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report(metrics)
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")

    def test_500_metrics_medium_data(self, suite):
        """Benchmark with 500 metrics on 10k rows."""
        ref_df, current_df = create_synthetic_drift_data(n_rows=10_000, n_features=10)

        metrics = [ValueDrift(column=f"feature_{i % 10}") for i in range(500)]
        metrics.append(DriftedColumnsCount(columns=[f"feature_{i}" for i in range(10)]))

        result = BenchmarkResult("metrics_500_medium", dataset_size=10_000, num_metrics=501)

        result.initial_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.start_time = time.perf_counter()

        report = Report(metrics)
        snapshot = report.run(current_df, ref_df)

        result.end_time = time.perf_counter()
        result.peak_memory_mb = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        result.record_execution()

        suite.results.append(result)
        assert len(snapshot.metric_results) > 0
        print(f"\n{result}")


@pytest.fixture(scope="session", autouse=True)
def save_benchmark_results():
    """Fixture to save benchmark results after test run."""
    yield
    # This will be enhanced in Phase 1 to actually save results
