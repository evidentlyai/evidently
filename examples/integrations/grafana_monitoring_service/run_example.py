#!/usr/bin/env python3

import argparse
import logging
import os
import shutil
import subprocess

import pandas as pd

# suppress SettingWithCopyWarning: warning
pd.options.mode.chained_assignment = None


def setup_logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler()]
    )


def check_docker_installation():
    logging.info("Check docker version")
    docker_version_result = os.system("docker -v")

    if docker_version_result:
        exit("Docker was not found. Try to install it with https://www.docker.com")


def check_dataset(
    force: bool,
    datasets_path: str,
    dataset_name: str
) -> None:
    logging.info("Check dataset %s", dataset_name)
    dataset_path = os.path.join(datasets_path, dataset_name)

    if os.path.exists(dataset_path):
        if force:
            logging.info("Remove dataset directory %s", dataset_path)
            shutil.rmtree(dataset_path)
            os.makedirs(dataset_path)

        else:
            logging.info("Dataset %s already exists", dataset_name)
            return

    logging.info("Download dataset %s", dataset_name)
    run_script(cmd=["scripts/prepare_datasets.py", "-d", dataset_name, "-p", dataset_path], wait=True)


def download_test_datasets(force: bool):
    datasets_path = os.path.abspath("datasets")
    logging.info("Check datasets directory %s", datasets_path)

    if not os.path.exists(datasets_path):
        logging.info("Create datasets directory %s", datasets_path)
        os.makedirs(datasets_path)

    else:
        logging.info("Datasets directory already exists")

    for dataset_name in ("bike_random_forest", "bike_gradient_boosting", "kdd_k_neighbors_classifier"):
        check_dataset(force, datasets_path, dataset_name)


def run_docker_compose():
    logging.info("Run docker compose")
    run_script(cmd=["docker", "compose", "up", "-d"], wait=True)


def run_script(cmd: list, wait: bool) -> None:
    logging.info("Run %s", " ".join(cmd))
    script_process = subprocess.Popen(" ".join(cmd), stdout=subprocess.PIPE, shell=True)

    if wait:
        script_process.wait()

        if script_process.returncode != 0:
            exit(script_process.returncode)


def send_data_requests():
    os.system("scripts/example_run_request.py")


def stop_docker_compose():
    os.system("docker compose down")


def main(force: bool):
    setup_logger()
    check_docker_installation()
    download_test_datasets(force=force)
    run_docker_compose()
    send_data_requests()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Remove and download again test datasets",
    )
    parameters = parser.parse_args()
    main(force=parameters.force)
