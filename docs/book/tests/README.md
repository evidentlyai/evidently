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

You can apply some tests on the dataset level, for example, to evaluate dataset data drift. Here is an example with the default test parameters (defaults described below):
```python
data_drift_suite = TestSuite(tests=[
TestShareOfDriftedFeatures(),
TestNumberOfDriftedFeatures(),
])

data_drift_suite.run(reference_data=ref, current_data=curr,
column_mapping=ColumnMapping())
```

You get the visual report automatically if you call object `data_drift_suite `in Jupyter notebook:
```python
Data_drift_suite
```

You can get the test output as a JSON:
```python
data_drift.json()
```

Or in Python dictionary format:
```python
data_drift.as_dict()
```

## How to run tests for individual features

You can apply some tests to the individual features, for example, to check if a feature stays within the range. Here is an example with the default test parameters (defaults described below).
```python
suite = TestSuite(tests=[
TestColumnNANShare(column_name='hours-per-week'),
TestFeatureValueDrift(column_name='education'),
TestMeanInNSigmas(column_name='hours-per-week')
])

suite.run(reference_data=ref, current_data=curr)
```

You can get the test output as a JSON:
```python
suite.json()
```

You can also generate the visual report by calling the object suite:
```python
Suite
```

## How to set test parameters

You can set the parameters for specific tests to define the condition or expectation of the metric value. 

For example, you can set the upper or lower boundaries by defining **gt** (greater than) and **lt** (less than).  

```python
feature_level_tests = TestSuite(tests=[
    TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
    TestShareOfOutRangeValues(column_name='hours-per-week', lte=0),
    TestNumberOfOutListValues(column_name='education', lt=0),
    TestColumnNANShare(column_name='education', lt=0.2),
])

feature_level_tests.run(reference_data=ref, current_data=curr)
feature_level_tests
```

## Available parameters

| Condition parameter name | Explanation                                | Usage Example                                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------------------|
| eq: val                  | test_result == val                         | TestFeatureMin(feature_name=”numeric_feature”, eq=5)            |
| not_eq: val              | test_result != val                         | TestFeatureMin(feature_name=”numeric_feature”, ne=0)            |
| gt: val                  | test_result > val                          | TestFeatureMin(feature_name=”numeric_feature”, gt=5)            |
| gte: val                 | test_result >= val                         | TestFeatureMin(feature_name=”numeric_feature”, gte=5)           |
| lt: val                  | test_result <=val                          | TestFeatureMin(feature_name=”numeric_feature”, lt=5)            |
| lte: val                 | test_result <= val                         | TestFeatureMin(feature_name=”numeric_feature”, lte=5)           |
| is_in: list              | test_result == one of the values from list | TestFeatureMin(feature_name=”numeric_feature”, is_in=[3,5,7])   |
| not_in: list             | test_result != any of the values from list | TestFeatureMin(feature_name=”numeric_feature”, not_in=[-1,0,1]) |


# Available presets

The following presets are currently available in the library. You can also create your own test suites from individual tests, or combine individual tests and presets. 

## NoTargetPerformance 

**When to use it?**

If you generate model predictions in batches and get the true labels or values with a delay. 

You can run this preset to evaluate model quality through proxy metrics. For example, you can detect prediction drift or values far off the expected range that would signal that model operates in an unfamiliar environment.   

**Arguments:**

You can pass the list of the most important features for data drift evaluation. 

```python
no_target_performance = TestSuite(tests=[
   NoTargetPerformance(most_important_features=['education-num', 'hours-per-week']),
])

no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```

**Preset contents:**

