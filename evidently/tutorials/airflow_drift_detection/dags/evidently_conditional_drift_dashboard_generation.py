from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.operators.python_operator import BranchPythonOperator

from datetime import datetime, timedelta
import pandas as pd
from sklearn import datasets
import os
import json

from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

default_args = {
	"start_date": datetime(2020, 1, 1),
	"owner": "airflow",
	"retries": 1,
	"retry_delay": timedelta(minutes=5),
}

dir_path = 'reports'
file_path = 'data_drift_dashboard_by_airflow.html'

#evaluate data drift with Evidently Profile
def _detect_dataset_drift(reference, production, column_mapping, confidence=0.95, threshold=0.5, get_ratio=False):
    """
    Returns True if Data Drift is detected, else returns False.
    If get_ratio is True, returns ration of drifted features.
    The Data Drift detection depends on the confidence level and the threshold.
    For each individual feature Data Drift is detected with the selected confidence (default value is 0.95).
    Data Drift for the dataset is detected if share of the drifted features is above the selected threshold (default value is 0.5).
    """
    
    data_drift_profile = Profile(sections=[DataDriftProfileSection])
    data_drift_profile.calculate(reference, production, column_mapping=column_mapping)
    report = data_drift_profile.json()
    json_report = json.loads(report)

    drifts = []
    num_features = column_mapping.get('numerical_features') if column_mapping.get('numerical_features') else []
    cat_features = column_mapping.get('categorical_features') if column_mapping.get('categorical_features') else []
    for feature in num_features + cat_features:
        drifts.append(json_report['data_drift']['data']['metrics'][feature]['p_value']) 
        
    n_features = len(drifts)
    n_drifted_features = sum([1 if x<(1. - confidence) else 0 for x in drifts])
    
    if get_ratio:
        return n_drifted_features/n_features
    else:
        return True if n_drifted_features/n_features >= threshold else False


def load_data_execute(**context):
	#print("load_data_execute   ")
	data = datasets.load_boston()
	data_frame = pd.DataFrame(data.data, columns=data.feature_names)

	data_columns = {}
	data_columns['numerical_features'] = ['CRIM', 'ZN', 'INDUS', 'NOX', 'RM', 'AGE', 'DIS', 'TAX','PTRATIO', 'B', 'LSTAT']
	#data_columns['categorical_features'] = ['CHAS', 'RAD']

	context['ti'].xcom_push(key='data_frame', value=data_frame)
	context['ti'].xcom_push(key='data_columns', value=data_columns)

def drift_analysis_execute(**context):
	#print("drift_analysis_execute   ")
	data = context.get("ti").xcom_pull(key='data_frame')
	data_columns = context.get("ti").xcom_pull(key='data_columns')

	dataset_drift = _detect_dataset_drift(
		data[:200], 
		data[200:],
		column_mapping=data_columns)

	context['ti'].xcom_push(key='dataset_drift', value=dataset_drift)


def detect_drift_execute(**context):
	#print("detect_drift_execute   ")
	drift = context.get("ti").xcom_pull(key='dataset_drift')
	if drift:
		return 'create_dashboard'

def create_dashboard_execute(**context):
	print("create_dashboard_execute   ")
	data = context.get("ti").xcom_pull(key='data_frame')
	print("data")
	data_drift_dashboard = Dashboard(tabs=[DataDriftTab])
	data_drift_dashboard.calculate(data[:200], data[200:])

	try:
		os.mkdir(dir_path)
	except OSError:
		print ("Creation of the directory {} failed".format(dir_path))

	data_drift_dashboard.save(os.path.join(dir_path, file_path))


with DAG(
	dag_id='evidently_conditional_drift_dashboard_generation', 
	schedule_interval='@daily', 
	default_args=default_args, 
	catchup=False) as dag:

	load_data = PythonOperator(
		task_id="load_data",
		python_callable=load_data_execute,
		provide_context=True,
		op_kwargs={"parameter_variable":"parameter_value"} #not used now
	)

	drift_analysis = PythonOperator(
		task_id="drift_analysis",
		python_callable=drift_analysis_execute,
		provide_context=True,
	)

	detect_drift = ShortCircuitOperator(
		task_id='detect_drift',
		python_callable=detect_drift_execute,
		provide_context=True,
		do_xcom_push=False, 
	)

	create_dashboard = PythonOperator(
		task_id='create_dashboard',
		provide_context=True,
		python_callable=create_dashboard_execute
	)


load_data >> drift_analysis >> detect_drift >> [create_dashboard]

