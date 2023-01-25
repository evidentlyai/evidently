import json
import os
from datetime import datetime
from datetime import timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import ShortCircuitOperator
from sklearn import datasets

from evidently.metric_preset import DataDriftPreset
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report

default_args = {
    "start_date": datetime(2020, 1, 1),
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dir_path = "reports"
file_path = "data_drift_report_by_airflow.html"


# evaluate data drift with Evidently Profile
def _detect_dataset_drift(reference, production, column_mapping):
    """
    Returns True if Data Drift is detected, else returns False.
    If get_ratio is True, returns ration of drifted features.
    The Data Drift detection depends on the confidence level and the threshold.
    For each individual feature Data Drift is detected with the selected confidence (default value is 0.95).
    Data Drift for the dataset is detected
        if share of the drifted features is above the selected threshold (default value is 0.5).
    """

    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=reference, current_data=production, column_mapping=column_mapping)

    report = data_drift_report.as_dict()

    return report["metrics"][0]["result"]["dataset_drift"]


def load_data_execute(**context):
    data = datasets.load_boston()
    data_frame = pd.DataFrame(data.data, columns=data.feature_names)

    data_columns = ColumnMapping()
    data_columns.numerical_features = [
        "CRIM",
        "ZN",
        "INDUS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT",
    ]

    data_columns.categorical_features = ["CHAS", "RAD"]

    context["ti"].xcom_push(key="data_frame", value=data_frame)
    context["ti"].xcom_push(key="data_columns", value=data_columns)


def drift_analysis_execute(**context):
    data = context.get("ti").xcom_pull(key="data_frame")
    data_columns = context.get("ti").xcom_pull(key="data_columns")

    dataset_drift = _detect_dataset_drift(data[:200], data[200:], column_mapping=data_columns)

    if dataset_drift:
        return "create_report"


def create_report_execute(**context):
    data = context.get("ti").xcom_pull(key="data_frame")
    data_columns = context.get("ti").xcom_pull(key="data_columns")
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=data[:200], current_data=data[200:], column_mapping=data_columns)

    try:
        os.mkdir(dir_path)
    except OSError:
        print("Creation of the directory {} failed".format(dir_path))

    data_drift_report.save_html(os.path.join(dir_path, file_path))


with DAG(
    dag_id="evidently_conditional_drift_report",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=load_data_execute,
        provide_context=True,
        op_kwargs={"parameter_variable": "parameter_value"},  # not used now
    )

    drift_analysis = PythonOperator(
        task_id="drift_analysis",
        python_callable=drift_analysis_execute,
        provide_context=True,
    )

    create_report = PythonOperator(
        task_id="create_report",
        provide_context=True,
        python_callable=create_report_execute,
    )


load_data >> drift_analysis >> [create_report]
