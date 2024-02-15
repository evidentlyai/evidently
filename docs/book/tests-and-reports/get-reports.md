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

To see in Jupyter notebook or Colab, call the resulting object: 

```python
drift_report
```

You can also export the Report results in different formats in addition to rendering them in the notebook.

**Evidently snapshot**. You can save the output as an Evidently JSON `snapshot`. This will allow you to visualize the model or data quality over time using the Evidently ML monitoring dashboard. This also allows you to load the JSON back to the Python environment after saving to be able to view the Report or export it in another format.

```python
drift_report.save("snapshot.json")
```

{% hint style="info" %}
**Building a live ML monitoring dashboard**. To better understand how the ML monitoring dashboard works, we recommend going through the [ML Monitoring Quickstart](../get-started/tutorial-monitoring.md).
{% endhint %}

**HTML**. You can save the interactive visual report as an HTML, to be able to open it in the browser or share with the team. 

To export HTML as a separate file: 

```python
drift_report.save_html(“file.html”)
```

{% hint style="info" %} 
Reports contain interactive visualizations inside the HTML, so large reports might take time to load. In this case, downsample your data. 
{% endhint %}

**JSON**. You can get the results of the calculation as a JSON with metrics. It is best for automation and integration in your prediction pipelines. 

To get the JSON:

```python
drift_report.json()
```

To export JSON as a separate file: 

```python
drift_report.save_json("file.json")
```

**Python dictionary**. You can get the output in the Python dictionary format. Using a Python object might be more convenient if you want to apply multiple transformations to the output.

To get the dictionary:

```python
drift_report.as_dict()
```

**Pandas dataframe**. You can get the output in tabular format as a dataframe.

You can also export the results for a specific Metric only. 

```python
drift_report.as_dataframe("DataDriftTable")
```

You can also export results for the complete Report. In this case, you get a dictionary of dataframes.

```python
drift_report.as_dataframe()
```

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
