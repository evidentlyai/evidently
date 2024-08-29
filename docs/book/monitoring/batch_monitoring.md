---
description: How to run batch monitoring workflows.
---   

For an overview of monitoring architectures, read the [introduction](monitoring_overview.md).

In a batch monitoring workflow, you regularly run evaluation jobs and log the results to the Evidently Platform for ongoing monitoring.

# Code example

Check the tutorials:

{% content-ref url="../examples/tutorial-monitoring.md" %}
[Data and ML monitoring](../examples/tutorial-monitoring.md)
{% endcontent-ref %}

{% content-ref url="../examples/tutorial-monitoring.md" %}
[LLM evaluations and monitoring](../examples/tutorial-llm.md)
{% endcontent-ref %}

# How it works
Here’s a general overview of how batch monitoring works:

**Create a monitoring [Project](../projects/add_project.md)**. This will organize all your data and evaluation results in one place.

**Configure evaluations**. Decide which [Reports and Test Suites](../tests-and-reports/overview.md) you want to run at regular intervals. These could focus on data quality, data drift, model performance, or LLM output quality.
 
**Design monitoring jobs**. Set up jobs to run evaluations at specific points in your prediction pipeline or by querying your prediction database. These jobs will generate JSON snapshots (special versions of Evidently Reports or Test Suites) to upload to the platform.

Essentially, you're setting up a routine process to run the same evaluation jobs you might run manually during experimentation but now automating them for regular monitoring.

Learn how to generate snapshots:

{% content-ref url="../evaluations/snapshots.md" %}
[Generate snapshots](../evaluations/snapshots.md)
{% endcontent-ref %}

{% hint style="info" %}
**Example**: in a daily scoring pipeline, you could add validation steps to check input data quality and prediction drift. Use the `DataStabilityTestPreset` and `DataDriftTestPreset`, or your selected combination of Metrics or Tests. Another job could compute model quality metrics once the true labels are available, using something like `BinaryClassificationTestPreset`. You can run these jobs via a Python script or manage them using workflow tools like Airflow.
{% endhint %}

## Batch 

You can run monitoring jobs using a Python script or a workflow manager tool like Airflow. 

You can add a monitoring or validation step to an existing batch pipeline. Say, you generate predictions daily:
* on every run, you can capture a data summary snapshot and check for data quality and prediction drift
* once you get the true labels, you can compute the model quality metrics.

![](../.gitbook/assets/monitoring/monitoring_batch_workflow_min.png)

You can also run tests during CI/CD (e.g., after model retraining), and implement automatic actions based on the validation results.

If you store your data (model inference logs) in a data warehouse, you can design separate monitoring jobs. For example, you can set up a script to query the data and compute snapshots on a regular cadence, e.g., hourly, daily, weekly, or after new data or labels are added. 


