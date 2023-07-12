ARG PYTHON_BASE_IMAGE="apache/airflow:slim-2.6.2-python3.10"
ARG PYTHON_MAJOR_MINOR_VERSION="3.9"

FROM ${PYTHON_BASE_IMAGE} as airflow-build-image
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

# Make sure noninteractive debian install is used and language variables set
ENV DEBIAN_FRONTEND=noninteractive LANGUAGE=C.UTF-8 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    LC_CTYPE=C.UTF-8 LC_MESSAGES=C.UTF-8

ARG AIRFLOW_PIP_VERSION=23.1.2

# By default PIP has progress bar but you can disable it.
ARG PIP_PROGRESS_BAR="on"

COPY docker/airflow_base/requirements.txt airflow_requirements.txt
RUN pip install --no-cache-dir --upgrade "pip==${AIRFLOW_PIP_VERSION}" && \
    pip install --no-cache-dir -r airflow_requirements.txt && \
    rm airflow_requirements.txt

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade "pip==${AIRFLOW_PIP_VERSION}" && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt 
    
ARG AIRFLOW_HOME=/opt/airflow
ARG AIRFLOW_UID="1000"
ARG AIRFLOW_GID="1000"
ENV AIRFLOW_UID=${AIRFLOW_UID}
ENV AIRFLOW_GID=${AIRFLOW_GID}

ARG AIRFLOW_USER_HOME_DIR=/home/airflow
ENV AIRFLOW_USER_HOME_DIR=${AIRFLOW_USER_HOME_DIR}

ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Make Airflow files belong to the root group and are accessible. This is to accommodate the guidelines from
# OpenShift https://docs.openshift.com/enterprise/3.0/creating_images/guidelines.html
RUN mkdir -pv "${AIRFLOW_HOME}"; \
    mkdir -pv "${AIRFLOW_HOME}/dags"; \
    mkdir -pv "${AIRFLOW_HOME}/logs"; \
    chown -R "airflow:root" "${AIRFLOW_USER_HOME_DIR}" "${AIRFLOW_HOME}"; \
    find "${AIRFLOW_HOME}" -executable -print0 | xargs --null chmod g+x && \
        find "${AIRFLOW_HOME}" -print0 | xargs --null chmod g+rw

ENV PATH="${AIRFLOW_USER_HOME_DIR}/.local/bin:${PATH}"
ENV GUNICORN_CMD_ARGS="--worker-tmp-dir /dev/shm"

WORKDIR ${AIRFLOW_HOME}

EXPOSE 8080

USER ${AIRFLOW_UID}