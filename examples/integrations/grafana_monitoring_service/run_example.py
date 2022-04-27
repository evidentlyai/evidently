#!/usr/bin/env python3

import argparse
import os
import logging
import io
import json
import shutil
import subprocess
import zipfile
from typing import Callable

import pandas as pd
import requests
from sklearn import neighbors
from sklearn import model_selection
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor


# suppress SettingWithCopyWarning: warning
pd.options.mode.chained_assignment = None


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )


def check_docker_installation():
    logging.info("Check docker version")
    docker_version_result = os.system("docker -v")

    if docker_version_result:
        exit("Docker was not found. Try to install it with https://www.docker.com")


def check_dataset(
        force: bool,
        datasets_path: str,
        dataset_name: str,
        get_dataset_method: Callable
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

    else:
        os.makedirs(dataset_path)

    reference_data, production_data = get_dataset_method()
    reference_data.to_csv(os.path.join(dataset_path, "reference.csv"), index=False)
    production_data.to_csv(os.path.join(dataset_path, "production.csv"), index=False)
    logging.info("Dataset %s is downloaded", dataset_name)


def get_data_bike():
    logging.info(f"Load data for dataset bike")
    data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"
    content = requests.get(data_url).content

    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        with arc.open("day.csv") as datafile:
            raw_data = pd.read_csv(datafile, header=0, sep=",", parse_dates=["dteday"])

    reference_bike_data = raw_data[:120]
    production_bike_data = raw_data[120:]

    target = "cnt"
    numerical_features = ["mnth", "temp", "atemp", "hum", "windspeed"]
    categorical_features = ["season", "holiday", "weekday", "workingday", "weathersit"]

    features = numerical_features + categorical_features

    logging.info(f"num features: {json.dumps(numerical_features)}")
    logging.info(f"cat features: {json.dumps(categorical_features)}")
    logging.info(f"target: {target}")

    # get predictions
    model = BaggingRegressor(random_state=0)
    model.fit(reference_bike_data[features], reference_bike_data[target])
    reference_bike_data["prediction"] = model.predict(reference_bike_data[features])
    production_bike_data["prediction"] = model.predict(production_bike_data[features])
    return reference_bike_data, production_bike_data


def get_data_iris_classification():
    logging.info(f"Load data for dataset iris")
    from sklearn import datasets
    iris = datasets.load_iris()
    iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_frame['target'] = iris.target
    reference_data, production_data = model_selection.train_test_split(iris_frame, random_state=0)
    model = neighbors.KNeighborsClassifier(n_neighbors=1)
    model.fit(reference_data[iris.feature_names], reference_data.target)
    reference_prediction = model.predict(reference_data[iris.feature_names])
    production_prediction = model.predict(production_data[iris.feature_names])
    reference_data['prediction'] = reference_prediction
    production_data['prediction'] = production_prediction
    return reference_data, production_data


def get_data_kdd_classification():
    logging.info(f"Load data for dataset kddcup99")

    # local import for make other cases faster
    from sklearn.datasets import fetch_kddcup99

    data = fetch_kddcup99(as_frame=True)
    features = list(set(data.feature_names) - {"protocol_type", "service", "flag"})
    reference_kdd_data, production_kdd_data = model_selection.train_test_split(
        data.frame, random_state=0, train_size=0.2, test_size=0.1
    )
    target = data.target_names[0]
    reference_kdd_data.reset_index(inplace=True, drop=True)
    reference_kdd_data[target] = reference_kdd_data[target].apply(lambda x: x.decode("utf8"))
    production_kdd_data.reset_index(inplace=True, drop=True)
    production_kdd_data[target] = production_kdd_data[target].apply(lambda x: x.decode("utf8"))

    classification_model = neighbors.KNeighborsClassifier(n_neighbors=1)
    classification_model.fit(reference_kdd_data[features], reference_kdd_data[target])

    reference_kdd_data["prediction"] = classification_model.predict(reference_kdd_data[features])
    production_kdd_data["prediction"] = classification_model.predict(production_kdd_data[features])

    return reference_kdd_data[features + [target, "prediction"]], production_kdd_data
    

def download_test_datasets(force: bool):
    datasets_path = os.path.abspath("datasets")
    logging.info("Check datasets directory %s", datasets_path)

    if not os.path.exists(datasets_path):
        logging.info("Create datasets directory %s", datasets_path)
        os.makedirs(datasets_path)

    else:
        logging.info("Datasets directory already exists")

    for dataset_name, get_dataset_method in (
            ("bike_random_forest", get_data_bike),
            ("kdd_k_neighbors_classifier", get_data_kdd_classification),
            ("iris", get_data_iris_classification),
    ):
        check_dataset(force, datasets_path, dataset_name, get_dataset_method)


def run_applications():
    with subprocess.Popen("docker compose up", stdout=subprocess.PIPE, shell=True):
        os.system("./example_run_request.py")


def main(force: bool):
    setup_logger()
    check_docker_installation()
    download_test_datasets(force=force)
    run_applications()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    parser.add_argument(
        "-f",
        "--force",
        action='store_true',
        help="Remove and download again test datasets",
    )
    parameters = parser.parse_args()
    main(force=parameters.force)
