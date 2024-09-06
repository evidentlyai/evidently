---
description: How to run evals in Python and upload to Evidently Platform.
---   

This page walks you through how to run evaluations locally in Python and send the results to Evidently Platform. This applies both to on-the-fly evaluations during experiments and to those you run automatically during batch monitoring or regression testing.

Once you upload the evaluation results as JSON `snapshots`, you can explore, compare, and track them on the Evidently Platform.

# What is snapshot?

A `snapshot` is a JSON summary containing evaluation results. It captures the data and AI system performance for the specific dataset or data batch you evaluated. Snapshots can include metrics, test results, column summaries, and additional render data. You choose what to include when running your evaluation.

The snapshot functionality is based on Evidently [Reports and Test Suites](../tests-and-reports/overview.md). Put simply, a snapshot is a JSON "version" of an Evidently Report or Test Suite.

When you run individual evaluations, you can explore and compare their results. As you send multiple snapshots to a Project, you can also use a Dashboard to track results over time. This helps you monitor metric changes across experiments or track evaluations on production data. 

You can optionally include the Dataset together with the evaluation results you upload.

# How it works

Here is the general workflow.

**1. Create or connect to a [Project](../projects/add_project.md)** in your Workspace where you want to send the snapshots. This will organize all your evaluations in one place.

```python
project = ws.get_project("PROJECT_ID")
```
**2. Prepare the data**. You run each evaluation on a Dataset. 

You can prep your input data locally as a Pandas DataFrame or first upload it to the Evidently Platform and call it from there.

{% hint style="info" %}
**Working with data**. Check how to prepare your [input data](../input-data/data-requirements.md) or upload and manage [Datasets](../datasets/datasets_overview.md).
{% endhint %}

**3. Define the snapshot compostion**. Define what you want to evaluate.

* Create a `Report` or `Test Suite` object.
* Pass the chosen `metrics` or `tests`.
* Optionally, pass custom parameters for Metric calculations and/or Test conditions.

{% hint style="info" %}
**Reports and Tests**. Check how to get [Reports](../tests-and-reports/get-reports.md), run [Test Suites](../tests-and-reports/run-tests.md) or generate [Text Descriptors](../tests-and-reports/text-descriptors.md).
{% endhint %}

**4. Run the Report or Test Suite**. Execute the evaluation on your dataset.

* Pass the `current` dataset you want to evaluate or profile.
* Optional (but highly recommended): pass the `column_mapping` to define the data schema. 
* Optional (required for data distribution checks): pass the `reference` dataset.
* Optional: add a `tags` or `metadata` to identify this specific evaluation run.
* Optional: and a custom `timestamp` to the current run. 

**5. Send the snapshot**. 

After you compute the Report or Test Suite, use the `add_report` or `add_test_suite` methods to send them to a corresponding Project in your workspace.

# Examples

## Send snapshots

**Report**. To create and send a Report with data summaries for a single dataset `batch1` to the workspace `ws`:

```python
data_report = Report(
      metrics=[
          DataQualityPreset(),
      ],
   )
data_report.run(reference_data=None, current_data=batch1)
ws.add_report(project.id, data_report)
```

**Test Suite**. To create and send a Test Suite with data drift checks, passing current and reference data:

```python
drift_checks = TestSuite(tests=[
  DataDriftTestPreset(),
])
drift_checks.run(reference_data=reference_batch, current_data=batch1)
ws.add_test_suite(project.id, drift_checks)
```

**Send a snapshot**. The `add_report` or `add_test_suite` methods generate snapshots automatically. If you already have a snapshot (e.g., you previously saved it), you can load it load and send it to your Project:

```python
ws.add_snapshot(project.id, snapshot.load("data_drift_snapshot.json"))
```

{% hint style="info" %}
**Snapshot size**. A single upload to Evidently Cloud should not exceed 50MB (Free plan) or 500MB (Pro plan). This limitation applies to the size of the JSON, not the dataset itself. Example: a data drift report for 50 columns and 10,000 rows of current and reference data results in a snapshot of approximately 1MB. (For 100 columns x 10,000 rows: ~ 3.5MB; for 100 columns x 100,000 rows: ~ 9MB). The size varies depending on the metrics or tests used.
{% endhint %}

## Add dataset 

When you upload a Report or Test Suite, you can optionally include the Dataset you evaluated, together with added Descriptors (if any). This helps with row-level debugging and analysis.

Use the `include_data` parameters (defaults to False):

```python
ws.add_report(project.id, data_report, include_data=True)
```

## Add timestamp

Each `snapshot` is associated with a single timestamp. By default, Evidently will assign the `datetime.now()` using the Report/Test Suite computation time based on the user time zone.

You can also add your own timestamp. Pass it to the run method when you compute the snapshot: 

```python
drift_checks.run(
    reference_data=reference_batch,
    current_data=batch1,
    timestamp=datetime.now()
)
```

Since you can assign arbitrary timestamps, you can log snapshots asynchronously or with a delay (for example, after you receive ground truth) and assign it to the specific period.

## Add tags and metadata

You can include `tags` and `metadata` in snapshots. This is useful for search and data filtering. By adding **Tags**, you can then visualize data only from a specific subset of your snapshots on a monitoring Panel.

Examples of when to use tags include:
* You want to identify a specific evaluation run or group of experiments by model version or test scenario.
* You are logging data on production/shadow, champion/challenger, or A/B model versions.
* You compute snapshots with different reference datasets (for example, to compare distribution drift week-by-week and month-by-month).
* You have data for multiple models of the same type inside a Project.
* You capture snapshots for multiple segments in your data.
* You want to tag individual Reports, e.g., a datasheet card, a model card, etc.

**Custom tags**. Pass any custom Tags as a list: 

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

**Default metadata**. Use built-in metadata fields `model_id`, `reference_id`, `batch_size`, `dataset_id`:

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

**Add Tags to existing Reports.**. You can add Tags to a previously generated Report or Test Suite:

```python
data_summary_report.tags=["training_data"]
```

# Delete snapshots

To delete snapshots in the Workspace `ws`, pass the Project ID and snapshot ID. You can see the snapshot ID on the Report or Test Suite page.

```python
ws.delete_snapshot(project_id, snapshot_id)
```

# What's next?

Once you've sent data to the Project, you can [add monitoring Panels and Tabs](../dashboard/design_dashboard.md).
