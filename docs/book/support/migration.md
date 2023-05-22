---
description: How to migrate to the new Evidently API.
---

# What changed

Starting from Evidently 0.1.59, the old API that uses `Dashboards` and `json profiles` was deprecated. This functionality is now available using the `Report` object. 

In Evidently 0.3.0, the old API was removed from the code base.

# If your code breaks

If you get an error `no module named 'evidently.dashboard'`, you might be running the code that uses old API, with a newer Evidently version.

To make sure your existing code that uses `Dashboards` or `json profiles` works, **fix the Evidently version to 0.2.8 or earlier**.

For example, when installing Evidently, specify:

```
!pip install evidently==0.2.8
```

You can continue using the older versions and access old documentation, but they are no longer supported.

# Migrate to the new version

To make use of all the latest Evidently functionality, including Test Suites, data drift detection and evaluations for text data, new Metrics and Presets, parameter customization, etc. you should migrate to the new API. 

To understand the new API, go through the [Getting Started tutorial](../get-started/tutorial.md) or any of the [sample notebooks](../examples/examples.md). 

## Pre-built report example

Here is a quick example of the change. 

Previously, to generate a pre-built Data Drift Report, you had to import a `Dashboard` object and specify the `tab`. For JSON profile, you needed to create a separate object.

Now, both are unified in a single `Report` object, and you include a `preset` instead of a `tab`. Here is how it works for Data Drift report.  

To get a visual HTML report in Jupyter notebook or Colab.

```
data_drift_report = Report(metrics=[
    DataDriftPreset(),
])

data_drift_report.run(reference_data=ref, current_data=cur)
data_drift_report
```

If you want to keep non-aggregated visualization from the earlier Evidently version, set the [corresponding "agg_data" parmeter to False](../customization/report-data-aggregation.md).

To get what was previously as JSON profile (and has now been improved and re-worked!), simply get the Report output as JSON:

```
data_drift_report.json()
```

If you want to include all the render data in the JSON output, use [parameters to include additional information in JSON](../customization/json-dict-output.md).

You can also get the output as a Python dictionary.

```
data_drift_report.as_dict()
```

It works the same for all other pre-built Reports that are availble as presets. Browse the [sample notebooks](../examples/examples.md) to see the code.

## Custom report example

You can already easily create custom Reports by listing individual metrics to include. Here is the example code to generate custom report:

```
data_quality_column_report = Report(metrics=[
    ColumnDistributionMetric(column_name="education"), 
    ColumnQuantileMetric(column_name="education-num", quantile=0.75), 
    ColumnCorrelationsMetric(column_name="education"),
    ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]), 
    ColumnValueRangeMetric(column_name="age", left=10, right=20),
    
])
```

# Help

If you need any help, ask in our [Discord community](https://discord.com/invite/xZjKRaNp8b).
