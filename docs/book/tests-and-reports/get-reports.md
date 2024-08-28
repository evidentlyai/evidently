---
description: How to use Metric Presets in Evidently.
---   

**TL;DR:** Evidently has pre-built Reports that work out of the box. To use them, simply pass your data and choose the Preset. 

# Installation and prep

After [installation](../installation/install-evidently.md), import the `Report` component and the required `metric_presets`:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset
```

You need two datasets for comparison: **reference** and **current**. You can also generate some of the Reports with a single dataset. 

{% hint style="info" %} 
Refer to the [input data](../input-data/data-requirements.md) and [column mapping](../input-data/column-mapping.md) for more details on data preparation.
{% endhint %}

# Using metric presets 

Evidently has ready-made **Metric Presets** that group relevant Metrics in a single Report. You can use them as templates to evaluate a specific aspect of the data or model performance.

To use the Preset, create a `Report` object and specify the chosen `preset` in a list of `metrics`. You should also point to the current and reference dataset (if available). If nothing else is specified, the Report will run with the default parameters for all columns in the dataset.

**Example 1**. To generate the Report that includes two Presets for Data and Target Drift:

```python
drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
 
drift_report.run(reference_data=reference, current_data=current)
drift_report
```
 
It will display the HTML combined report. 

**Example 2**. To generate the Report for a single dataset:

```python
data_quality_report = Report(metrics=[
    DataQualityPreset()
])

data_quality_report.run(current_data=current, reference_data = None, column_mapping=None)
data_quality_report
```

**Aggregated visuals in plots.** Starting from v 0.3.2, all visuals in the Evidently Reports are aggregated by default. This helps decrease the load time and report size for larger datasets. If you work with smaller datasets or samples, you can pass an [option to generate plots with raw data](../customization/report-data-aggregation.md). You can choose whether you want it on not based on the size of your dataset.

# Available presets

Here is a list of Metric Presets you can try:

```python
DataQualityPreset
DataDriftPreset
TargetDriftPreset 
RegressionPreset
ClassificationPreset
```

{% hint style="info" %} 
Refer to the [Presets overview](../presets/all-presets.md) to understand when to use each Preset. Refer to the [example notebooks](../examples/examples.md) to see interactive examples.
{% endhint %}

# Output formats 

To see the visual Report in Jupyter notebook or Colab, call the resulting object: 

```python
drift_report
```

To get a text summary, use a Python dictionary.

```python
drift_report.as_dict()
```

{% hint style="info" %} 
***There are more output formats!**. You can also export and save Report results in different formats: HTML, JSON, dataframe, etc. Refer to the [Output Formats](output_formats.md) for details.
{% endhint %}

# Preset parameters 

You can customize some of the Presets using parameters. For example, you can calculate the quality metrics for a binary probabilistic classification model with a custom decision threshold:

```python
dataset_report = Report(metrics=[
    ClassificationQualityMetric(probas_threshold=0.5),
])
```
{% hint style="info" %} 
Refer to the [All metrics](../reference/all-metrics.md) table to see available parameters that you can pass for each preset.
{% endhint %}

If you want to change the composition of the Report or pass additional parameters, you can [create a custom report](custom-report.md).

# Create a custom Report

You can create a custom report from individual Metrics available in the library.  

## 1. Choose metrics

To design a custom report, you should first define which metrics you want to include. 

You can use Metric Presets as a starting point to explore types of analysis available in the library. Note that there are additional metrics that are not included in the presets that you can choose from. 

{% hint style="info" %} 
**Reference**: The complete list of metrics is available in the [All metrics](../reference/all-metrics.md) table. To see interactive examples, refer to the [Example notebooks](../examples/examples.md).
{% endhint %}

### Dataset-level metrics

Some of the metrics are calculated on the dataset level. For example, there is a metric that evaluates data drift for the whole dataset.

To create a custom report with dataset-level metrics, you need to create a `Report` object and list the `metrics`:    

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

### Column-level metrics

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

**Combining metrics and presets**. When you define the composition of the Report, you can include metrics presets and individual tests in the same list. You can also combine feature-level and dataset-level metrics. 

```python
my_report = Report(metrics=[
    DataQualityPreset(),
    DatasetDriftMetric(),
    ColumnDriftMetric('age'),
])
```

## 2. Set metric parameters

Some metrics include default parameters. For example, probabilistic classification quality metrics have a default 0.5 decision threshold. You can override the defaults by setting custom parameters. 

Some metrics have required parameters. For example, if you want to calculate the number of values that match a regular expression, you need to specify it. 

**Example 1**. How to specify regular expression (required parameter):

```python
data_integrity_column_report = Report(metrics=[
    ColumnRegExpMetric(column_name="education", reg_exp=r".*-.*", top=5),
    ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*")
])

data_integrity_column_report.run(reference_data=adult_ref, current_data=adult_cur)
data_integrity_column_report
```

**Example 2**. How to specify a custom DataDrift test (optional parameter). 

```python
data_drift_column_report = Report(metrics=[
    ColumnDriftMetric('age'),
    ColumnDriftMetric('age', stattest='psi'),
])
data_drift_column_report.run(reference_data=adult_ref, current_data=adult_cur)

data_drift_column_report
```

{% hint style="info" %} 
**Reference**: The available parameters for each metric are listed in the [All metrics](../reference/all-metrics.md) table.
{% endhint %}

