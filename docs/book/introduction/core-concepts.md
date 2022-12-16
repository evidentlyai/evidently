This is an explanatory page to describe the key features and concepts at Evidently. 

# TL;DR

Evidently helps evaluate, test and monitor ML models in production. 

A **Metric** is a core component of Evidently. You can combine multiple **Metrics** in a **Report**. Reports are best for visual analysis and debugging of your models and data.

A **Test** is a metric with a condition. Each test returns a pass or fail result. You can combine multiple **Tests** in a **Test Suite**. Test Suites are best for automated model checks as part of an ML pipeline.

For both Tests and Metrics, Evidently has **Presets**. These are pre-built combinations of metrics or checks that fit a specific use case. 

# Metrics and Reports

## What is a Metric?

A **Metric** is a component that evaluates a specific aspect of the data or model quality. 

A **Metric** can be, literally, a single metric (for example, `DatasetMissingValuesMetric()` returns the share of missing features). It can also be a combination of metrics (for example, `DatasetSummaryMetric()` calculates various descriptive statistics for the dataset). Metrics exist on the dataset level and on the column level. 

Each **Metric** has a visual render. Some visualizations simply return the values:  

![RegressionQualityMetric](../.gitbook/assets/reports/metric_example_regression_quality-min.png)

Others have rich visualizations. Here is an example of a dataset-level Metric that evaluates the error of a regression model:

![RegressionErrorDistribution](../.gitbook/assets/reports/metric_example_error_distribution-min.png)

Here is an example of a column-level Metric that evaluates the value range of certain feature: 

![ColumnValueRangeMetric](../.gitbook/assets/reports/metric_example_value_range-min.png)

Metric output is available as an interactive HTML report, JSON, or Python dictionary. The JSON “version” returns any new calculated values and, optionally, some other useful information such as histogram bins. 

Evidently contains 35+ **Metrics** related to data quality, integrity, drift and model performance. You can also implement a custom one.

## What is a Report?

A **Report** is a combination of different Metrics that evaluate data or ML model quality. 

Уou can display an interactive report inside a Jupyter notebook or export it as an HTML file:

![Data Drift report example](../.gitbook/assets/reports/report_example_data_drift-min.png)

You can also generate the Report as a text summary: as a JSON or as a Python dictionary. 

```python
{'timestamp': '2022-10-26 17:46:47.214403',
 'metrics': {'DatasetDriftMetric': {'threshold': 0.5,
   'number_of_columns': 15,
   'number_of_drifted_columns': 5,
   'share_of_drifted_columns': 0.3333333333333333,
   'dataset_drift': False},
  'DataDriftTable': {'number_of_columns': 15,
   'number_of_drifted_columns': 5,
   'share_of_drifted_columns': 0.3333333333333333,
   'dataset_drift': False,
   'drift_by_columns': {'age': {'column_name': 'age',
     'column_type': 'num',
     'stattest_name': 'Wasserstein distance (normed)',
     'drift_score': 0.18534692319042428,
     'drift_detected': True,
     'threshold': 0.1}}}}}
```
Most Reports can be calculated for a single dataset. If you pass two datasets, they will show a side-by-side comparison.

You can generate a Report by listing individual **Metrics** to include in it. You can also run one of the **Presets** that cover a specific aspect of the model or data performance. 

## What is a Metric Preset?

A **Metric Preset** is a pre-built Report that combines Metrics for a particular use case.

You can think of it as a template. For example, there is a Preset to check for Data Drift (`DataDriftPreset`), Data Quality (`DataQualityPreset`), or Regression Performance (`RegressionPreset`). 

![ColumnValueRangeMetric](../.gitbook/assets/reports/evidently_reports_min.png)

You can explore all Metrics and Presets here:

{% content-ref url="../reference/all-metrics.md" %}
[All metrics](all-metrics.md)
{% endcontent-ref %}

## When to use Reports

You can use Reports at different stages of the ML lifecycle: from exploratory data analysis and model validation to production monitoring and debugging.  

**Debugging and exploration**. Reports are best for visual analysis of the data or model performance. For example, during model quality evaluation on the training set, when debugging the model quality decay, or comparing two models. 

