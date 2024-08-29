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

## Batch 

You can run monitoring jobs using a Python script or a workflow manager tool like Airflow. 

You can add a monitoring or validation step to an existing batch pipeline. Say, you generate predictions daily:
* on every run, you can capture a data summary snapshot and check for data quality and prediction drift
* once you get the true labels, you can compute the model quality metrics.

![](../.gitbook/assets/monitoring/monitoring_batch_workflow_min.png)

You can also run tests during CI/CD (e.g., after model retraining), and implement automatic actions based on the validation results.

If you store your data (model inference logs) in a data warehouse, you can design separate monitoring jobs. For example, you can set up a script to query the data and compute snapshots on a regular cadence, e.g., hourly, daily, weekly, or after new data or labels are added. 