| Test | Description | Default |
|---|---|---|
| TestValueDriftt(column=prediction_column) | Column-level test. Checks if the distribution of the model predictions drifted. | If the predictions drift is detected, the test fails.  The test uses the default Evidently drift detection logic.  |
| TestShareOfDriftedFeatures(ls=current.shape[1]//3) | Dataset-level test. Checks the share of drifting features in the dataset. | If >= 1/3 of features drifted, the test fails. |
| TestColumnsType(column='all') | Dataset-level test. Checks the match of all column types against the reference.  | If at least 1 column type does not match, the test fails.  |
| TestColumnNANShare(column=’all’) | Column-level test. Checks the share of missing values in all columns. | If no reference is provided: the test fails if > 0% of features are missing. If the reference is provided: the test fails if the share of missing values in a given column is at least 10% higher than in the reference.  |
| TestShareOfOutRangeValues(column=numerical_columns) | Column-level test. Checks if individual numerical columns contain values out of range.  | The test fails if at least 10% of values are out of range.  |
| TestShareOfOutListValues(column=categorical_columns) | Column-level test. Checks if individual categorical columns contain values out of the list. | The test fails if at least 10% of values are out of list.  |
| TestMeanInNSigmas(column=numerical_columns, n=2) | Column-level test. Checks if the mean values of all numerical columns are within the expected range, defined in standard deviations.  | The test fails if the mean value of a feature is out of 2 Std Dev range from its mean value in the reference.  |
| If most important feature list specified: TestValueDrift(column=most_important_feature_list) | Column-level test. Checks if the distributions of the important model features drifted. | If the feature drift is detected, the test fails. |

## DataStability

**When to use it?**

If you receive a new batch of input data and want to compare it to the previous one. 

You can run this preset to compare key descriptive statistics and the overall data shape between two batches you expect to be similar. For example, you can detect the appearance of the new categorical values, new values, or a significant difference in the number of rows. 

```python
data_stability = TestSuite(tests=[
   DataStability(),
])

data_stability.run(reference_data=ref, current_data=curr)
data_stability
```

**Preset contents:**

| Test | Description | Default |
|---|---|---|
| TestNumberOfRows() | Dataset-level test. Checks the number of rows against the reference.  | The test fails if the number of rows is at least 10% different compared to the reference.  |
| TestNumberOfColumns() | Dataset-level test. Checks the number of columns against the reference.  | If no reference is provided: the test fails if the number of columns is 0. If the reference is provided: the test fails if the number of columns is different from the reference.  |
| TestColumnsType(column='all') | Dataset-level test. Checks the match of all column types against the reference.  | The test fails if at least 1 column type does not match. |
| TestColumnNANShare(column=’all’) | Column-level test. Checks the share of missing values in all columns. | If no reference is provided: the test fails if > 0% of features are missing. If the reference is provided: the test fails if the share of missing values in a given column is at least 10% higher than in the reference.  |
| TestShareOfOutRangeValues(column=numerical_columns) | Column-level test. Checks if individual numerical columns contain values out of range.  | The test fails if at least 10% of values are out of range.  |
| TestShareOfOutListValues(column=categorical_columns) | Column-level test. Checks if individual categorical columns contain values out of the list. | The test fails if at least 10% of values are out of list.  |
| TestValueMeanInSTD(column=numerical_columns, n=2) | Column-level test. Checks if the mean values of all numerical columns are within the expected range, defined in standard deviations.  | The test fails if the mean value of a feature is out of 2 Std Dev range from its mean value in the reference.  |

## DataQuality

**When to use it?**

If you want to evaluate data quality, even without a reference dataset.

You can run this preset to assess whether a data batch is suitable for training or retraining. It would detect issues like missing data, duplicates, or constant and almost constant features.  


```python
data_quality = TestSuite(tests=[
   DataQuality(),
])

data_quality.run(reference_data=ref,current_data=curr)
data_quality
```
**Preset contents:**

| Test | Description | Default |
|---|---|---|
| TestColumnNANShare(column=’all’) | Column-level test. Checks the share of missing values in all columns. | If no reference is provided: the test fails if > 0% of features are missing. If the reference is provided: the test fails if the share of missing values in a given column is at least 10% higher than in the reference.  |
| TestMostCommonValueShare(column=’all’) | Column-level test. Checks the share of the most common value in each column. | If no reference is provided: the test fails if the share of the most common value is >= 80%. If the reference is provided: the test fails if the share of the most common value is at least 10% higher or lower than in the reference.  |
| TestNumberOfConstantColumns() | Dataset-level test. Checks the number of columns with all constant values.  | If no reference is provided: the test fails if there is at least 1 constant column. If the reference is provided: the test fails if the number of constant columns is higher than in the reference. |
| TestNumberOfDuplicatedColumns()      | Dataset-level test. Checks the number of duplicate columns. | If no reference is provided: the test fails if there is at least 1 duplicate column. If the reference is provided: the test fails if the number of duplucate columns is higher than in reference. |
| TestNumberOfDuplicatedRows(), | Dataset-level test. Checks the number of duplicate rows. | If no reference is provided: the test fails if there is at least 1 duplicate row. If the reference is provided: the test fails if the number of duplucate row is at least 10% higher or lower than in the reference. |
| TestHighlyCorrelatedFeatures() | Dataset-level test. Checks if any of the columns are highly correlated. | If no reference is provided: the test fails if there is at least 1 pair of features with the correlation >= 0.9 If the reference is provided:  the test fails if there is at least 10% change in the correlation strength for the most correlated feature pair. |

## DataDrift

**When to use it?**

If you receive a new batch of input data or generate a new set of predictions and want to compare the distributions. 

You can run this preset to detect data and concept drift. It would detect a shift in distributions using statistical tests and distance metrics. By default, it uses the in-built Evidently [drift detection logic](https://docs.evidentlyai.com/reports/data-drift#how-it-works) which selects the detection method based on data volume and type.

```python
data_drift = TestSuite(tests=[
   DataDrift(),
])

data_drift.run(reference_data=ref, current_data=curr)
data_drift
```

| Test | Description | Default |
|---|---|---|
| TestShareOfDriftedFeatures() | Dataset-level test. Checks the share of drifting features in the dataset. | If >= 1/3 features drifted, the test fails. |
| TestValueDrift(column=target) | Column-level test. Checks if the distribution of the model target (if available) drifted. | If the target drift is detected, the test fails.  |
| TestValueDrift(column=prediction) | Column-level test. Checks if the distribution of the model predictions drifted. | If the predictions drift is detected, the test fails.  |
| TestValueDrift(column=numerical_columns+categorical_columns) | Column-level test. Checks if the distribution of each individual feature drifted. | If the feature drift is detected, the test fails.  |

# Available tests

The following tests are currently available in the library: 

```python
TestNumberOfColumns()
TestNumberOfRows()
TestColumnNANShare()
TestShareOfOutRangeValues()
TestNumberOfOutListValues()
TestMeanInNSigmas()
TestMostCommonValueShare()
TestNumberOfConstantColumns()
TestNumberOfDuplicatedColumns()
TestNumberOfDuplicatedRows()
TestHighlyCorrelatedFeatures()
TestTargetFeaturesCorrelations()
TestShareOfDriftedFeatures()
TestValueDrfit()
TestColumnsType()
```

We are constantly expanding the list of available tests. You can see all currently available tests in the example notebook, grouped by per-column and per-dataset level tests.

# Example

You can refer to this example notebook:
[https://colab.research.google.com/drive/1IH1TYrZXT8tBFc1i6XFVmFy4rOkkX3va?usp=sharing]

