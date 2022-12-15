
# Custom report

You can create a custom report from individual metrics.

You need to create a `Report` object and list which `metrics` to include.    

## Dataset-level metrics

Some of the metrics are calculated on the dataset level. For example, there is a metric that evaluates data drift for the whole dataset.

To create a custom report with dataset-level metrics:

```python
data_drift_dataset_report = Report(metrics=[
    DatasetDriftMetric(),
    DataDriftTable(),    
])
```

To calculate the metrics and get the visual report:

```python
data_drift_dataset_report.run(reference_data=ref, current_data=cur)
data_drift_dataset_report
```

## Column-level metrics

Some of the metrics are calculated on the column level. For example, to calculate drift in a specific feature or model predictions.

To create a custom report with column-level metrics:

```python
data_drift_column_report = Report(metrics=[
    ColumnDriftMetric('age'),
    ColumnDriftMetric('education'),   
])
```

To calculate the metrics and get the visual report:

```python
data_drift_column_report.run(reference_data=adult_ref, current_data=adult_cur)
data_drift_column_report
```

**Combining tests**. When you define the contents of the Report, you can include metrics presets and individual tests in the same list. You can also combine feature-level and dataset-level metrics. 

## Available metrics

Evidently library has dozens of individual metrics with different visualizations. Here are some examples: 

```python
DatasetSummaryMetric()
DatasetMissingValuesMetric()
DatasetCorrelationsMetric()
DatasetDriftMetric()
DataDriftTable()  
```

{% hint style="info" %} 
**Reference**: The complete list of metrics is available in the [All metrics](../reference/all-metrics.md) table.
{% endhint %}

# Metric parameters

Some metrics include default parameters. For example, probabilistic classification quality metrics have a default 0.5 decision threshold. You can override the defaults by setting custom parameters. 

Some metrics also have required parameters. For example, if you want to calculate the number of values that match a regular expression, you need to specify it. 

**Example 1**. How to specify regular expression (required parameter):

```python
data_integrity_column_report = Report(metrics=[
    ColumnRegExpMetric(column_name="education", reg_exp=r".*-.*", top=5),
    ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*")
])

data_integrity_column_report.run(reference_data=adult_ref, current_data=adult_cur)
data_integrity_column_report
```

**Example 2**. Some custom parameters might be set through the Options object. Here is an example of choosing the custom DataDrift test. 

```python
data_drift_column_report = Report(metrics=[
    ColumnDriftMetric('age'),
    ColumnDriftMetric('age', stattest='psi'),
])
data_drift_column_report.run(reference_data=adult_ref, current_data=adult_cur)

data_drift_column_report
```
{% hint style="info" %} 
**Reference**: The available parameters are listed in the [All metrics](../reference/all-metrics.md) table.
{% endhint %}
