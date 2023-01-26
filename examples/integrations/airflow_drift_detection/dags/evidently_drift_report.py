try:
    import os
    from datetime import datetime
    from datetime import timedelta

    import pandas as pd
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from sklearn import datasets

    from evidently.metric_preset import DataDriftPreset
    from evidently.pipeline.column_mapping import ColumnMapping
    from evidently.report import Report

except Exception as e:
    print("Error  {} ".format(e))

dir_path = "reports"
file_path = "boston_data_drift_by_airflow.html"


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

    boston_data_drift_report = Report(metrics=[DataDriftPreset()])
    boston_data_drift_report.run(reference_data=data[:200], current_data=data[200:], column_mapping=data_columns)

    try:
        os.mkdir(dir_path)
    except OSError:
        print("Creation of the directory {} failed".format(dir_path))

    boston_data_drift_report.save_html(os.path.join(dir_path, file_path))


with DAG(
    dag_id="evidently_drift_report",
    schedule_interval="@daily",
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 1, 1),
    },
    catchup=False,
) as f:

    load_data_execute = PythonOperator(
        task_id="load_data_execute",
        python_callable=load_data_execute,
        provide_context=True,
        op_kwargs={"parameter_variable": "parameter_value"},  # not used now, may be used to specify data
    )

    drift_analysis_execute = PythonOperator(
        task_id="drift_analysis_execute",
        python_callable=drift_analysis_execute,
        provide_context=True,
    )

load_data_execute >> drift_analysis_execute
