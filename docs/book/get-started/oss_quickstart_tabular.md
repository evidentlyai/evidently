---
description: Run your first evaluation using Evidently open-source, for tabular data.
---

You can launch this hello-world example in Jupyter notebook, Colab or other Python environment.

# Installation 

Install **Evidently** using the pip package manager:

```python
!pip install evidently
``` 

# Imports 

Import the Evidently components and a toy “Iris” dataset:

```python
import pandas as pd

from sklearn import datasets

from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

iris_data = datasets.load_iris(as_frame='auto')
iris_frame = iris_data.frame
``` 

# Run a Test Suite

Split the data into two batches. Run a set of pre-built data quality Tests to evaluate the quality of the `current_data`:

```python
data_stability= TestSuite(tests=[
    DataStabilityTestPreset(),
])
data_stability.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_stability 
```

This will automatically generate tests on share of nulls, out-of-range values, etc. – with test conditions generated based on the first "reference" dataset.

# Get a Report

Get a Data Drift Report to see if the data distributions shifted between two datasets:

```python
data_drift_report = Report(metrics=[
    DataDriftPreset(),
])

data_drift_report.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_drift_report
```

# Want to see more?

* Take the complete [Report & Test Suite Tutorial](tutorial.md) to learn how to run checks like this in detail (15 minutes). You can also evaluate ML model quality, e.g., for classification, regression, and ranking models, and work with text data.
* Start with ML monitoring. Go through the [Evidently Cloud Quickstart](quickstart-cloud.md) (2 min) to get a dashboard to track metrics over time.
* Working with LLMs? See an [LLM Evaluation Quicktart](quickstart-llm.md) to see how to run checks for text data.
