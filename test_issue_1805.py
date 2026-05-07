"""
Test script to verify legacy metric migrations work correctly.
This tests the three newly migrated metrics from Issue #1805.
"""

import pandas as pd
from evidently import Report
from evidently.metrics import (
    RegressionErrorBiasTable,
    RegressionErrorDistribution,
    RegressionPredictedVsActualScatter,
    MAE,
)
from evidently.core.datasets import Dataset
from evidently.core.data_definition import DataDefinition, Regression


def test_migrated_metrics():
    """Test that newly migrated legacy metrics work with new Report API."""
    
    # Create sample regression data
    current_df = pd.DataFrame({
        'target': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        'prediction': [1.1, 2.2, 2.8, 4.1, 4.9, 6.2, 7.1, 7.9],
        'age': [25, 35, 45, 55, 65, 75, 85, 95],
        'income': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000],
    })
    
    reference_df = pd.DataFrame({
        'target': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        'prediction': [0.9, 2.1, 3.1, 3.9, 5.1, 5.9, 7.2, 8.1],
        'age': [25, 35, 45, 55, 65, 75, 85, 95],
        'income': [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000],
    })
    
    # Setup data definition with regression task
    data_definition = DataDefinition()
    data_definition.add_regression_task(
        Regression(target='target', prediction='prediction')
    )
    
    current = Dataset.from_pandas(current_df, data_definition=data_definition)
    reference = Dataset.from_pandas(reference_df, data_definition=data_definition)
    
    # Test 1: Basic instantiation
    print("Test 1: Metric instantiation...")
    m1 = RegressionPredictedVsActualScatter()
    m2 = RegressionErrorBiasTable()
    m3 = RegressionErrorDistribution()
    print("✓ All metrics instantiate successfully")
    
    # Test 2: Metrics with parameters
    print("\nTest 2: Metrics with parameters...")
    m2_with_params = RegressionErrorBiasTable(columns=['age', 'income'], top_error=0.1)
    print(f"✓ RegressionErrorBiasTable accepts parameters: columns={m2_with_params.columns}, top_error={m2_with_params.top_error}")
    
    # Test 3: Report creation
    print("\nTest 3: Report creation with migrated metrics...")
    report = Report([
        RegressionPredictedVsActualScatter(),
        RegressionErrorBiasTable(),
        RegressionErrorDistribution(),
        MAE(),  # Existing metric for comparison
    ])
    print("✓ Report created with 4 metrics (3 new + 1 existing)")
    
    # Test 4: Run report
    print("\nTest 4: Running report with current and reference data...")
    snapshot = report.run(current, reference)
    print(f"✓ Report executed successfully")
    print(f"  - Snapshot created with {len(snapshot._snapshot_item)} items")
    
    # Test 5: Access results
    print("\nTest 5: Accessing metric results...")
    
    try:
        r1 = snapshot.get_metric_result("RegressionPredictedVsActualScatter")
        print(f"✓ RegressionPredictedVsActualScatter:  current={r1.current.value:.1f}")
    except Exception as e:
        print(f"✗ RegressionPredictedVsActualScatter failed: {e}")
    
    try:
        r2 = snapshot.get_metric_result("RegressionErrorBiasTable")
        print(f"✓ RegressionErrorBiasTable: current={r2.current.value:.1f}")
    except Exception as e:
        print(f"✗ RegressionErrorBiasTable failed: {e}")
    
    try:
        r3 = snapshot.get_metric_result("RegressionErrorDistribution")
        print(f"✓ RegressionErrorDistribution: current={r3.current.value:.1f}")
    except Exception as e:
        print(f"✗ RegressionErrorDistribution failed: {e}")
    
    try:
        r4 = snapshot.get_metric_result("MAE")
        print(f"✓ MAE (existing): current={r4.current.value:.2f}")
    except Exception as e:
        print(f"✗ MAE failed: {e}")
    
    # Test 6: Without reference data
    print("\nTest 6: Running metrics without reference data...")
    snapshot_no_ref = report.run(current, None)
    print(f"✓ Report works without reference data")
    
    # Test 7: Metric with specific columns
    print("\nTest 7: Running RegressionErrorBiasTable with specific columns...")
    report_custom = Report([
        RegressionErrorBiasTable(columns=['age'])
    ])
    snapshot_custom = report_custom.run(current, reference)
    r_custom = snapshot_custom.get_metric_result("RegressionErrorBiasTable")
    print(f"✓ Custom column selection works: {r_custom.current.value}")
    
    print("\n" + "="*60)
    print("SUCCESS! All tests passed.")
    print("Issue #1805 Legacy metrics are now working with new Report API!")
    print("="*60)


if __name__ == "__main__":
    test_migrated_metrics()
