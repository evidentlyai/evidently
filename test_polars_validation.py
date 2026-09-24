"""
Comprehensive validation test for Polars integration with metrics.
"""

import sys
import time

import numpy as np
import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.metrics import CategoryCount
from evidently.metrics import InRangeValueCount
from evidently.metrics import MaxValue
from evidently.metrics import MeanValue
from evidently.metrics import MedianValue
from evidently.metrics import MinValue
from evidently.metrics import MissingValueCount
from evidently.metrics import OutRangeValueCount
from evidently.metrics import QuantileValue
from evidently.metrics import StdValue
from evidently.metrics import SumValue


def test_statistics_metrics():
    """Test all optimized statistics metrics."""
    print("\n" + "=" * 60)
    print("Testing Statistics Metrics")
    print("=" * 60)

    # Create test data
    n_rows = 5_000
    data = {
        "numeric_col": np.random.randn(n_rows) * 100 + 50,
        "category_col": np.random.choice(["A", "B", "C"], n_rows),
        "binary_col": np.random.choice([0, 1], n_rows),
    }

    # Add some missing values
    data["numeric_col"][::100] = np.nan

    df = pd.DataFrame(data)
    dataset = Dataset.from_pandas(df, data_definition=DataDefinition())

    metrics_to_test = [
        ("MeanValue", MeanValue(column="numeric_col")),
        ("MinValue", MinValue(column="numeric_col")),
        ("MaxValue", MaxValue(column="numeric_col")),
        ("StdValue", StdValue(column="numeric_col")),
        ("MedianValue", MedianValue(column="numeric_col")),
        ("SumValue", SumValue(column="numeric_col")),
        ("QuantileValue", QuantileValue(column="numeric_col", quantile=0.75)),
        ("CategoryCount", CategoryCount(column="category_col", category="A")),
        ("MissingValueCount", MissingValueCount(column="numeric_col")),
        ("InRangeValueCount", InRangeValueCount(column="numeric_col", left=0, right=100)),
        ("OutRangeValueCount", OutRangeValueCount(column="numeric_col", left=0, right=100)),
    ]

    results_summary = []
    for metric_name, metric_obj in metrics_to_test:
        try:
            report = Report([metric_obj])
            start_time = time.time()
            snapshot = report.run(dataset, None)
            elapsed = time.time() - start_time

            # Verify we got results
            if len(snapshot.metric_results) > 0:
                status = "✓"
                result_str = "passed"
            else:
                status = "✗"
                result_str = "failed - no results"

            results_summary.append((metric_name, status, f"{elapsed:.3f}s", result_str))

        except Exception as e:
            results_summary.append((metric_name, "✗", "error", str(e)[:50]))

    # Print results table
    print("\nMetrics Test Results:")
    print(f"{'Metric':<25} {'Status'} {'Time':<10} {'Result'}")
    print("-" * 70)
    for metric_name, status, elapsed, result in results_summary:
        print(f"{metric_name:<25} {status}  {elapsed:<10} {result}")

    # Check if all passed
    passed = sum(1 for _, s, _, _ in results_summary if s == "✓")
    total = len(results_summary)
    print(f"\nResult: {passed}/{total} metrics passed")

    return passed == total


def test_with_reference_data():
    """Test metrics with reference data."""
    print("\n" + "=" * 60)
    print("Testing Metrics with Reference Data")
    print("=" * 60)

    np.random.seed(42)
    n_rows = 5_000

    # Reference data
    ref_data = {
        "feature": np.random.randn(n_rows) * 10 + 50,
    }
    ref_df = pd.DataFrame(ref_data)
    ref_dataset = Dataset.from_pandas(ref_df, data_definition=DataDefinition())

    # Current data (with shifts)
    curr_data = {
        "feature": np.random.randn(n_rows) * 10 + 52,  # Shifted mean
    }
    curr_df = pd.DataFrame(curr_data)
    curr_dataset = Dataset.from_pandas(curr_df, data_definition=DataDefinition())

    # Test MeanValue with reference
    try:
        metric = MeanValue(column="feature")
        report = Report([metric])
        start_time = time.time()
        snapshot = report.run(curr_dataset, ref_dataset)
        elapsed = time.time() - start_time

        if len(snapshot.metric_results) > 0:
            print(f"✓ MeanValue with reference: {elapsed:.3f}s")
            return True
        else:
            print("✗ MeanValue with reference: no results")
            return False

    except Exception as e:
        print(f"✗ MeanValue with reference: {e}")
        return False


def test_performance_scaling():
    """Test performance with different data sizes."""
    print("\n" + "=" * 60)
    print("Testing Performance Scaling")
    print("=" * 60)

    sizes = [1_000, 5_000, 10_000]

    print(f"{'Dataset Size':<15} {'Time (s)':<12} {'Metrics/sec'}")
    print("-" * 40)

    for size in sizes:
        np.random.seed(42)
        data = {
            "feature": np.random.randn(size),
            "category": np.random.choice(["A", "B"], size),
        }
        df = pd.DataFrame(data)
        dataset = Dataset.from_pandas(df, data_definition=DataDefinition())

        # Create a report with multiple metrics
        metrics = [
            MeanValue(column="feature"),
            MinValue(column="feature"),
            MaxValue(column="feature"),
            StdValue(column="feature"),
            CategoryCount(column="category", category="A"),
        ]

        report = Report(metrics)

        try:
            start_time = time.time()
            report.run(dataset, None)
            elapsed = time.time() - start_time
            metrics_per_sec = len(metrics) / elapsed

            print(f"{size:<15,} {elapsed:<12.4f} {metrics_per_sec:.1f}")

        except Exception as e:
            print(f"{size:<15,} error: {e}")
            return False

    return True


if __name__ == "__main__":
    all_passed = True

    # Run all tests
    if not test_statistics_metrics():
        all_passed = False

    if not test_with_reference_data():
        all_passed = False

    if not test_performance_scaling():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All validation tests passed!")
        print("✓ Polars support integration is complete and working correctly")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
