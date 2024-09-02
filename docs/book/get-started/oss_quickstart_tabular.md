---
description: Run your first evaluation using Evidently open-source, for tabular data.
---

It's best to run this example in Jupyter Notebook or Google Colab so that you can render HTML Reports directly in a notebook cell.

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

# What's next?

Want more details on Reports and Test Suites? See an in-depth tutorial.

{% content-ref url="../examples/tutorial_reports_tests.md" %}
[Reports and Tests Tutorial](../examples/tutorial_reports_tests.md). 
{% endcontent-ref %}

Want to set up monitoring? Send the evaluation results to Evidently Cloud for analysis and tracking. See the Quickstart:

{% content-ref url="cloud_quickstart_llm.md" %}
[Evidently Cloud Quickstart](cloud_quickstart_tabular.md). 
{% endcontent-ref %}

Working with LLMs? Check the Quickstart:

{% content-ref url="cloud_quickstart_llm.md" %}
[LLM Evaluation Quickstart](oss_quickstart_llm.md). 
{% endcontent-ref %}

Need help? Ask in our [Discord community](https://discord.com/invite/xZjKRaNp8b).
