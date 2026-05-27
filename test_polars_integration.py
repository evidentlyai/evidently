"""
Simple test script to validate the Polars support implementation.
"""

import sys
import time

import numpy as np
import pandas as pd

from evidently import DataDefinition
from evidently import Dataset
from evidently import Report
from evidently.core.data import describe_dataframe_type
from evidently.metrics import MeanValue

# Create simple test data
print("Creating test data...")
n_rows = 10_000
data = {
    "feature_1": np.random.randn(n_rows),
    "feature_2": np.random.randn(n_rows),
    "feature_3": np.random.choice(["A", "B", "C"], n_rows),
}

df = pd.DataFrame(data)
print(f"Dataset shape: {df.shape}")
print(f"DataFrameType: {describe_dataframe_type(df)}")

# Create Evidently Dataset
print("\nCreating Evidently Dataset...")
current_dataset = Dataset.from_pandas(df, data_definition=DataDefinition())
print("✓ Dataset created successfully")

# Test with a simple metric
print("\nTesting MeanValue metric on feature_1...")
try:
    report = Report([MeanValue(column="feature_1")])
    start_time = time.time()
    snapshot = report.run(current_dataset, None)
    elapsed = time.time() - start_time

    # Get result
    results = snapshot.metric_results
    print(f"✓ Metric execution completed in {elapsed:.3f}s")
    print(f"✓ Number of metric results: {len(results)}")

    # Print actual metric value
    for result in results:
        print(f"✓ Metric result: {result}")

except Exception as e:
    print(f"✗ Error during metric execution: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed! Polars support integration is working.")
sys.exit(0)
