---
description: How to generate and use Evidently snapshots.
---   

To visualize data in the Evidently ML monitoring interface, you must capture data and model metrics as Evidently JSON `snapshots`. 

# What is snapshot?

JSON `snapshots` power the backend of the Evidently ML monitoring.

Each `snapshot` summarizes the data and model performance for a specific period. You can think of a `snapshot` as a singular "log" in the Evidently universe. You can flexibly define which metrics and tests to log as part of the `snapshot`.

{% hint style="info" %}
**Snapshots vs. Reports.** The snapshot functionality is directly based on the Evidently Reports and Test Suites. Put simply, a snapshot is a JSON "version" of the Evidently Report or Test Suite. After you generate the Report or Test Suite and save it as a snapshot, you can load it back and restore it as in the HTML or other formats.
{% endhint %}

To enable monitoring, you must compute multiple `snapshots` over time. For example, you can capture daily or weekly `snapshots` and log them to a specific directory.

You can capture `snapshots` at different stages of a pipeline. For example, when the data arrives, when you generate predictions, when you get the labels, etc. 

You can capture `snapshots` in near real-time, asynchronous batch jobs, or both. You can also compute `snapshots` for past periods and have multiple `snapshots` related to the same period.

To be able to launch a Monitoring UI over the logged `snapshots`, you must store the related `snapshots` (e.g., for the same ML model) in the same directory.

# Generate snapshots

This section explains how to generate and work with individual `snapshots`. 

To simplify organizing multiple `snapshots` relating to a specific model over time, you should first create a `workspace`, as explained in the previous [section of the docs](workspace_project.md).

## Code example

This notebook shows how to save and load individual JSON snapshots:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_snapshots.ipynb" %}

## Create a Report or Test Suite

To generate a snapshot, you must first create an Evidently Test Suite or a Report object. Follow the usual Test Suite and Report API:
* List `metrics`, `tests` or `presets` to include.
* Pass the `current` and optional `reference` dataset. 
* Pass optional `column_mapping`.

**Example 1**. You can pass the `current` data batch and generate a `snapshot` with descriptive statistics of the dataset:

```python
data_summary_report = Report(metrics=[
   DatasetSummaryMetric(),
])
data_summary_report.run(reference_data=None, current_data=batch1)
```

{% hint style="info" %}
**What is a Report or a Test Suite?** If you are new to Evidently, go through the Test and Reports [QuickStart Tutorial](https://docs.evidentlyai.com/get-started/tutorial). 
{% endhint %}

**Reference dataset.** Some metrics, like data drift, require `reference` data. For example, to compare this week's data distribution to the previous, you must pass the reference dataset for the past week. You can also choose to pass the `reference` to derive test conditions automatically. For example, to compare the column types to the column types in the reference dataset.

**Example 2**. Here is how you create a Test Suite, passing both `current` and `reference` datasets:

```python
data_drift_checks = TestSuite(metrics=[
   DataDriftTestPreset(),
])
data_drift_checks.run(reference_data=reference_batch, current_data=batch1)
```

{% hint style="info" %}
**What other Metrics and Tests are there?** Browse the complete list of [Presets](../presets/all-presets.md), [Metrics](../reference/all-metrics.md) and [Tests](../reference/all-tests.md) to see what you can log as `snapshots`.
{% endhint %}

## Save the snapshot

After creating a Report or a Test Suite, you must use the `save()` method to create a `snapshot`. Specify the path where to save it:

```python
data_drift_checks.save("data_drift_snapshot.json")
```

{% hint style="info" %}
**Snapshots vs. JSON export.** This `save()` function is different from using `json()` or `save_json("file.json")` function for Evidently Reports or Test Suites. The usual JSON export returns a structured output with limited information. You cannot convert this JSON back to an HTML. A `snapshot` contains more data: you can use it to restore an HTML (or other formats) without accessing the initial raw data.
{% endhint %}

To load the snapshot back, you can use the `load()` function.

```python
restored_report = Report.load("data_drift_snapshot.json")
restored_report
```

This way, you load the snapshot file and restore the visual Report or Test Suite. You can also export them as HTML files, JSON, or a Python dictionary.
 
**Note**: This step is not required for monitoring. You can use it to visualize and explore individual snapshots in the notebook environment: for example, if you want to look at the daily data statistics outside the monitoring UI. 

## Add timestamp

We recommend adding a `timestamp` to the Report or Test Suite that you log as snapshots. Each snapshot has one timestamp.

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	timestamp=datetime.now(),
)
```

If you do not pass a timestamp, Evidently will assign the `datetime.now()` timestamp with the Report/Test Suite computation time based on the user time zone.

**Note**: even if the dataset you use to generate the snapshot contains a DateTime column, Evidently will not use it automatically. You can manually specify, for example, that the snapshot timestamp should match the last value of the DateTime column in the dataset you pass.

**Example**. If you want to assign the last available date from the DateTime index as a timestamp for your snapshot:

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	timestamp=dataset.iloc[-1:].index,
)
```

Since you can assign arbitrary timestamps, you can log snapshots asynchronously or with a delay (for example, when you receive ground truth).

## Add tags 

You can add optional `tags` and `metadata` to the snapshots. This will allow you to group and filter related `snapshots` when you define which values to display on a specific panel of the monitoring dashboard. 

Here are some example use cases when you might want to use tags:
* To tag models deployed in a shadow mode
* To tag champion/challenger model
* To tag groups of snapshots that use different reference datasets (for example, as you compare distribution drift week-by-week and month-by-month)
* To tag training dataset, etc.

**Example 1**. You can pass a set of custom tags as a list: 

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	tags=[groupA, shadow],
)
```

**Example 2**. You can also pass metadata as a Python dictionary in key:value pairs:

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric(),
	],
	metadata = {
	"deployment": "shadow",
	"status": "production",
	}
)
```

**Example 3**. You can also use in-built metadata fields `model_id`, `reference_id`, `batch_size`, `dataset_id`:

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric(),
	],
	model_id=model_id,
	reference_id=reference_id,
	batch_size=batch_size,
	dataset_id=dataset_id,
)
```

All `tags` and `metadata` fields are optional and added for convenience. 

**Example 4**. You can also add `tags` later to an existing Report or Test Suite:

```python
data_summary_report.tags=["training_data"]
```
