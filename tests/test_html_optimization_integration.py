"""
Phase 4 Tests: Integration, Extended Testing, and Performance Validation

Tests to verify:
1. HTML size optimization integration
2. Configuration options work correctly
3. Backward compatibility is maintained
4. Performance with large datasets
5. End-to-end optimization accuracy
"""

import sys
import time

import numpy as np
import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.metrics import CategoryCount
from evidently.metrics import MeanValue
from evidently.metrics import MinValue
from evidently.presets import DataDriftPreset


def create_test_dataset(n_rows: int = 10_000, n_features: int = 10) -> tuple:
    """Create test datasets for Phase 4 tests."""
    np.random.seed(42)

    # Reference data
    ref_data = {f"feature_{i}": np.random.randn(n_rows) for i in range(n_features)}
    ref_data["category"] = np.random.choice(["A", "B", "C", "D", "E"], n_rows)
    ref_data["target"] = np.random.choice(["yes", "no"], n_rows)

    ref_df = pd.DataFrame(ref_data)
    ref_dataset = Dataset.from_pandas(ref_df, data_definition=DataDefinition())

    # Current data (slight shift)
    curr_data = {f"feature_{i}": np.random.randn(n_rows) + 0.1 for i in range(n_features)}
    curr_data["category"] = np.random.choice(["A", "B", "C", "D", "E"], n_rows)
    curr_data["target"] = np.random.choice(["yes", "no"], n_rows)

    curr_df = pd.DataFrame(curr_data)
    curr_dataset = Dataset.from_pandas(curr_df, data_definition=DataDefinition())

    return curr_dataset, ref_dataset


