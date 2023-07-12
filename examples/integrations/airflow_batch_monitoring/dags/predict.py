import os

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from config import BATCH_INTERVAL
from config import END_DATE_TIME
from config import START_DATE_TIME

dag = DAG(
    dag_id="predict",
    start_date=pendulum.parse(START_DATE_TIME),
    end_date=pendulum.parse(END_DATE_TIME),
    schedule_interval="@hourly",
    max_active_runs=1,
)

with dag:

    PROJECT_DIR = os.environ["PROJECT_DIR"]
    TS = "{{ ts }}"  # The DAG run’s logical date

    predict_task = BashOperator(
        task_id="predict_task",
        bash_command=f"""

            cd $PROJECT_DIR && echo $PWD && \
            export PYTHONPATH=. && echo $PYTHONPATH && \

            python src/pipelines/predict.py \
                --ts { TS } \
                --interval { BATCH_INTERVAL }
        """,
    )

    predict_task
