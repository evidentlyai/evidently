# What is a test?

Tests help perform structured data and ML model performance checks. 

Tests are best-suited for integration in ML prediction pipeline, for example, with tools like Airflow. You can also execute the tests in the Jupyter notebook and Colab. The output is available as a JSON or as an HTML report.

A **test** is a single check. It calculates a specific metric and compares it with the defined condition or threshold. Some tests require a reference dataset for comparison. When possible, tests also have default conditions. If the user does not specify a condition, Evidently will compare the metric value against this default.   

The test can return one of the following results: 
* **Success**: test condition is satisfied.
* **Fail**: test condition is not satisfied; the test has top priority.
* **Warning**: test condition is not satisfied; the test has secondary priority. (The test importance parameter will be available in the next release.)  * **Error**: the test execution failed.

A **test suite** is a combination of checks grouped for a particular use case. A test suite executes multiple tests simultaneously and returns the summary of results. You can create your test suite from individual tests or use one of the existing **presets**. 

# How to run tests in Evidently

## Installation and data prep

After [installation](https://docs.evidentlyai.com/install-evidently), import evidently and the required tests or test suites:

```python
from evidently import ColumnMapping
from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import NoTargetPerformance, DataQuality, DataStability, DataDrift
```

You need to prepare two datasets for comparison. Here is a simple example:

```python
#load data
data = fetch_openml(name='adult', version=2, as_frame='auto')
df = data.frame
 
#create target and prediction
df['target'] = df['education-num']
df['prediction'] = df['education-num'].values + np.random.normal(0, 6, df.shape[0])
 
#split data into reference and current
#reference data
ref = df[~df.education.isin(['Some-college', 'HS-grad', 'Bachelors'])]
 
#current data
curr = df[df.education.isin(['Some-college', 'HS-grad', 'Bachelors'])]
```
Refer to the [input data](https://docs.evidentlyai.com/features/dashboards/input_data) and [column mapping](https://docs.evidentlyai.com/features/dashboards/column_mapping) for more details on data preparation. 

## How to run tests for a dataset
