try:
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    
    from datetime import datetime, timedelta
    import pandas as pd
    from sklearn import datasets
    import os

    from evidently.dashboard import Dashboard
    from evidently.tabs import DataDriftTab

    from evidently.model_profile import Profile
    from evidently.profile_sections import DataDriftProfileSection

except Exception as e:
    print("Error  {} ".format(e))

dir_path = 'reports'
file_path = 'boston_data_drift_by_airflow.html'

def load_data_execute(**context):
    print("load_data_execute   ")

    boston = datasets.load_boston()
    boston_frame = pd.DataFrame(boston.data, columns = boston.feature_names)

    context['ti'].xcom_push(key='boston_frame', value=boston_frame)


def drift_analysis_execute(**context):
    data = context.get("ti").xcom_pull(key='boston_frame')

    boston_data_drift_dashboard = Dashboard(tabs=[DataDriftTab])
    boston_data_drift_dashboard.calculate(data[:200], data[200:])

    try:
        os.mkdir(dir_path)
    except OSError:
        print ("Creation of the directory {} failed".format(dir_path))

    boston_data_drift_dashboard.save(os.path.join(dir_path, file_path))


with DAG(
        dag_id="evidently_drift_dashboard",
        schedule_interval="@daily",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2021, 1, 1),
        },
        catchup=False) as f:

    load_data_execute = PythonOperator(
        task_id="load_data_execute",
        python_callable=load_data_execute,
        provide_context=True,
        op_kwargs={"parameter_variable":"parameter_value"} #not used now, may be used to specify data
    )

    drift_analysis_execute = PythonOperator(
        task_id="drift_analysis_execute",
        python_callable=drift_analysis_execute,
        provide_context=True,
    )

load_data_execute >> drift_analysis_execute


