<h1 align="center">10 minutes to Evidently</h1>

This is a short introduction to Evidently. 

# Input Data

You should prepare the data as pandas DataFrames. It could be two datasets - reference data and current production data. Or just one - you will need to identify rows that refer to reference and current data. If you do not want to perform a comparison, you can also pass a single dataset.

If you deal with large datasets, you can take a sample from it:

```python
df.sample(1000, random_state=0) 
```
# Column mapping
To create column mapping, you need to specify the following parameters:
* `target` - the name of the column with the target function
* `prediction` - the name of the column(s) with model predictions
* `id` - ID column in the dataset
* `datetime` - the name of the column with datetime
* `numerical_features` - list of numerical features
* `categorical_features` - list of categorical features

If the column_mapping is not specified or set as None, we use the default mapping strategy:
* All features will be treated as numerical.
* The column with 'id' name will be treated as an ID column.
* The column with 'datetime' name will be treated as a datetime column.
* The column with 'target' name will be treated as a target function.
* The column with 'prediction' name will be treated as a model prediction.

Example 

```python
from evidently import ColumnMapping

column_mapping = ColumnMapping()

column_mapping.target = 'y'
column_mapping.prediction = 'pred' # predictions
column_mapping.id = None 
column_mapping.datetime = 'date' 
column_mapping.numerical_features = ['temp', 'atemp', 'humidity'] 
column_mapping.categorical_features = ['season', 'holiday'] 
```

# Choose a Report

A report evaluates a specific aspect of the model or data performance.

You can choose one or several Metric Presets to generate a pre-built report:

* `DataQualityPreset` to explore the dataset and evaluate its quality
* `DataDriftPreset` to estimate the data drift in the input feature
* `TargetDriftPreset` to estimate target (prediction) drift
* `RegressionPerformancePreset` to explore the performance of a regression model
* `ClassificationPerformancePreset` to explore the performance of a classification model

## Generate the Report

To generate the chosen report and explore it in the Jupyter notebook run these commands:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.metric_preset import TargetDriftPreset

drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
drift_report.run(reference_data=reference, current_data=current)
drift_report
```

## Export the Report in different formats

To save the Drift report as an HTML file, run:

```python
drift_report.save_html("file.html")
```

You can also get the output as a JSON or Python dictionary if you want to integrate the calculated metrics and statistical test results into external pipelines and visualization tools.

To get the output as a JSON, run:

```python
drift_report.json()
```

To get the output as a Python dictionary, run:

```python
drift_report.as_dict()
```

# Test Suites 

You can also run the Test Suites. This is an alternative interface that helps perform an explicit comparison of each metric against a defined condition and returns a pass or fail result.

You can choose one or several of the several Test Presets to run the pre-built Test Suites.
* `NoTargetPerformanceTestPreset` to evaluate the model performance without ground truth labels
* `DataStabilityTestPreset`to compare descriptive stats and similarity between the two data batches
* `DataQualityTestPreset`to check the data for issues like missing values or duplicates
* `DataDriftTestPreset` to compare the column distribution
* `RegressionTestPreset` to test the quality of a regression model
* `MulticlassClassificationTestPreset` to test the quality of a multi-class classification model
* `BinaryClassificationTopKTestPreset` to test the quality of a binary classification model at K
* `BinaryClassificationTestPreset` to test the quality of a binary classification model

To run the NoTargetPerformanceTestPreset and get the visual report with the result of the tests:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformanceTestPreset(),
])
no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```
To get the output as a JSON, run:

```python
no_target_performance.json()
```

# Customization

You can also build a custom Report from individual Metrics or a Test Suite from individual Tests. Evidently has 50+ inidvidual metrics and tests to choose from. All you need is to list which metrics or tests to include. 

Here is how you build a custom Test Suite from individual tests:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfMissingValues(column_name='hours-per-week'),
    TestColumnDrift(column_name='education'),
    TestMeanInNSigmas(column_name='hours-per-week')
])
```

Each metric and test has parameters that you can pass to modify how the metric is calculated or to define a custom condition of the test. You can consult these documentation pages for reference:
* [All tests](https://docs.evidentlyai.com/reference/all-tests): all individual tests and parameters
* [All metrics](https://docs.evidentlyai.com/reference/all-metrics): all individual metrics and parameters
