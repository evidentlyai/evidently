You can launch this hello-world example in Jupyter notebook or in Colab. 

# Installation 

## MAC OS and Linux, Jupyter notebook

Install **Evidently** using the pip package manager:

```bash
$ pip install evidently
```

Install and enable Jupyter **nbextension**. Run the two following commands in the terminal from the Evidently directory:

```
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
$ jupyter nbextension enable evidently --py --sys-prefix
```

## Colab

Install **Evidently**:

```python
try:
    import evidently
except:
    !npm install -g yarn
    !pip install git+https://github.com/evidentlyai/evidently.git
``` 

# Imports 

Import toy data and required Evidently components:

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

# Run a test suite

Split the toy data into two batches and compare them: 

```python
data_stability= TestSuite(tests=[
    DataStabilityTestPreset(),
])
data_stability.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_stability 
``` 

# Get a report

Get a visual report to explore the feature distribution drift in detail:

```python
data_drift_report = Report(metrics=[
    DataDriftPreset(),
])

data_drift_report.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_drift_report
``` 

# Want to see more?

You can explore a more detailed [Getting Started] tutorial to understand how Evidently works.