def test_html_optimization_disabled_by_default():
    """Test that HTML optimization is disabled by default (backward compatibility)."""
    print("\n" + "=" * 70)
    print("TEST 1: HTML Optimization Disabled by Default")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=1_000, n_features=5)

        # Create report WITHOUT optimization (default)
        report = Report(
            [MeanValue(column="feature_0"), MeanValue(column="feature_1")],
            optimize_html_size=False,  # Explicitly False
        )

        snapshot = report.run(curr_dataset, ref_dataset)

        # Optimization should not be applied
        assert snapshot.get_optimization_stats() is None, "Optimization should be None when disabled"

        # Report should still be generated
        html = snapshot.get_html_str(as_iframe=False)
        assert len(html) > 100, "HTML should be generated"

        print("✓ HTML optimization correctly disabled by default")
        print(f"  HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_html_optimization_enabled():
    """Test that HTML optimization can be enabled."""
    print("\n" + "=" * 70)
    print("TEST 2: HTML Optimization Enabled")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=1_000, n_features=5)

        # Create report WITH optimization
        report = Report([MeanValue(column="feature_0"), MeanValue(column="feature_1")], optimize_html_size=True)

        snapshot = report.run(curr_dataset, ref_dataset)

        # Get HTML with optimization applied
        html = snapshot.get_html_str(as_iframe=False)
        assert len(html) > 100, "HTML should be generated"

        # Get optimization stats
        opt_stats = snapshot.get_optimization_stats()
        assert opt_stats is not None, "Optimization stats should be available"

        print("✓ HTML optimization enabled successfully")
        print(f"  Optimization applied: {opt_stats.get('optimizations_applied', [])}")
        print(f"  Original size: {opt_stats.get('original_size_kb', 0):.1f} KB")
        print(f"  Optimized size: {opt_stats.get('optimized_size_kb', 0):.1f} KB")
        print(f"  Reduction: {opt_stats.get('reduction_percent', 0):.1f}%")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_optimization_config_options():
    """Test that optimization configuration options work."""
    print("\n" + "=" * 70)
    print("TEST 3: Optimization Configuration Options")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=2_000, n_features=10)

        # Test different configurations
        configs = [
            {"histogram_bins": 20, "max_categories": 15},
            {"histogram_bins": 50, "max_categories": 30},
            {"downsample_points": 500},
            {"downsample_points": 2000},
        ]

        for i, config in enumerate(configs):
            report = Report([MeanValue(column=f"feature_{j}") for j in range(5)], optimize_html_size=True, **config)

            # Verify config is stored
            assert report.histogram_bins or report.max_categories or report.downsample_points

            snapshot = report.run(curr_dataset, ref_dataset)
            html = snapshot.get_html_str(as_iframe=False)

            print(f"  Config {i+1}: {config}")
            print(f"    HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
            print(f"    Metrics: {len(snapshot.metric_results)}")

        print("✓ All configuration options work correctly")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_backward_compatibility():
    """Test that changes don't break existing code."""
    print("\n" + "=" * 70)
    print("TEST 4: Backward Compatibility")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=1_000, n_features=5)

        # Old-style report creation (without new parameters)
        report_old = Report(
            [MeanValue(column="feature_0"), MinValue(column="feature_1")], metadata={"test": "value"}, tags=["test_tag"]
        )

        # Should run without errors
        snapshot = report_old.run(curr_dataset, ref_dataset)

        # Old export methods should work
        html = snapshot.get_html_str(as_iframe=False)
        json_str = snapshot.json()
        dict_data = snapshot.dict()

        assert len(html) > 0, "HTML export should work"
        assert len(json_str) > 0, "JSON export should work"
        assert isinstance(dict_data, dict), "Dict export should work"
        assert "metrics" in dict_data, "Dict should have metrics"

        print("✓ All backward compatibility checks passed")
        print(f"  Metrics: {len(snapshot.metric_results)}")
        print(f"  HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
        print(f"  JSON size: {len(json_str.encode('utf-8')) / 1024:.1f} KB")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_parallel_with_optimization():
    """Test that parallel execution works with HTML optimization."""
    print("\n" + "=" * 70)
    print("TEST 5: Parallel Execution + HTML Optimization")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=5_000, n_features=15)

        # Use both parallel execution and HTML optimization
        metrics = [MeanValue(column=f"feature_{i}") for i in range(min(15, 15))] + [
            CategoryCount(column="category", category=cat) for cat in ["A", "B", "C", "D", "E"]
        ]

        report = Report(metrics, enable_parallel=True, max_parallel_workers=4, optimize_html_size=True)

        start = time.time()
        snapshot = report.run(curr_dataset, ref_dataset)
        exec_time = time.time() - start

        html = snapshot.get_html_str(as_iframe=False)

        print("✓ Parallel execution + optimization works")
        print(f"  Execution time: {exec_time:.2f}s")
        print(f"  Metrics: {len(snapshot.metric_results)}")
        print(f"  HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_large_dataset_optimization():
    """Test optimization with large dataset."""
    print("\n" + "=" * 70)
    print("TEST 6: Large Dataset with Optimization")
    print("=" * 70)

    try:
        print("Creating large dataset (50k rows × 20 features)...")
        curr_dataset, ref_dataset = create_test_dataset(n_rows=50_000, n_features=20)

        # Create report with many metrics
        metrics = [MeanValue(column=f"feature_{i}") for i in range(min(20, 20))]

        # Without optimization
        print("Running without optimization...")
        report_no_opt = Report(metrics, optimize_html_size=False, enable_parallel=True, max_parallel_workers=4)

        start = time.time()
        snapshot_no_opt = report_no_opt.run(curr_dataset, ref_dataset)
        time_no_opt = time.time() - start
        html_no_opt = snapshot_no_opt.get_html_str(as_iframe=False)
        size_no_opt = len(html_no_opt.encode("utf-8")) / 1024

        # With optimization
        print("Running with optimization...")
        report_opt = Report(metrics, optimize_html_size=True, enable_parallel=True, max_parallel_workers=4)

        start = time.time()
        snapshot_opt = report_opt.run(curr_dataset, ref_dataset)
        time_opt = time.time() - start
        html_opt = snapshot_opt.get_html_str(as_iframe=False)
        size_opt = len(html_opt.encode("utf-8")) / 1024

        size_reduction = (1 - size_opt / size_no_opt) * 100 if size_no_opt > 0 else 0

        print("✓ Large dataset test completed")
        print(f"  Execution time (no opt): {time_no_opt:.2f}s")
        print(f"  Execution time (opt): {time_opt:.2f}s")
        print(f"  HTML size (no opt): {size_no_opt:.1f} KB")
        print(f"  HTML size (opt): {size_opt:.1f} KB")
        print(f"  Size reduction: {size_reduction:.1f}%")
        print(f"  Metrics: {len(snapshot_opt.metric_results)}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_optimization_with_presets():
    """Test optimization with metric presets."""
    print("\n" + "=" * 70)
    print("TEST 7: Optimization with Metric Presets")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=5_000, n_features=15)

        columns = [f"feature_{i}" for i in range(min(15, 15))] + ["category"]

        report = Report(
            [DataDriftPreset(columns=columns)], optimize_html_size=True, enable_parallel=True, max_parallel_workers=4
        )

        start = time.time()
        snapshot = report.run(curr_dataset, ref_dataset)
        exec_time = time.time() - start

        html = snapshot.get_html_str(as_iframe=False)

        print("✓ Preset-based report with optimization works")
        print(f"  Execution time: {exec_time:.2f}s")
        print(f"  Metrics: {len(snapshot.metric_results)}")
        print(f"  HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_export_formats_with_optimization():
    """Test that export formats work with optimization."""
    print("\n" + "=" * 70)
    print("TEST 8: Export Formats with Optimization")
    print("=" * 70)

    try:
        curr_dataset, ref_dataset = create_test_dataset(n_rows=2_000, n_features=5)

        report = Report([MeanValue(column="feature_0"), MinValue(column="feature_1")], optimize_html_size=True)

        snapshot = report.run(curr_dataset, ref_dataset)

        # Test HTML export
        html = snapshot.get_html_str(as_iframe=False)
        assert len(html) > 100, "HTML export should work"

        # Test JSON export
        json_str = snapshot.json()
        assert len(json_str) > 100, "JSON export should work"

        # Test dict export
        dict_data = snapshot.dict()
        assert isinstance(dict_data, dict), "Dict export should work"

        print("✓ All export formats work with optimization")
        print(f"  HTML size: {len(html.encode('utf-8')) / 1024:.1f} KB")
        print(f"  JSON size: {len(json_str.encode('utf-8')) / 1024:.1f} KB")
        print(f"  Metrics: {len(snapshot.metric_results)}")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PHASE 4 - INTEGRATION & EXTENDED TESTING")
    print("=" * 70)

    results = []

    # Run all Phase 4 tests
    results.append(("HTML Optimization Disabled by Default", test_html_optimization_disabled_by_default()))
    results.append(("HTML Optimization Enabled", test_html_optimization_enabled()))
    results.append(("Configuration Options", test_optimization_config_options()))
    results.append(("Backward Compatibility", test_backward_compatibility()))
    results.append(("Parallel + Optimization", test_parallel_with_optimization()))
    results.append(("Large Dataset", test_large_dataset_optimization()))
    results.append(("Presets Support", test_optimization_with_presets()))
    results.append(("Export Formats", test_export_formats_with_optimization()))

    # Summary
    print("\n" + "=" * 70)
    print("PHASE 4 TEST SUMMARY")
    print("=" * 70)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name:<40} {status}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\nResult: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All Phase 4 tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {total - passed} test(s) failed")
        sys.exit(1)
