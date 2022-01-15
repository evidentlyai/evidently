---
description: Run model evaluation or data drift analysis as a batch job.
---

# Evidently + Airflow

Apache Airflow is an open-source [workflow management tool](https://airflow.apache.org).&#x20;

You can use it to schedule Evidently HTML reports and JSON profiles as a step in the Airflow DAG.

**An integration example is available as a Docker container:**

{% embed url="https://github.com/evidentlyai/evidently/tree/main/evidently/tutorials/airflow_drift_detection" %}

Follow the readme to install and modify the example.&#x20;

It contains two specific DAGs that match common batch monitoring needs.

### 1. Generate model performance reports as a batch job

You can generate an Evidently report (e.g. a data drift report) every time the new data arrives. You can then store it in your file system.&#x20;

**Here is a DAG example:**

{% embed url="https://github.com/evidentlyai/evidently/blob/main/evidently/tutorials/airflow_drift_detection/dags/evidently_drift_dashboard.py" %}

### 2. Generate visual performance reports on defined conditions  &#x20;

You might not always need to generate visual reports every time.&#x20;

For example, you can run checks on the model performance and only generate the reports if a certain condition is satisfied. For example, if you detect drift or performance drop. Otherwise, you can simply log the results.

**Here is a DAG example:**

{% embed url="https://github.com/evidentlyai/evidently/blob/main/evidently/tutorials/airflow_drift_detection/dags/evidently_conditional_drift_dashboard_generation.py" %}

It works as the following:

* Run a data drift check by generating an Evidently JSON profile&#x20;
* If the drift is not detected, log the JSON output
* If the drift is detected, generate and store a visual HTML report&#x20;



