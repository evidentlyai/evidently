---
description: How to send snapshots for data and ML monitoring.
---   

To visualize data in the Evidently ML monitoring interface, you must capture data and model metrics as Evidently JSON `snapshots`. 

# What is snapshot?

Evidently `snapshot` is a JSON file summarizing data and model performance for a specific period. Each snapshot includes metrics, data summaries, test results, and supporting render data. You choose which metrics to include when creating a snapshot.

Snapshots power the backend of Evidently ML monitoring. By sending multiple snapshots to the Project (e.g., hourly, daily, or weekly), you create a data source for monitoring panels. You can plot metrics and trends over time from multiple snapshots and view individual ones for each period.

You can:
* Send the snapshots sequentially on a schedule (e.g., send a data summary every hour or every day).
* Send one-off snapshots after specific evaluations (e.g., send results of CI/CD checks).
* Backdate your snapshots (e.g., to log model quality after you get the labels).
* Log multiple snapshots for the same period (e.g., for shadow and production models).

{% hint style="info" %}
**Snapshots vs. Reports.** The snapshot functionality is directly based on the Evidently Reports and Test Suites. Put simply, a snapshot is a JSON "version" of the Evidently Report or Test Suite. 
{% endhint %}

# How it works

Here is the general workflow.

**1. Connect to a Project**. Connect to a [Project](add_project.md) in your workspace where you want to send the snapshots.

```python
project = ws.get_project("PROJECT_ID")
```

**2. Define and compute a snapshot**. Define an Evidently Test Suite or Report as usual:
* Create a `Report` or `Test Suite` object. Define the `metrics` or `tests`.
* Pass the `current` dataset you want to evaluate or profile.
* Optional: pass the `column_mapping` to define the data schema. (Required for model quality or text data checks to map target, prediction, text columns, etc.).
* Optional: pass the `reference` dataset. (Required for drift data drift checks).
* Optional: pass parameters for metric calculations and/or test conditions.

For monitoring, you can also add `tags` and `timestamp` to your snapshots. 

{% hint style="info" %}
**New to Evidently?** Check the [Reports and Test Suites tutorial](../get-started/tutorial.md)) and a related [docs section](../tests-and-reports/) for end-to-end examples.  Browse [Presets](../presets/all-presets.md), [Metrics](../reference/all-metrics.md) and [Tests](../reference/all-tests.md) to see available checks.
{% endhint %}

3. **Send the snapshot**. After you compute the Report or Test Suite, use the `add_report` or `add_test_suite` methods to send them to a corresponding Project in your workspace.

# Send snapshots

**Send a Report**. To create and send a Report with data summaries for a single dataset `batch1`:

```python
data_report = Report(
      metrics=[
          DataQualityPreset(),
      ],
   )
data_report.run(reference_data=None, current_data=batch1)
ws.add_report(project.id, data_report)
```

**Send a Test Suite**. To create and send Test Suite with data drift checks, passing both current and reference datasets:

```python
drift_checks = TestSuite(tests=[
  DataDriftTestPreset(),
])
drift_checks.run(reference_data=reference_batch, current_data=batch1)
ws.add_test_suite(project.id, drift_checks)
```

**Send a snapshot**. The `add_report` or `add_test_suite` methods generate snapshots automatically. But if you already have a snapshot (e.g., a previously saved Report), you can load it into Python and send it to your workspace:

```
ws.add_snapshot(project.id, snapshot.load("data_drift_snapshot.json"))
```

{% hint style="info" %}
**Snapshot size**. Ensure that a single upload to Evidently Cloud does not exceed 50 GB for free trial users or 500 GB for users on the Pro plan. Note that this limitation applies to the size of the resulting JSON, not the dataset itself. For example, a data drift report for 50 columns and 10,000 rows of current and reference data results in a snapshot of approximately 1MB. (For 100 columns x 10,000 rows: ~ 3.5MB; for 100 columns x 100,000 rows: ~ 9MB). However, the size varies depending on the metrics or tests used.
{% endhint %}

## Add timestamp

Each `snapshot` is associated with a single timestamp. By default, Evidently will assign the `datetime.now()` timestamp using the Report/Test Suite computation time based on the user time zone.

You can also add your own timestamp: 

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	timestamp=datetime.now(),
)
```

Evidently won't automatically use DateTime columns from your data. You can manually specify the snapshot timestamp to match the last value of the DateTime column in your dataset:

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	timestamp=dataset.iloc[-1:].index,
)
```

Since you can assign arbitrary timestamps, you can log snapshots asynchronously or with a delay (for example, when you receive ground truth).

## Add tags and metadata

You can include `tags` and `metadata` in snapshots. This is optional but useful for search and data filtering.

Examples of when to use tags include:
* You have production/shadow or champion/challenger models and want to visualize them separately on a dashboard.
* You compute snapshots with different reference datasets (for example, to compare distribution drift week-by-week and month-by-month).
* You have multiple models of the same type inside a Project.
* You capture snapshots for multiple segments in your data.
* You want to tag specific individual Reports in a Project, such as a datasheet card for the training dataset, a model card, etc.

**Custom tags**. Pass any custom tags as a list: 

```python
data_drift_report = Report(
	metrics=[
	DatasetSummaryMetric().
	],
	tags=["groupA", "shadow"],
)
```

**Custom metadata**. Pass metadata as a Python dictionary in key:value pairs:

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

**Default metadata**. You can also use built-in metadata fields `model_id`, `reference_id`, `batch_size`, `dataset_id`:

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

**Add tags to existing Reports.**. You can also add tags to a previously generated Report or Test Suite:

```python
data_summary_report.tags=["training_data"]
```

# What's next?

Now that you've sent data to the Project, you can design monitoring panels. Check the next [section](design_dashboard.md.md) to learn more.
{% endhint %}


