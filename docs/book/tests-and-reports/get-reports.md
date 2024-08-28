---
description: How to generate Reports using Evidently Python library.
---   

# Code examples

To see code examples with generating Reports, check the sample notebooks in [Examples](../examples/examples.md).

# Imports

After [installing Evidently](../installation/install-evidently.md), import the `Report` component and the necessary `metric_presets` or `metrics` you plan to use:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import *
```

# How it works

Here is the general flow.
* **Input data**. Prepare data as a Pandas DataFrame. This will be your `current` data to run evaluations for. For some checks, you may need a second `reference` dataset. Check the [input data requirements](../input-data/data-requirements.md).
* **Schema mapping**. Optionally, define your data schema using [Column Mapping](../input-data/column-mapping.md).
* **Define the Report**. Create a `Report` object and include the selected Metrics or Preset in the `metrics` list.
* **Run the Report**. Run the Report on your `current_data`. If applicable, pass the `reference_data` and `column_mapping`.
* **Get the results**. Get a visual Report in Jupyter notebook, export the metrics, or upload it to Evidently Platform.

You can use Metric Presets, which are pre-built Reports that work out of the box, or create a custom Report selecting Metrics one by one.

# Metric Presets 

To generate a Report using Metric Preset, simply include the selected Metric Preset in the `metrics` list.

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
**Available Presets**. There are other Presets: for example, `DataDriftPreset`, `RegressionPreset` and `ClassificationPreset`. Refer to the [Presets overview](../presets/all-presets.md) to understand individual Presets, and to [All metrics](../reference/all-metrics.md) to see all available options. 
{% endhint %}

**Example 2**. You can include multiple Presets in a Report. To combine Data Drift and Data Quality and run them over two datasets, including a reference dataset necessary for data drift evaluation:

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

**Example 4**. You can customize some of the Metrics inside the Preset by passing parameters to it. For example, calculate quality metrics for a binary probabilistic classification model with a custom decision threshold instead of default 0.5:

```python
dataset_report = Report(metrics=[
    ClassificationPreset(probas_threshold=0.7),
])
```

**Example 5**. You can pass a list of columns to the Preset, so column-specific Metrics are generated only for those columns, not the entire dataset.

```python
drift_report = Report(metrics=[
    DataDriftPreset(columns=["age", "position"]),
])
```

{% hint style="info" %} 
Refer to the [All metrics](../reference/all-metrics.md) table to see defaults and available parameters that you can pass for each Preset.
{% endhint %}

# Get a custom Report

While Presets are a great starting point, you may want to customize the Report by choosing Metrics or adjusting their parameters even more. To do this, create a custom Report using individual Metrics.

## 1. Choose metrics

First, define which Metrics you want to include in your custom Report. Metrics can be either dataset-level or column-level.

{% hint style="info" %} 
**List of available Metrics**: The complete list of Metrics is available in the [All metrics](../reference/all-metrics.md) table. To see interactive examples, check the [Example notebooks](../examples/examples.md).
{% endhint %}

{% hint style="info" %} 
**Row-level evaluations**: If you want to generate scores on the row-level, which is often relevant for text data where you score individual texts, read more about [Text Descriptors](text-descriptors.md.md).
{% endhint %}

**Dataset-level metrics**. Some Metrics evaluate the entire dataset. For example, a Metric that checks for data drift across the whole dataset or calculates accuracy.

To create a custom Report with dataset-level metrics, create a `Report` object and list the `metrics` one by one:    

```python
data_drift_dataset_report = Report(metrics=[
    DatasetDriftMetric(),
    DataseSummaryMetric(),  
])
```

**Column-level Metrics**. Some Metrics focus on individual columns, like evaluating distribution drift or summarizing specific columns. To include column-level Metrics, you must pass the name of the column to each such Metric:

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

Metrics can have optional or required parameters. For example, the data drift detection algorithm selects a method automatically, but you can override this by specifying your preferred method (Optional). To calculate the number of values matching a regular expression, you must always define this expression (Required).

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
