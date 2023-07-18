import os
from pathlib import Path

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.filesystem import FileSensor
from config import BATCH_INTERVAL
from config import END_DATE_TIME
from config import MODELS_DIR
from config import START_DATE_TIME
from dateutil.relativedelta import relativedelta

dag = DAG(
    dag_id="monitor_model",
    start_date=pendulum.parse(START_DATE_TIME).add(minutes=BATCH_INTERVAL),
    end_date=pendulum.parse(END_DATE_TIME),
    schedule_interval="@hourly",
    max_active_runs=1,
)

with dag:

    PROJECT_DIR = os.environ["PROJECT_DIR"]
    TS = "{{ ts }}"  # The DAG run’s logical date

    wait_predictions = ExternalTaskSensor(
        task_id="wait_predictions",
        external_dag_id="predict",
        external_task_id="predict_task",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
        execution_date_fn=lambda exec_date: exec_date
        - relativedelta(minutes=BATCH_INTERVAL),
        poke_interval=30,
    )

    model_path = f'{Path(PROJECT_DIR).absolute() / f"{MODELS_DIR}/model.joblib"}'
    check_model_exist = FileSensor(
        task_id="check_model_exist", filepath=model_path, timeout=10
    )

    monitor_model = BashOperator(
        task_id="monitor_model",
        bash_command=f"""

            cd $PROJECT_DIR && echo $PWD && \
            export PYTHONPATH=. && echo $PYTHONPATH && \

            python src/pipelines/monitor_model.py \
                --ts { TS } \
                --interval { BATCH_INTERVAL }
        """,
    )

    wait_predictions >> monitor_model
    check_model_exist >> monitor_model