**Metric logging**. You can also add a model or data evaluation step in the ML pipeline, get outputs as JSON, and log it to a database. For example, you can later visualize it using other BI tools.

**Reporting and documentation**. You can also use Evidently reports to share results with the team and stakeholders or log them as documentation. For example, you can record the results of the model performance after training.

# Tests and Test Suites

## What is a Test?

Tests help perform structured data and ML model performance checks. They explicitly define the expectations from your data and model.

A **Test** is a metric with a condition. It calculates a value and compares it against the defined threshold. 

If the condition is satisfied, the test returns a **success**. 

If you choose to get a visual output with the test results, you will see the current value of the metric and the test condition. On expand, you will get a supporting visualization. 

Here is an example of a column-level Test that evaluates the mean value stability:

![Mean value stability test](../.gitbook/assets/tests/test_example_success_data-min.png)

Here is an example of a dataset-level Test that evaluates model error:

![Root mean square error test](../.gitbook/assets/tests/test_example_success_model-min.png)

If the condition is not satisfied, the Test returns a **fail**:

![Data drift per feature test](../.gitbook/assets/tests/test_example_fail-min.png)

If the Test execution fails, it will return an error. 

Evidently contains 70+ individual tests that cover different aspects of model and data quality. 

You can set test conditions on your own or pass the reference dataset to auto-generate test conditions. You can also run most of the tests using defaults even if you do not pass a reference dataset: the tests will use heuristics and dummy models.

Test output is available as an interactive HTML report, JSON, or Python dictionary.

## What is a Test Suite?

In most cases, you’d want to run more than one check. 

You can list multiple Tests and execute them together in a **Test Suite**. You will see a summary of the results:

![Custom test suite example](../.gitbook/assets/tests/test_suite_example-min.png)

If you include a lot of Tests, you can navigate the output by groups: 

![No target performance test suite example](../.gitbook/assets/tests/test_suite_navigation-min.png)

You can create your Test Suite from individual Tests or use one of the existing **Presets**. 

## What is a Test Preset?

A **Test Preset** is a pre-built Test Suite that combines checks for a particular use case. 

You can think of it as a template to start with. For example, there is a Preset to check for Data Quality (`DataQualityTestPreset`), Data Stability (`DataStabilityTestPreset`), or Regression model performance (`RegressionTestPreset`).

![Regression performance test suite example](../.gitbook/assets/tests/test_preset_example-min.png)

You can explore all Tests and Presets here:

{% content-ref url="../reference/all-tests.md" %}
[All tests](all-tests.md)
{% endcontent-ref %}

## When to use Test Suites

For **test-based monitoring** of production ML models: tests are best suited for integration in ML prediction pipelines. You can easily integrate Evidently Tests with workflow management tools like Airflow.

You can use them to perform batch checks for your data or models. 

For example, you can run the tests when you:
* get a new batch of the input data 
* generate a new set of predictions
* receive a new batch of the labeled data
* want to check on your model on a schedule

![Model lifecycle](../.gitbook/assets/tests/test_suite_lifecycle-min.png)

You can then build a conditional workflow based on the result of the tests: for example, generate a visual report for debugging, trigger model retraining, or send an alert.

**During model development**: you can also use tests during model development and validation. For example, you can run tests to evaluate the data quality of the new feature set or to compare test performance to training.

# Test Suites or Reports?

**Reports** and **Test Suites** are complementary interfaces. 

**Reports** are best for debugging, exploratory and ad hoc analytics. They focus on interactive visualizations and do not require setting any expectations upfront. You can use them, for example, when you just put a model in production and want to closely monitor the performance. It is best to use Reports on smaller datasets or sample your data first.  

**Test Suites** are best for automation. Use them when you can set up expectations upfront (or derive them from the reference dataset). Tests force you to think through what you expect from your data and models, and you can run them at scale, only reacting to the failure alerts. You can use Test Suites on larger datasets since they do not include heavy visuals.

You can also use both Reports and Test Suites. For example, run tests for automated model checks and if tests fail, use Reports for visual debugging. 
