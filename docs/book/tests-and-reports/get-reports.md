---
description: How to generate Reports using Evidently Python library.
---   

# Code examples

To see code examples with generating Reports, check the [Examples section](../examples/examples.md).

# Imports

After [installing Evidently](../installation/install-evidently.md), import the `Report` component and the necessary `metric_presets` or `metrics` you plan to use:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import *
```

{% hint style="info" %} 
**Data preparation**. Prepare your data as a Pandas DataFrame. For some evaluations, you may use two datasets: `reference` and `current`. Check the [input data requirements](../input-data/data-requirements.md) for details. You may also need to specify the data schema using a [Column Mapping](../input-data/column-mapping.md) object. 
{% endhint %}

# Metric Presets 

Evidently has pre-built Reports that work out of the box. To use them:
* Create a `Report` object and include the selected Metric Preset in the `metrics` list.
* Run the Report on your dataset by passing it as `current_data`. If applicable, also pass `reference_data` and `column_mapping`.
* View the output as a visual Report or export the metrics.

**Example 1**. To generate the Data Quality Report for a single dataset and get the visual output in Jupyter notebook or Colab:

```python
data_quality_report = Report(metrics=[
    DataQualityPreset()
])

data_quality_report.run(current_data=my_dataset,
                        reference_data=None,
                        column_mapping=None)
data_quality_report
```

If nothing else is specified, the Report will run with the default parameters for all columns in the dataset.

{% hint style="info" %} 
**Available Presets**. There are other Presets: for example, `DataDriftPreset`, `RegressionPreset` and `ClassificationPreset`. Refer to the [Presets overview](../presets/all-presets.md) to understand individual Presets, and to [All metrics](../reference/all-metrics.md) to see all available optionse. 
{% endhint %}

**Example 2**. You can list multiple Presets in a Report. To combine Data Drift and Data Quality and run them over two datasets, including a reference dataset necessary for data drift evaluation:

```python
drift_report = Report(metrics=[
     DataDriftPreset(),
     DataQualityPreset()
])
 
drift_report.run(reference_data=my_ref_dataset,
                current_data=my_cur_dataset)
drift_report
```

It will display the combined Report in Jupyter notebook or Colab. 

{% hint style="info" %} 
**Raw data in visuals**. All visuals in Reports are aggregated by default. This helps reduce load time and Report size for larger datasets, even those with millions of rows. If you work with smaller datasets or samples, you can pass an [option to generate plots with raw data](../customization/report-data-aggregation.md).
{% endhint %}

**Example 3**. To export the values computed inside the Report, export it as a Python dictionary.

```python
drift_report.as_dict()
```

{% hint style="info" %} 
**There are more output formats!**. You can also export Report results in different formats like HTML, JSON, dataframe, and more. Refer to the [Output Formats](output_formats.md) for details.
{% endhint %}

**Example 4**. You can customize some of the Presets using parameters. For example, calculate quality metrics for a binary probabilistic classification model with a custom decision threshold:

```python
dataset_report = Report(metrics=[
    ClassificationQualityMetric(probas_threshold=0.7),
])
```
{% hint style="info" %} 
Refer to the [All metrics](../reference/all-metrics.md) table to see available parameters that you can pass for each Preset.
{% endhint %}

# Get a custom Report

While Presets are a great starting point, you may want to customize the Report by choosing Metrics or adjusting their parameters. To do this, create a custom Report using individual Metrics.

## 1. Choose metrics

First, define which Metrics you want to include in your custom Report.

{% hint style="info" %} 
**Reference**: The complete list of Metrics is available in the [All metrics](../reference/all-metrics.md) table. To see interactive examples, check the [Example notebooks](../examples/examples.md).
{% endhint %}

{% hint style="info" %} 
**Row-level evaluations**: If you want to generate scores on the row-level, which is often relevant for text data where you score individual texts, read more about [Text Descriptors](text-descriptors.md.md).
{% endhint %}

Metrics can be either dataset-level or column-level.

**Dataset-level metrics**. Some Metrics evaluate the entire dataset. For example, a Metric that checks for data drift across the whole dataset or calculates accuracy.

To create a custom Report with dataset-level metrics, create a `Report` object and list the `metrics` one by one:    

```python
data_drift_dataset_report = Report(metrics=[
    DatasetDriftMetric(),
    DataseSummaryMetric(),  
])
```

**Column-level Metrics**. Some Metrics focus on individual columns, like evaluating distribution drift or summarizing specific columns. To include column-level Metrics, you must pass the name of the column to each of them:

```python
data_drift_column_report = Report(metrics=[
    ColumnSummaryMetric(column_name="age"),
    ColumnDriftMetric(column_name="age"),   
])
```

{% hint style="info" %} 
**Generating multiple column-level Metrics**: You can use a helper function to easily generate multiple column-level Metrics for a list of columns. See the page on [Metric Generator](test-metric-generator.md).
{% endhint %}

**Combining Metrics and Presets**. You can mix Metrics Presets and individual Metrics in the same Report, and also combine column-level and dataset-level Metrics.

```python
my_report = Report(metrics=[
    DataQualityPreset(),
    DatasetDriftMetric(),
    ColumnDriftMetric(column_name="age"),
])
```

## 2. Set metric parameters

Some Metrics come with default parameters, like the 0.5 decision threshold for probabilistic classification quality metrics. You can override these defaults by setting custom parameters.

Some Metrics have required parameters. For example, if you want to calculate the number of values that match a regular expression, you need to specify it. 

**Example 1**. How to specify a regular expression (required parameter):

```python
data_integrity_column_report = Report(metrics=[
    ColumnRegExpMetric(column_name="education", reg_exp=r".*-.*", top=5),
    ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*")
])

data_integrity_column_report.run(reference_data=adult_ref, current_data=adult_cur)
data_integrity_column_report
```

**Example 2**. How to specify a custom Data Drift test (optional parameter). 

```python
data_drift_column_report = Report(metrics=[
    ColumnDriftMetric('age'),
    ColumnDriftMetric('age', stattest='psi'),
])
data_drift_column_report.run(reference_data=adult_ref, current_data=adult_cur)

data_drift_column_report
```

{% hint style="info" %} 
**Reference**: The available parameters for each Metric are listed in the [All metrics](../reference/all-metrics.md) table.
{% endhint %}
