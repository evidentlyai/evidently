import os

import pendulum
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor

from airflow import DAG
from config import BATCH_INTERVAL, END_DATE_TIME, START_DATE_TIME

dag = DAG(
    dag_id="monitor_prediction",
    start_date=pendulum.parse(START_DATE_TIME),
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
        execution_date_fn=lambda exec_date: exec_date,
        poke_interval=30,
    )

    monitor_prediction = BashOperator(
        task_id="monitor_prediction",
        bash_command=f"""

            cd $PROJECT_DIR && echo $PWD && \
            export PYTHONPATH=. && echo $PYTHONPATH && \

            python src/pipelines/monitor_prediction.py \
                --ts { TS } \
                --interval { BATCH_INTERVAL }
        """,
    )

    monitor_prediction
