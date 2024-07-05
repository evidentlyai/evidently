---
description: How Evidently ML Monitoring works.
---   

# How It Works
ML monitoring helps track data and model performance over time, identify issues, and get alerts. 

* **Instrumentation**: You use the open-source Evidently Python library to collect metrics and generate JSON `snapshots` containing data summaries, metrics, and test results.
* **Snapshot Storage**: You save `snapshots` in Evidently Cloud or in a local or remote workspace.
* **Monitoring Service**: You visualize data from `snapshots` on a Dashboard in the Evidently Cloud web app or a self-hosted UI service.

The evaluation functionality relies on the open-source Evidently `Reports` and `Test Suites`. You can use 100+ Metrics and Tests on data quality, data and prediction drift, model quality (classification, regression, ranking, LLMs, NLP models) and add custom metrics.

![](../.gitbook/assets/cloud/cloud_service_overview-min.png)

{% hint style="info" %}
**Data privacy.** By default, Evidently does not store raw data or model inferences. Snapshots contain data aggregates (e.g., distribution summaries) and metadata with test results. This hybrid architecture helps avoid data duplication and preserves its privacy.
{% endhint %}

# Deployment Options

* **Evidently Cloud (Recommended)**: This is the easiest way to start, with UI service and snapshots hosted by Evidently. Evidently Cloud includes support, a scalable backend, and premium features such as built-in alerting, user management, and visual dashboard design. [Sign up](https://www.evidentlyai.com/register) to start free.
* **Self-hosted ML Monitoring**: Best for proof of concept, small-scale deployments, or teams with advanced infrastructure knowledge. In this case, you must host the open-source UI dashboard service and manage the data storage on your own. 
* **Private Enterprise Deployment**: For a scalable self-hosted version of Evidently Platform with support, contact us for a [demo of Evidently Enterprise](https://www.evidentlyai.com/get-demo). The platform be hosted in your private cloud or on-premises.

# Deployment architecture 

You can start by sending snapshots ad hoc. For production monitoring, you can orchestrate batch evaluation jobs or send live data directly from ML services.

## Batch 

You can run monitoring jobs using a Python script or a workflow manager tool like Airflow. 

You can add a monitoring or validation step to an existing batch pipeline. Say, you generate predictions daily:
* on every run, you can capture a data summary snapshot and check for data quality and prediction drift
* once you get the true labels, you can compute the model quality metrics.

![](../.gitbook/assets/monitoring/monitoring_batch_workflow_min.png)

You can also run tests during CI/CD (e.g., after model retraining), and implement automatic actions based on the validation results.

If you store your data (model inference logs) in a data warehouse, you can design separate monitoring jobs. For example, you can set up a script to query the data and compute snapshots on a regular cadence, e.g., hourly, daily, weekly, or after new data or labels are added. 

# Near real-time

If you have a live ML service, you can deploy and configure the **Evidently collector service**. You will then send the incoming data and predictions for near real-time monitoring.

Evidently Collector will manage data batching, compute `Reports` or `Test Suites` based on the configuration, and send them to the Evidently Cloud or to your designated workspace.

![](../.gitbook/assets/monitoring/monitoring_collector_min.png)

If you receive delayed ground truth, you can also later compute and log the model quality to the same Project via a batch workflow. You can run it as a separate process or monitoring job.

![](../.gitbook/assets/monitoring/monitoring_collector_delayed_labels_min.png)

# How to start 

For an end-to-end example, check these tutorials:
* [Evidently Cloud: Data & ML Monitoring](https://docs.evidentlyai.com/get-started/tutorial-cloud)
* [Self-hosting ML Monitoring](https://docs.evidentlyai.com/get-started/tutorial-monitoring)

This user guide explains each step in detail:
* [Set up your Workspace](workspace.md)
* [Create a Project](add_project.md)
* [Log snapshots](snapshots.md) or set up a near real-time [collector service](collector_service.md) 
* [Get a pre-built Dashboard](add_dashboard_tabs.md)
* Understand available [Panel types](design_dashboard.md) and add custom [monitoring Panels](design_dashboard_api.md)
* [Send alerts](alerting.md)
