---
description: Run model evaluation or data drift analysis as a part of Airflow DAG.
---

Apache Airflow is an open-source [workflow management tool](https://airflow.apache.org).

You can generate Evidently Reports and Test Suites as a step in the Airflow DAG.

**An integration example is available as a Docker container:**

{% embed url="https://github.com/evidentlyai/evidently/tree/main/examples/integrations/airflow_drift_detection" %}

Follow the readme to install and modify the example. You can execute different Evidently Reports and Test Suites in a similar fashion.

It contains several specific DAGs that match common batch monitoring needs.

![](<../.gitbook/assets/integrations/airflow_evidently_dags-min.png>)

## 1. Generate model performance reports as a batch job

You can generate an Evidently HTML report (e.g., a data drift report) every time new data arrives. You can then store it at a defined destination. To perform drift analysis, you must also provide a reference dataset to compare the new data against it.

**Here is a DAG example:**

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/airflow_drift_detection/dags/evidently_drift_report.py" %}

## 2. Generate visual performance reports on defined conditions 

You might not need to generate visual reports every time.

For example, you can perform model performance checks and only generate the visual reports if a certain condition is satisfied. For example, if you detect drift or performance drop. Otherwise, you can simply log the results.

In this example, you perform drift checks without generating the visual report. In case drift is detected, the visual report is generated for debugging.

**Here is a DAG example:**

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/airflow_drift_detection/dags/evidently_conditional_drift_report_generation.py" %}

## 3. Run test suites to perform multiple checks 

![](<../.gitbook/assets/integrations/airflow_dag_test_suite-min.png>)

To perform multiple checks with explicit pass/fail results, you can use Test Suites. In this example, you create a Test Suite that is made from individual tests related to data quality and drift. If all tests pass, you simply log the results. If some tests fail, you generate a summary report for debugging. 

Using Test Suites instead of Reports is recommended for production use and automation. This way, you can conveniently specify the condition for each test and structure your evaluation.

**Here is a DAG example:**

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/airflow_drift_detection/dags/evidently_test_suite.py" %}
