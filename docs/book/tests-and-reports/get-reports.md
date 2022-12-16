---
description: How to use Metric Presets in Evidently.
---   

**TL;DR:** Evidently has pre-built Reports that work out of the box. To use them, simply pass your data and choose the Preset. 

# Installation and prep

After [installation](../installation/install-evidently.md), import the `Report` component and the required `metric_presets`:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
```

You need to prepare two datasets for comparison: **reference** and **current**. You can also generate some of the Reports with a single dataset. 

{% hint style="info" %} 
Refer to the [input data](../input-data/data-requirements.md) and [column mapping](../input-data/column-mapping.md) for more details on data preparation.
{% endhint %}

# Using metric presets 

Evidently has ready-made `metric_presets` that group relevant `metrics` in a single Report. You can use them as templates to evaluate a specific aspect of the data or model performance.

To use the Preset, create a `Report` object and specify the chosen `preset` in a list of `metrics`. You should also point to the current dataset and reference dataset (if available). If nothing else is specified, the Report will run with the default parameters.

**Example**. To generate the Report that includes two Presets for Data and Target Drift:

```python
drift_report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
 
drift_report.run(reference_data=reference, current_data=current)
drift_report
```
 
It will display the HTML combined report. 

# Available presets

Here is a list of metric presets you can try:

```python
DataQualityPreset
DataDriftPreset
TargetDriftPreset 
RegressionPreset
ClassificationPreset
```

{% hint style="info" %} 
Refer to the [presets overview](../presets/all-presets.md) to understand when to use each preset. Refer to the [example notebooks](../examples/examples.md) to see interactive examples.
{% endhint %}

# Output formats 

You can get the Report results in different formats. 

**HTML**. You can get an interactive visual report. It is best for exploration and debugging. You can also document the results and share them with the team. 

To see in Jupyter notebook or Colab, call the object: 

```python
drift_report
```

To export HTML as a separate file: 

```python
drift_report.save_html(“file.html”)
```

{% hint style="info" %} 
Reports contain interactive visualizations inside the HTML, so large reports might take time to load. In this case, downsample your data. 
{% endhint %}

**JSON**. You can get the results of the calculation as a JSON. It is best for automation and integration in your prediction pipelines. 

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
