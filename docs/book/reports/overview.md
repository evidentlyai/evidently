This is an explanatory page to describe the functionality of the Evidently Reports and Metrics. For code instructions, head to the [user guide](../tests-and-reports/get-reports.md).

# What is a Report?

A **Report** is a combination of different metrics that evaluate data or ML model quality. 

Уou can display an interactive report inside a Jupyter notebook or export it as an HTML file:

![Data Drift report example](../.gitbook/assets/reports/report_example_data_drift-min.png)

You can also generate the report as a text summary: as a JSON or as a Python dictionary. 

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
Most reports can be calculated for a single dataset. If you pass two datasets, they will show a side-by-side comparison.

You can generate a report by listing individual **Metrics** to include in it. You can also run one of the **Presets** that cover a specific aspect of the model or data performance. 

# What is a Metric?

A **Metric** is a component of a report that evaluates a specific aspect of the data or model quality. 

A **Metric** can be, literally, a single metric (such as an accuracy value). It can also be a combination of metrics, a plot, or a table. Each **Metric** has a visual render.

Some metrics simply return the values:  

![RegressionQualityMetric](../.gitbook/assets/reports/metric_example_regression_quality-min.png)

Others have rich visualizations or plots. Here is an example of a model-related metric:

![RegressionErrorDistribution](../.gitbook/assets/reports/metric_example_error_distribution-min.png)

Here is an example of a data-related metric applied to a single column: 

![ColumnValueRangeMetric](../.gitbook/assets/reports/metric_example_value_range-min.png)

The JSON “version” of a metric returns any new calculated values and, optionally, some other useful information such as histogram bins. 

Evidently contains 30+ **Metrics** related to data quality, integrity, drift and model performance. You can also implement a custom one.

# What is a Metric Preset?

A metric **Preset** is a pre-built report that combines metrics for a particular use case.

You can think of it as a template. For example, there is a preset to check for Data Drift (`DataDriftPreset`), Data Quality (`DataQualityPreset`), or Regression Performance (`RegressionPreset`). 

![ColumnValueRangeMetric](../.gitbook/assets/reports/evidently_reports_min.png)

You can explore all metrics and presets here:

{% content-ref url="../reference/all-metrics.md" %}
[All metrics](all-metrics.md)
{% endcontent-ref %}

# When to use Reports

You can use Reports at different stages of the ML lifecycle: from exploratory data analysis and pre-deployment model evaluation to production monitoring and debugging.  

**Debugging and exploration**. Reports are best for visual analysis of the data or model performance. For example, during model quality evaluation on the training set, when debugging the model quality decay, or comparing two models.

**Metric logging**. You can also add a model or data evaluation step in the ML pipeline, get outputs as JSON, and log it to a database. For example, you can later visualize it using other BI tools.

**Reporting and documentation**. You can also use Evidently reports to share results with the team and stakeholders or log them as documentation. For example, you can record the results of the model performance after training.

# Test Suites or Reports?

**Reports** and **[Test Suites](../tests/overview.md)** are complementary interfaces. 

Test Suites are best for automation and integration in the prediction pipelines. They require defining test conditions (expectations for your data and model performance) upfront or providing a reference dataset to learn from.

Reports are best for visual exploration and ad hoc evaluation, debugging, and reporting. 

# How to get Reports?

Head here for a complete user guide with the code snippets:
 
{% content-ref url="../tests-and-reports/get-reports.md" %}
[Get reports](get-reports.md)
{% endcontent-ref %}
