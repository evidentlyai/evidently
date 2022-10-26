---
description: How to generate reports in Evidently.
---

{% hint style="info" %} The Report object unites the functionality of Dashboards and JSON Profiles. It is currently in development. We are migrating the existing tabs and sections to the new API. It will also soon be possible to quickly create custom reports from individual Metrics.{% endhint %} 

{% hint style="info" %} If you have any issues, you can continue using Dashboards and JSON Profiles. However, they will be depreciated in the future.{% endhint %}      

# Installation and prep

After [installation](../get-started/install-evidently.md), import the Report component and the required metrics (available soon) and metric presets:

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

**Example**. To generate the report for Data Drift together with numerical Target Drift:

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
