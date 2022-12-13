---
description: How to generate reports in Evidently.
---   

TL;DR: You can start with ready-made Metric Presets. You can also create custom Reports from individual Metrics. 

# Installation and prep

After [installation](../get-started/install-evidently.md), import the Report component and the required Metrics and Metric Presets:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
```

You need to prepare two datasets for comparison: **reference** and **current**. You can also generate some of the reports with a single current dataset. 

{% hint style="info" %} 
Refer to the [input data](input-data.md) and [column mapping](column-mapping.md) for more details on data preparation and requirements.
{% endhint %}

# Metric presets 

Evidently has ready-made `metric_presets` that group relevant metrics together in a single Report. You can use them as templates to evaluate a specific aspect of the data or model performance.

You need to create a `report` object and specify the preset to generate. You should also point to the current dataset and reference dataset (if available).

If nothing else is specified, the reports will run with the default parameters.

## How to run metric presets

**Example**. To generate the report for Data Drift together with Target Drift:

```python
drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
 
drift_report.run(reference_data=reference, current_data=current)
drift_report
```
 
It will display the HTML combined report. 

## Available presets

Here is a list of metric presets you can try:

```python
DataQualityPreset
DataDriftPreset
TargetDriftPreset 
RegressionPreset
ClassificationPreset
```

## Output formats 

You can get the test results in different formats. 

**HTML**. You can get an interactive visual report. It is best for exploration and debugging. You can also document еру results and share them with the team. 

To see in Jupyter notebook or Colab, call the object: 

```python
drift_report
```

To export HTML as a separate file: 

```python
drift_report.save_html(“file.html”)
```

**JSON**. You can get the results of the calculation as a JSON. It is best for test automation and integration in your prediction pipelines. 

To get the JSON:

```python
drift_report.json()
```

To export JSON as a separate file: 

```python
drift_report.save_json(“file.json”)
```

**Python dictionary**. You can get the output in the Python dictionary format. Using a Python object might be more convenient if you want to apply multiple transformations to the output.

To get the dictionary:

```python
drift_report.as_dict()
```

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
