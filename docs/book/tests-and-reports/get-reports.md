---
description: How to generate reports in Evidently.
---   

TL;DR: You can start with ready-made Metric Presets that work out of the box. 

# Installation and prep

After [installation](../installation/install-evidently.md), import the Report component and the required Metric Presets:

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
```

You need to prepare two datasets for comparison: **reference** and **current**. You can also generate some of the reports with a single current dataset. 

{% hint style="info" %} 
Refer to the [input data](../input-data/data-requirements.md) and [column mapping](../input-data/column-mapping.md) for more details on data preparation.
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
